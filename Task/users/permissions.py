from rest_framework import permissions
from .models import User


class Check(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.roleId == User.ADMIN or (request.user and request.user.is_logged_in)
        return request.user and request.user.is_authenticated and request.user.roleId == User.ADMIN

    def has_object_permission(self, request, view, obj):
        return obj == request.user.roleId == User.ADMIN or (request.user and request.user.is_logged_in)