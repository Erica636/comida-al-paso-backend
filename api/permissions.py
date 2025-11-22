from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """
    Permiso que solo permite acceso a usuarios con is_staff=True
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff
