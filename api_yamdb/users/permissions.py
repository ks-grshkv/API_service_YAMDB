from rest_framework import permissions

from .models import Roles


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == Roles.admin
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and request.user.role == Roles.admin
        )


class IsAdminOrSelf(permissions.BasePermission):

    def has_permission(self, request, view):
        verdict = (
            request.user.is_authenticated
            and request.user.role == Roles.admin
        ) or request.user.is_superuser
        return verdict

    def has_object_permission(self, request, view, obj):
        verdict = request.user.is_superuser or (
            request.user.is_authenticated
            and request.user.role == Roles.admin
        ) or request.user.username == obj.user.username
        return verdict


class IsAdminOrAuth(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated
