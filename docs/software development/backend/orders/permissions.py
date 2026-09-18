from rest_framework.permissions import BasePermission


class IsOrderStudentVendorOrAdmin(BasePermission):
    """A student sees/cancels their own orders; a vendor sees/updates orders placed at their stall; admins see all."""

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role == "admin":
            return True
        if user.role == "student":
            return obj.student_id == user.id
        if user.role == "vendor":
            return obj.vendor.owner_id == user.id
        return False
