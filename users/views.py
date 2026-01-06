# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import login

# from .forms import RegisterForm

# from .serializers import UserRegisterSerializer, UserLoginSerializer


# class RegisterAPIView(APIView):
#     def post(self, request):
#         serializer = UserRegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LoginAPIView(APIView):
#     def post(self, request):
#         serializer = UserLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data["user"]
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 "refresh": str(refresh),
#                 "access": str(refresh.access_token),
#             }, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#         def register_view(request):
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)  # auto-login after signup
#             return redirect("home")
#     else:
#         form = RegisterForm()

#     return render(request, "register.html", {"form": form})

# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import login

# from .forms import RegisterForm

# from .serializers import UserRegisterSerializer, UserLoginSerializer


# class RegisterAPIView(APIView):
#     def post(self, request):
#         serializer = UserRegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LoginAPIView(APIView):
#     def post(self, request):
#         serializer = UserLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data["user"]
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 "refresh": str(refresh),
#                 "access": str(refresh.access_token),
#             }, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#         def register_view(request):
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)  # auto-login after signup
#             return redirect("home")
#     else:
#         form = RegisterForm()

#     return render(request, "register.html", {"form": form})

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.core.mail import send_mail

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .forms import RegisterForm
from .models import User
from .utils import generate_otp, otp_expiry_time
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    OTPVerifySerializer,
)

# ==================================================
# UI (HTML) REGISTRATION WITH OTP
# ==================================================

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False

            # OTP rate limiting
            if user.otp_attempts >= 3:
                return render(
                    request,
                    "register.html",
                    {
                        "form": form,
                        "error": "Too many OTP requests. Try again later.",
                    },
                )

            user.otp_attempts += 1
            otp = generate_otp()
            user.otp = otp
            user.otp_expiry = otp_expiry_time()
            user.save()

            send_mail(
                subject="Your OTP for Car Rental",
                message=f"Your OTP is {otp}. It expires in 5 minutes.",
                from_email=None,
                recipient_list=[user.email],
            )

            request.session["verify_email"] = user.email
            return redirect("verify-otp")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def verify_otp_view(request):
    email = request.session.get("verify_email")
    if not email:
        return redirect("register")

    user = User.objects.filter(email=email).first()
    error = None

    if request.method == "POST":
        otp = request.POST.get("otp")

        if user and user.otp_is_valid(otp):
            user.is_active = True
            user.otp = None
            user.otp_expiry = None
            user.otp_attempts = 0
            user.save()

            send_mail(
                subject="Welcome to Car Rental 🎉",
                message="Your email has been successfully verified.",
                from_email=None,
                recipient_list=[user.email],
            )

            login(request, user)
            del request.session["verify_email"]
            return redirect("home")

        error = "Invalid or expired OTP"

    return render(request, "verify_otp.html", {"error": error})


def resend_otp_view(request):
    email = request.session.get("verify_email")
    if not email:
        return redirect("register")

    user = User.objects.filter(email=email).first()
    if not user:
        return redirect("register")

    if user.otp_attempts >= 3:
        return render(
            request,
            "verify_otp.html",
            {"error": "Too many OTP requests. Try again later."},
        )

    user.otp_attempts += 1
    otp = generate_otp()
    user.otp = otp
    user.otp_expiry = otp_expiry_time()
    user.save()

    send_mail(
        subject="Your new OTP for Car Rental",
        message=f"Your new OTP is {otp}. It expires in 5 minutes.",
        from_email=None,
        recipient_list=[user.email],
    )

    return redirect("verify-otp")


# ==================================================
# API (JWT-BASED OTP VERIFICATION)
# ==================================================

class VerifyOTPAPIView(APIView):
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            otp = serializer.validated_data["otp"]

            user = User.objects.filter(email=email).first()
            if user and user.otp_is_valid(otp):
                user.is_active = True
                user.otp = None
                user.otp_expiry = None
                user.otp_attempts = 0
                user.save()

                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"error": "Invalid or expired OTP"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==================================================
# API (JWT-BASED REGISTER & LOGIN)
# ==================================================

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
