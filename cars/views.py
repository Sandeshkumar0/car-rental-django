from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend

from .models import Car
from .serializers import CarSerializer
from .pagination import CarPagination

from bookings.models import Booking
from bookings.services import is_car_available
from datetime import date



# =========================
# TEMPLATE VIEWS (HTML UI)
# =========================

@login_required
def car_detail_view(request, car_id):
    car = get_object_or_404(Car, id=car_id, is_active=True)
    error = None

    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        if start_date >= end_date:
            error = "End date must be after start date."

        elif not is_car_available(car, start_date, end_date):
            error = "Car is not available for selected dates."

        else:
            Booking.objects.create(
                user=request.user,
                car=car,
                start_date=start_date,
                end_date=end_date,
            )
            return redirect("my-bookings")

    return render(
    request,
    "car_detail.html",
    {
        "car": car,
        "error": error,
        "today": date.today().isoformat(),
    },
)


# =========================
# API VIEWS (DRF)
# =========================

class CarListAPIView(generics.ListAPIView):
    """
    Public API: list cars
    """
    queryset = Car.objects.filter(is_active=True)
    serializer_class = CarSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = CarPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["brand"]


class CarCreateAPIView(generics.CreateAPIView):
    """
    Admin API: create car
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAdminUser]
