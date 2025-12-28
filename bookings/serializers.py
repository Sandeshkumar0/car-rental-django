# from rest_framework import serializers
# from .models import Booking
# from .services import is_car_available


# class BookingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Booking
#         fields = ["id", "car", "start_date", "end_date"]

#     def validate(self, data):
#         if data["start_date"] >= data["end_date"]:
#             raise serializers.ValidationError("End date must be after start date")

#         if not is_car_available(
#             data["car"], data["start_date"], data["end_date"]
#         ):
#             raise serializers.ValidationError("Car is not available for these dates")

#         return data

#     def create(self, validated_data):
#         return Booking.objects.create(
#             user=self.context["request"].user,
#             **validated_data
#         )


from rest_framework import serializers
from django.utils import timezone

from .models import Booking
from .services import is_car_available


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "car", "start_date", "end_date", "status"]
        read_only_fields = ["status"]

    def validate(self, data):
        start = data["start_date"]
        end = data["end_date"]

        if start >= end:
            raise serializers.ValidationError("End date must be after start date")

        if start < timezone.now().date():
            raise serializers.ValidationError("Cannot book in the past")

        if not is_car_available(data["car"], start, end):
            raise serializers.ValidationError("Car not available for selected dates")

        return data

    def create(self, validated_data):
        return Booking.objects.create(
            user=self.context["request"].user,
            **validated_data
        )
