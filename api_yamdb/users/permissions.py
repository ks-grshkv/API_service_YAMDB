from rest_framework import permissions

from .models import Roles


class IsAuth(permissions.BasePermission):

    def has_permission(self, request, view):
        print('dddddddddd')
        return True

    def has_object_permission(self, request, view, obj):
        print('sssssssss')
        return True


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        print('AAAAAAAAAA')
        return (
            request.user.is_authenticated
            and request.user.role == Roles.admin
        )

    def has_object_permission(self, request, view, obj):
        print('AAAAAAAAAA')
        return (
            request.user.is_authenticated
            and request.user.role == Roles.admin
        )


class IsAdminOrSelf(permissions.BasePermission):

    def has_permission(self, request, view):
        print('cccccccccccc')
        return (
            request.user.is_authenticated
            and request.user.role == Roles.admin
        ) or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        print('ssswwsssswww')
        return request.user.is_superuser or (
            request.user.is_authenticated
            and request.user.role == Roles.admin
        ) or request.user.username == obj.user.username
