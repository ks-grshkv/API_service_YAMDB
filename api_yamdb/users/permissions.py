from rest_framework import permissions

from .models import Roles


class IsAdminOrSuper(permissions.BasePermission):

    def has_permission(self, request, view):

        verdict = (
            request.user.is_authenticated
            and request.user.role == Roles.admin.name
        ) or request.user.is_superuser
        return verdict

    def has_object_permission(self, request, view, obj):

        verdict = request.user.is_superuser or (
            request.user.is_authenticated
            and request.user.role == Roles.admin.name
        ) or request.user.username == obj.user.username
        return verdict


class IsAuth(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated
