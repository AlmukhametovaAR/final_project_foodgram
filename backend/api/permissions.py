from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    """
    Object-level permission
    that allows editing and deleting a record only for its author.
    """
    message = 'Changing and deleting someone else\'s recipe is not allowed!'

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
