from django.urls import path
from .views import CarListAPIView, CarCreateAPIView,car_detail_view

urlpatterns = [
    path("", CarListAPIView.as_view(), name="car-list"),
    path("create/", CarCreateAPIView.as_view(), name="car-create"),
    path("<int:car_id>/", car_detail_view, name="car-detail"),
]
