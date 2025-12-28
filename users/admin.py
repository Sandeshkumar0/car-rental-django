# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import User


# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     ordering = ("email",)
#     list_display = ("email", "is_staff", "is_active")
#     search_fields = ("email",)

#     fieldsets = (
#         (None, {"fields": ("email", "password")}),
#         ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
#         ("Important dates", {"fields": ("last_login",)}),
#     )

#     add_fieldsets = (
#         (None, {
#             "classes": ("wide",),
#             "fields": ("email", "password1", "password2"),
#         }),
#     )

#     filter_horizontal = ("groups", "user_permissions")


from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from config.admin import custom_admin_site


class UserAdmin(BaseUserAdmin):
    ordering = ("email",)
    list_display = ("email", "is_staff", "is_active")
    search_fields = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login",)}),
    )


custom_admin_site.register(User, UserAdmin)
