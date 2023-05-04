from rest_framework import permissions
from rest_framework.views import View
from users.models import User


class IsAccountEmployee(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        return (
            request.user.is_authenticated
            and request.user.is_superuser
            or obj == request.user
        )

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated and request.user.is_superuser
