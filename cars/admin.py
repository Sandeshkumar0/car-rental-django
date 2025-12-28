from django.contrib import admin
from .models import Car, CarImage
from config.admin import custom_admin_site


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1


class CarAdmin(admin.ModelAdmin):
    list_display = ("id", "brand", "name", "price_per_day", "is_active")
    list_filter = ("brand", "is_active")
    search_fields = ("brand", "name")
    inlines = [CarImageInline]


custom_admin_site.register(Car, CarAdmin)
