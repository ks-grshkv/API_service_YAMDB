from rest_framework import permissions
from users.models import Roles


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == Roles.admin

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:         
            return True   
        return request.user.is_authenticated and request.user.role == Roles.admin


class OwnerModAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.role == Roles.moderator
                or request.user.role == Roles.admin)
