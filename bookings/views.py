# from rest_framework import generics, permissions
# from .models import Booking
# from .serializers import BookingSerializer


# class BookingCreateAPIView(generics.CreateAPIView):
#     serializer_class = BookingSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class BookingListAPIView(generics.ListAPIView):
#     serializer_class = BookingSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Booking.objects.filter(user=self.request.user)


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Booking
from .serializers import BookingSerializer
from .permissions import IsOwnerOrAdmin
from .services import cancel_booking


# ==================================================
# UI (TEMPLATE-BASED, SESSION AUTH)
# ==================================================

@login_required
def cancel_booking_view(request, booking_id):
    """
    Cancel booking from Django template (session-based auth)
    """
    if request.method != "POST":
        return HttpResponseForbidden("Invalid request method")

    booking = get_object_or_404(Booking, id=booking_id)

    # Only owner or admin can cancel
    if booking.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("Not allowed")

    cancel_booking(booking)
    return redirect("my-bookings")


# ==================================================
# API (JWT-BASED)
# ==================================================

class BookingCreateAPIView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookingListAPIView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


class BookingCancelAPIView(generics.UpdateAPIView):
    """
    API: Cancel a booking (soft cancel, JWT protected)
    """
    queryset = Booking.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def update(self, request, *args, **kwargs):
        booking = self.get_object()

        try:
            cancel_booking(booking)
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"message": "Booking cancelled successfully"},
            status=status.HTTP_200_OK
        )


class AdminBookingListAPIView(generics.ListAPIView):
    """
    Admin API: View all bookings
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "car", "user"]
