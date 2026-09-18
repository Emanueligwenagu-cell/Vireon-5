from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from accounts.permissions import IsStudent
from .models import Order
from .permissions import IsOrderStudentVendorOrAdmin
from .serializers import OrderCreateSerializer, OrderSerializer, OrderStatusUpdateSerializer


class OrderViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                    mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    POST /api/orders/                place an order (student)
    GET  /api/orders/                 list *my* relevant orders (student -> own, vendor -> their stall, admin -> all)
    GET  /api/orders/{id}/            view one order (participants + admin only)
    POST /api/orders/{id}/set_status/ move an order forward through its lifecycle (vendor of that order, or admin)
    POST /api/orders/{id}/cancel/     cancel a still-pending order (the student who placed it, or admin)
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Order.objects.select_related("student", "vendor").prefetch_related("items")
        if user.role == "admin":
            return qs
        if user.role == "vendor":
            return qs.filter(vendor__owner=user)
        return qs.filter(student=user)

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return OrderSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated(), IsStudent()]
        if self.action in ("retrieve", "set_status", "cancel"):
            return [permissions.IsAuthenticated(), IsOrderStudentVendorOrAdmin()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def set_status(self, request, pk=None):
        order = self.get_object()
        if request.user.role not in ("vendor", "admin"):
            return Response({"detail": "Only the vendor or an admin can update order status."}, status=status.HTTP_403_FORBIDDEN)
        serializer = OrderStatusUpdateSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(OrderSerializer(order).data)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if request.user.role not in ("student", "admin"):
            return Response({"detail": "Only the student or an admin can cancel an order."}, status=status.HTTP_403_FORBIDDEN)
        if request.user.role == "student" and order.student_id != request.user.id:
            return Response({"detail": "You can only cancel your own order."}, status=status.HTTP_403_FORBIDDEN)
        if order.status != Order.Status.PENDING:
            return Response({"detail": "Only a pending order can be cancelled."}, status=status.HTTP_400_BAD_REQUEST)
        order.status = Order.Status.CANCELLED
        order.save(update_fields=["status"])
        return Response(OrderSerializer(order).data)
