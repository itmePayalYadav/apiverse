from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = ("email", "username", "role", "is_verified", "is_staff")
    
    list_filter = ("role", "is_verified", "is_staff", "login_type")
    
    search_fields = ("email", "username")
    
    ordering = ("email",)
    
    readonly_fields = ("refresh_token", "forgot_password_token", "email_verification_token")
    
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Permissions", {"fields": ("role", "is_verified", "is_staff", "is_superuser")}),
        ("Important tokens", {"fields": ("refresh_token", "forgot_password_token", "email_verification_token")}),
        ("Login Type", {"fields": ("login_type",)}),
    )
    
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2", "role", "is_staff")
        }),
    )
    
admin.site.register(User, UserAdmin)