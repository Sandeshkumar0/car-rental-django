# from django.contrib import admin
# from .models import Booking


# @admin.register(Booking)
# class BookingAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "user",
#         "car",
#         "start_date",
#         "end_date",
#         "status",
#     )
#     list_filter = ("status", "car")
#     search_fields = ("user__email", "car__name")

# from django.contrib import admin
# from .models import Booking

# def cancel_selected_bookings(modeladmin, request, queryset):
#     updated = queryset.filter(status="BOOKED").update(status="CANCELLED")
#     modeladmin.message_user(
#         request,
#         f"{updated} booking(s) successfully cancelled."
#     )


# cancel_selected_bookings.short_description = "Cancel selected bookings"

# @admin.register(Booking)
# class BookingAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "user",
#         "car",
#         "start_date",
#         "end_date",
#         "status",
#         "created_at",
#     )

#     list_filter = ("status", "car")
#     search_fields = ("user__email", "car__name")
#     readonly_fields = (
#         "user",
#         "car",
#         "start_date",
#         "end_date",
#         "created_at",
#     )

#     actions = [cancel_selected_bookings]

#     def has_delete_permission(self, request, obj=None):
#         return False

from django.contrib import admin
from .models import Booking
from config.admin import custom_admin_site


def cancel_selected_bookings(modeladmin, request, queryset):
    updated = queryset.filter(status="BOOKED").update(status="CANCELLED")
    modeladmin.message_user(
        request,
        f"{updated} booking(s) cancelled."
    )


class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "car",
        "start_date",
        "end_date",
        "status",
        "created_at",
    )
    list_filter = ("status", "car")
    readonly_fields = (
        "user",
        "car",
        "start_date",
        "end_date",
        "created_at",
    )
    actions = [cancel_selected_bookings]

    def has_delete_permission(self, request, obj=None):
        return False


custom_admin_site.register(Booking, BookingAdmin)
