from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

from cars.models import Car
from bookings.models import Booking


def home_view(request):
    cars = Car.objects.filter(is_active=True)
    return render(request, "home.html", {"cars": cars})


class UserLoginView(LoginView):
    template_name = "login.html"


class UserLogoutView(LogoutView):
    next_page = "/"


@login_required
def my_bookings_view(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, "bookings.html", {"bookings": bookings})
