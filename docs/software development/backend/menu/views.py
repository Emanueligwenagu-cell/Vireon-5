from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import MenuItem
from .serializers import MenuItemSerializer


class IsOwningVendorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.role == "admin":
            return True
        return obj.vendor.owner_id == request.user.id


class MenuItemViewSet(viewsets.ModelViewSet):
    """
    /api/menu/?vendor=1&category=pizza&search=wrap    GET (public)
    /api/menu/                                         POST (owning vendor)
    /api/menu/{id}/                                     PATCH/DELETE (owning vendor or admin)
    """

    queryset = MenuItem.objects.select_related("vendor").filter(is_available=True, vendor__is_approved=True)
    serializer_class = MenuItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["vendor", "category", "is_available"]
    search_fields = ["name", "description"]
    ordering_fields = ["price", "prep_time_minutes", "name"]

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [permissions.IsAuthenticated(), IsOwningVendorOrReadOnly()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        # Vendors managing their own menu (including hidden/unavailable items) pass ?mine=1
        if self.request.query_params.get("mine") == "1" and self.request.user.is_authenticated:
            return MenuItem.objects.select_related("vendor").filter(vendor__owner=self.request.user)
        return super().get_queryset()
