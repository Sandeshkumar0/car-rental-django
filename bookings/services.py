from django.utils import timezone
from .models import Booking


def is_car_available(car, start_date, end_date):
    return not Booking.objects.filter(
        car=car,
        status="BOOKED",
        start_date__lt=end_date,
        end_date__gt=start_date,
    ).exists()


def cancel_booking(booking):
    """
    Safely cancel a booking
    """
    if booking.status == "CANCELLED":
        raise ValueError("Booking is already cancelled")

    booking.status = "CANCELLED"
    booking.save()
    return booking
