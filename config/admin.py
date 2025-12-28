from django.contrib import admin
from django.template.response import TemplateResponse

from cars.models import Car
from bookings.models import Booking


class CustomAdminSite(admin.AdminSite):
    site_header = "Car Rental Administration"
    site_title = "Car Rental Admin"
    index_title = "Dashboard"

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}

        extra_context["stats"] = {
            "total_cars": Car.objects.count(),
            "active_cars": Car.objects.filter(is_active=True).count(),
            "total_bookings": Booking.objects.count(),
            "active_bookings": Booking.objects.filter(status="BOOKED").count(),
            "cancelled_bookings": Booking.objects.filter(status="CANCELLED").count(),
        }

        return super().index(request, extra_context=extra_context)


custom_admin_site = CustomAdminSite(name="custom_admin")
