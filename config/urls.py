"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.http import JsonResponse


def health_check(request):
    return JsonResponse({"status": "Backend is running"})


# urlpatterns = [
#     path("", health_check),
#     path("admin/", admin.site.urls),
#     path("api/auth/", include("users.urls")),
#     path("api/cars/", include("cars.urls")),
#     path("api/bookings/", include("bookings.urls")),
# ]



# urlpatterns = [

#     path("", health_check),
#     path("admin/", admin.site.urls),

#     path("api/v1/auth/", include("users.urls")),
#     path("api/v1/cars/", include("cars.urls")),
#     path("api/v1/bookings/", include("bookings.urls")),
# ]


from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from config.admin import custom_admin_site

from config.views import (
    home_view,
    UserLoginView,
    UserLogoutView,
    my_bookings_view,
)

from django.conf import settings
from django.conf.urls.static import static


def health_check(request):
    return JsonResponse({"status": "Backend is running"})


urlpatterns = [
    path("admin/", custom_admin_site.urls),

    # Frontend
    path("", home_view, name="home"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("my-bookings/", my_bookings_view, name="my-bookings"),

    # APIs
    path("api/v1/auth/", include("users.urls")),
    path("api/v1/cars/", include("cars.urls")),
    path("api/v1/bookings/", include("bookings.urls")),
]

# Media files (ONLY append AFTER urlpatterns is defined)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



