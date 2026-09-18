from decimal import Decimal

from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.permissions import IsAdminUser

from .models import PromoCode
from .serializers import PromoCodeSerializer, calculate_discount, get_valid_promo_or_error


class PromoCodeViewSet(viewsets.ModelViewSet):
    """Only admins manage promo codes; anyone authenticated can check one via /check/."""

    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get_permissions(self):
        if self.action == "check":
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    @action(detail=False, methods=["post"])
    def check(self, request):
        code = request.data.get("code", "")
        subtotal = Decimal(str(request.data.get("subtotal", "0")))
        promo = get_valid_promo_or_error(code, subtotal)
        discount = calculate_discount(promo, subtotal)
        return Response({
            "code": promo.code,
            "discount_amount": str(discount),
            "new_total": str(subtotal - discount),
        })
