from rest_framework.permissions import BasePermission, SAFE_METHODS


# class ReadOnlyOrAuthorizedCreateOrAuthorModerAdminEdit(BasePermission):
class SimpleResourceUsage(BasePermission):
    """ Read only for not authorized users or POST for authorized """
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            return True
        else:
            return request.method in SAFE_METHODS

    """Read only or admin/moder/author edit object"""
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated:
            if user.is_admin or user.is_staff or obj.author == user:
                return True
            return False
        else:
            return request.method in SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin
        return request.method in SAFE_METHODS


class IsCustomAdminUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin
        return False
