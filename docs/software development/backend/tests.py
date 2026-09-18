from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class RegistrationTests(APITestCase):
    def test_register_creates_hashed_password(self):
        url = reverse("auth-register")
        data = {
            "email": "student1@wsu.ac.za",
            "full_name": "Test Student",
            "password": "StrongPassw0rd!",
            "password_confirm": "StrongPassw0rd!",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email="student1@wsu.ac.za")
        self.assertNotEqual(user.password, "StrongPassw0rd!")
        self.assertTrue(user.check_password("StrongPassw0rd!"))

    def test_cannot_self_register_as_admin(self):
        url = reverse("auth-register")
        data = {
            "email": "sneaky@wsu.ac.za",
            "full_name": "Sneaky",
            "role": "admin",
            "password": "StrongPassw0rd!",
            "password_confirm": "StrongPassw0rd!",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_mismatched_passwords_rejected(self):
        url = reverse("auth-register")
        data = {
            "email": "student2@wsu.ac.za",
            "full_name": "Test Student",
            "password": "StrongPassw0rd!",
            "password_confirm": "Different!",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="login@wsu.ac.za", password="StrongPassw0rd!", full_name="Login Test"
        )

    def test_login_returns_tokens(self):
        url = reverse("auth-login")
        response = self.client.post(url, {"email": "login@wsu.ac.za", "password": "StrongPassw0rd!"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_wrong_password_rejected(self):
        url = reverse("auth-login")
        response = self.client.post(url, {"email": "login@wsu.ac.za", "password": "wrong"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
