from rest_framework import mixins, permissions, status, viewsets
from rest_framework.response import Response

from .models import Payment
from .serializers import InitiatePaymentSerializer, PaymentSerializer
from .services import PaymentGatewayUnavailable, get_gateway


class PaymentViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                      mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    POST /api/payments/   {"order": 5, "method": "card"} - charges amount = order.total server-side
    GET  /api/payments/    list the caller's own payments (admin sees all)
    """

    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == "admin":
            return Payment.objects.select_related("order", "student").all()
        return Payment.objects.select_related("order", "student").filter(student=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = InitiatePaymentSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        order = serializer.validated_data["order"]
        method = serializer.validated_data["method"]

        # amount is always order.total from the database - never client-supplied
        try:
            gateway = get_gateway(method)
        except PaymentGatewayUnavailable as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        result = gateway.charge(amount=order.total, method=method, order_id=order.id)

        payment = Payment.objects.create(
            order=order,
            student=request.user,
            method=method,
            amount=order.total,
            status=Payment.Status.SUCCEEDED if result.success else Payment.Status.FAILED,
            provider_reference=result.provider_reference,
        )
        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
