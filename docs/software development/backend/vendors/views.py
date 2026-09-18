from rest_framework import permissions, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.permissions import IsAdminUser, IsVendorUser

from .models import Vendor
from .permissions import IsOwnerVendorOrReadOnly
from .serializers import VendorSerializer


class VendorViewSet(viewsets.ModelViewSet):
    """
    /api/vendors/            GET (public), POST (vendor-role users, one profile each)
    /api/vendors/{id}/       GET (public), PATCH/DELETE (owner or admin)
    /api/vendors/{id}/approve/  POST (admin only)
    """

    queryset = Vendor.objects.select_related("owner").all()
    serializer_class = VendorSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated(), IsVendorUser()]
        if self.action in ("update", "partial_update", "destroy"):
            return [permissions.IsAuthenticated(), IsOwnerVendorOrReadOnly()]
        if self.action == "approve":
            return [permissions.IsAuthenticated(), IsAdminUser()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == "list" and self.request.query_params.get("mine") == "1":
            if self.request.user.is_authenticated and self.request.user.role == "admin":
                return qs
            if self.request.user.is_authenticated and self.request.user.role == "vendor":
                return qs.filter(owner=self.request.user)
            return qs.none()
        if self.action == "list":
            return qs.filter(is_approved=True)
        return qs

    def perform_create(self, serializer):
        if Vendor.objects.filter(owner=self.request.user).exists():
            raise serializers.ValidationError({"detail": "You already have a vendor profile."})
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        vendor = self.get_object()
        vendor.is_approved = True
        vendor.save(update_fields=["is_approved"])
        return Response(VendorSerializer(vendor).data)
