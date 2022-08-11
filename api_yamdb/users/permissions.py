from rest_framework import permissions


class IsUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.role == 'admin'
            or request.user.role == 'Администратор'
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.role == 'admin'
            or request.user.role == 'Администратор'
        )
