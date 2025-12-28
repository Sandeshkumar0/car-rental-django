# from django.urls import path
# from .views import BookingCreateAPIView, BookingListAPIView

# urlpatterns = [
#     path("create/", BookingCreateAPIView.as_view(), name="booking-create"),
#     path("", BookingListAPIView.as_view(), name="booking-list"),
# ]

# from django.urls import path
# from .views import (
#     BookingCreateAPIView,
#     BookingListAPIView,
#     BookingCancelAPIView,
# )

# urlpatterns = [
#     path("", BookingListAPIView.as_view(), name="booking-list"),
#     path("create/", BookingCreateAPIView.as_view(), name="booking-create"),
#     path("<int:pk>/cancel/", BookingCancelAPIView.as_view(), name="booking-cancel"),
# ]

# from django.urls import path
# from .views import (
#     BookingCreateAPIView,
#     BookingListAPIView,
#     BookingCancelAPIView,
#     AdminBookingListAPIView,
# )

# urlpatterns = [
#     path("", BookingListAPIView.as_view(), name="booking-list"),
#     path("create/", BookingCreateAPIView.as_view(), name="booking-create"),
#     path("<int:pk>/cancel/", BookingCancelAPIView.as_view(), name="booking-cancel"),
#     path("admin/all/", AdminBookingListAPIView.as_view(), name="admin-bookings"),
# ]


from django.urls import path
from .views import (
    BookingCreateAPIView,
    BookingListAPIView,
    BookingCancelAPIView,
    AdminBookingListAPIView,
    cancel_booking_view,   # ✅ ADD THIS
)

urlpatterns = [
    # UI (Template-based cancel)
    path(
        "cancel-ui/<int:booking_id>/",
        cancel_booking_view,
        name="booking-cancel-ui",
    ),

    # API (JWT-based)
    path("", BookingListAPIView.as_view(), name="booking-list"),
    path("create/", BookingCreateAPIView.as_view(), name="booking-create"),
    path("<int:pk>/cancel/", BookingCancelAPIView.as_view(), name="booking-cancel"),
    path("admin/all/", AdminBookingListAPIView.as_view(), name="admin-bookings"),
]
