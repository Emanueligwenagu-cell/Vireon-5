from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User

from .models import Vendor


class VendorCreationTests(APITestCase):
    def setUp(self):
        self.vendor_user = User.objects.create_user(
            email="vendor1@wsu.ac.za", password="StrongPassw0rd!", full_name="Vendor One", role=User.Role.VENDOR
        )
        self.student_user = User.objects.create_user(
            email="student1@wsu.ac.za", password="StrongPassw0rd!", full_name="Student One"
        )

    def test_student_cannot_create_vendor_profile(self):
        self.client.force_authenticate(self.student_user)
        response = self.client.post(reverse("vendor-list"), {"name": "Test Stall", "location": "Bldg 1"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_vendor_can_create_own_profile(self):
        self.client.force_authenticate(self.vendor_user)
        response = self.client.post(reverse("vendor-list"), {"name": "Test Stall", "location": "Bldg 1"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.get().owner, self.vendor_user)
