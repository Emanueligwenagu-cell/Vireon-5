from django.utils import timezone
from rest_framework import serializers

from .models import PromoCode


class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = [
            "id", "code", "discount_type", "discount_value", "max_percent_cap",
            "min_order_value", "valid_from", "valid_until", "max_redemptions",
            "times_redeemed", "is_active",
        ]
        read_only_fields = ["id", "times_redeemed"]


def get_valid_promo_or_error(code, order_subtotal):
    """
    Shared server-side validation used both by a 'check my code' endpoint and
    by order creation itself, so a promo can never be applied by trusting a
    discount amount the client sends.
    """
    try:
        promo = PromoCode.objects.get(code__iexact=code)
    except PromoCode.DoesNotExist:
        raise serializers.ValidationError({"promo_code": "Invalid promo code."})

    now = timezone.now()
    if not promo.is_active or not (promo.valid_from <= now <= promo.valid_until):
        raise serializers.ValidationError({"promo_code": "This promo code is not currently valid."})
    if promo.max_redemptions is not None and promo.times_redeemed >= promo.max_redemptions:
        raise serializers.ValidationError({"promo_code": "This promo code has been fully redeemed."})
    if order_subtotal < promo.min_order_value:
        raise serializers.ValidationError(
            {"promo_code": f"Order must be at least {promo.min_order_value} to use this code."}
        )
    return promo


def calculate_discount(promo, subtotal):
    if promo.discount_type == PromoCode.DiscountType.FIXED:
        discount = promo.discount_value
    else:
        discount = subtotal * (promo.discount_value / 100)
        if promo.max_percent_cap is not None:
            discount = min(discount, promo.max_percent_cap)
    return min(discount, subtotal)
