from decimal import Decimal

from django.db import transaction
from django.db.models import F
from rest_framework import serializers

from menu.models import MenuItem
from promos.serializers import calculate_discount, get_valid_promo_or_error
from promos.models import PromoCode

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "menu_item", "item_name", "unit_price", "quantity"]
        read_only_fields = ["id", "item_name", "unit_price"]


class OrderItemInputSerializer(serializers.Serializer):
    """What the client actually sends when placing an order: just item + quantity."""

    menu_item = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
    quantity = serializers.IntegerField(min_value=1, max_value=50)


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    student_email = serializers.EmailField(source="student.email", read_only=True)
    vendor_name = serializers.CharField(source="vendor.name", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "student", "student_email", "vendor", "vendor_name", "status",
            "fulfillment_type", "delivery_location", "subtotal", "discount_amount",
            "total", "promo_code", "notes", "items", "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "student", "vendor", "status", "subtotal", "discount_amount",
            "total", "created_at", "updated_at",
        ]


class OrderCreateSerializer(serializers.Serializer):
    """
    Everything money-related (unit prices, subtotal, discount, total) is
    computed here from the database, never taken from the request, so a
    tampered client payload cannot change what the student is charged.
    """

    items = OrderItemInputSerializer(many=True)
    fulfillment_type = serializers.ChoiceField(choices=Order.FulfillmentType.choices, default=Order.FulfillmentType.PICKUP)
    delivery_location = serializers.CharField(required=False, allow_blank=True)
    promo_code = serializers.CharField(required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("An order must contain at least one item.")
        vendor_ids = {item["menu_item"].vendor_id for item in items}
        if len(vendor_ids) > 1:
            raise serializers.ValidationError("All items in one order must be from the same vendor.")
        for item in items:
            mi = item["menu_item"]
            if not item["menu_item"].is_available or not mi.vendor.can_sell:
                raise serializers.ValidationError(f"'{mi.name}' is not currently available.")
        return items

    @transaction.atomic
    def create(self, validated_data):
        request = self.context["request"]
        items_data = validated_data["items"]
        vendor = items_data[0]["menu_item"].vendor

        subtotal = sum((item["menu_item"].price * item["quantity"] for item in items_data), Decimal("0"))

        promo = None
        discount = Decimal("0")
        code = validated_data.get("promo_code", "").strip()
        if code:
            promo = get_valid_promo_or_error(code, subtotal)
            promo = PromoCode.objects.select_for_update().get(pk=promo.pk)
            promo = get_valid_promo_or_error(promo.code, subtotal)
            discount = calculate_discount(promo, subtotal)

        order = Order.objects.create(
            student=request.user,
            vendor=vendor,
            fulfillment_type=validated_data["fulfillment_type"],
            delivery_location=validated_data.get("delivery_location", ""),
            subtotal=subtotal,
            discount_amount=discount,
            total=subtotal - discount,
            promo_code=promo,
            notes=validated_data.get("notes", ""),
        )

        OrderItem.objects.bulk_create([
            OrderItem(
                order=order,
                menu_item=item["menu_item"],
                item_name=item["menu_item"].name,
                unit_price=item["menu_item"].price,
                quantity=item["quantity"],
            )
            for item in items_data
        ])

        if promo:
            promo.times_redeemed = models_f_increment(promo)

        return order


def models_f_increment(promo):
    from django.db.models import F
    promo.__class__.objects.filter(pk=promo.pk).update(times_redeemed=F("times_redeemed") + 1)
    promo.refresh_from_db(fields=["times_redeemed"])
    return promo.times_redeemed


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]

    def validate_status(self, value):
        order = self.instance
        allowed_forward = {
            Order.Status.PENDING: {Order.Status.ACCEPTED, Order.Status.CANCELLED},
            Order.Status.ACCEPTED: {Order.Status.PREPARING, Order.Status.CANCELLED},
            Order.Status.PREPARING: {Order.Status.READY, Order.Status.CANCELLED},
            Order.Status.READY: {Order.Status.OUT_FOR_DELIVERY, Order.Status.COMPLETED},
            Order.Status.OUT_FOR_DELIVERY: {Order.Status.COMPLETED},
        }
        if value not in allowed_forward.get(order.status, set()):
            raise serializers.ValidationError(f"Cannot move an order from '{order.status}' to '{value}'.")
        return value
