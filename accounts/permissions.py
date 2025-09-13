from rest_framework import permissions

class IsAdminOrStaffOrSuperuser(permissions.BasePermission):
    """
    Allows access only to users who are:
    - Staff (is_staff=True)
    - Superuser (is_superuser=True)
    - Role is 'admin' (role='admin')
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        return user.is_staff or user.is_superuser or getattr(user, "role", None) == "admin"
