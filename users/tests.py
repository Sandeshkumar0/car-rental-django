from django.test import TestCase
from django.urls import reverse
from .models import User


class OTPAuthTests(TestCase):

    def test_register_and_verify(self):
        response = self.client.post(
            reverse("register"),
            {"email": "test@test.com", "password1": "StrongPass123", "password2": "StrongPass123"}
        )

        self.assertEqual(response.status_code, 302)
        user = User.objects.get(email="test@test.com")
        self.assertFalse(user.is_active)

        response = self.client.post(
            reverse("verify-otp"),
            {"otp": user.otp}
        )

        user.refresh_from_db()
        self.assertTrue(user.is_active)
