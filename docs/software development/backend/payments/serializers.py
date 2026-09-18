from rest_framework import serializers

from orders.models import Order

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "order", "student", "method", "status", "amount", "provider_reference", "created_at"]
        read_only_fields = ["id", "student", "status", "amount", "provider_reference", "created_at"]


class InitiatePaymentSerializer(serializers.Serializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    method = serializers.ChoiceField(choices=Payment.Method.choices)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate_order(self, order):
        request = self.context["request"]
        if order.student_id != request.user.id:
            raise serializers.ValidationError("You can only pay for your own order.")
        if order.status != order.Status.PENDING:
            raise serializers.ValidationError("Only pending orders can be paid.")
        if hasattr(order, "payment"):
            raise serializers.ValidationError("This order already has a payment record.")
        return order
