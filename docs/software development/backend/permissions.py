from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_student)


class IsVendorUser(BasePermission):
    """The requesting user has the vendor role (not necessarily owner of a given object)."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_vendor)


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "admin")


class IsSelfOrAdmin(BasePermission):
    """Object-level: users may only view/edit their own account, admins may touch any."""

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True
        return obj == request.user


class ReadOnlyOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.role == "admin")
