from django.urls import path
from .views import (
    register_view,
    verify_otp_view,
    resend_otp_view,
    RegisterAPIView,
    LoginAPIView,
    VerifyOTPAPIView,
)

urlpatterns = [
    # UI
    path("register/", register_view, name="register"),
    path("verify-otp/", verify_otp_view, name="verify-otp"),
    path("resend-otp/", resend_otp_view, name="resend-otp"),

    # API
    path("api/register/", RegisterAPIView.as_view(), name="api-register"),
    path("api/login/", LoginAPIView.as_view(), name="api-login"),
    path("api/verify-otp/", VerifyOTPAPIView.as_view(), name="api-verify-otp"),
]
