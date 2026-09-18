from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from vendors.models import Vendor

from .models import Category, MenuItem


class MenuItemPermissionTests(APITestCase):
    def setUp(self):
        self.vendor_user = User.objects.create_user(
            email="vendor@wsu.ac.za", password="StrongPassw0rd!", full_name="V", role=User.Role.VENDOR
        )
        self.other_vendor_user = User.objects.create_user(
            email="vendor2@wsu.ac.za", password="StrongPassw0rd!", full_name="V2", role=User.Role.VENDOR
        )
        self.vendor = Vendor.objects.create(owner=self.vendor_user, name="Stall", location="B1", is_approved=True)

    def test_other_vendor_cannot_add_item_to_someone_elses_stall(self):
        self.client.force_authenticate(self.other_vendor_user)
        response = self.client.post(reverse("menuitem-list"), {
            "vendor": self.vendor.id, "name": "Pie", "price": "20.00", "category": Category.SNACKS,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_owning_vendor_can_add_item(self):
        self.client.force_authenticate(self.vendor_user)
        response = self.client.post(reverse("menuitem-list"), {
            "vendor": self.vendor.id, "name": "Pie", "price": "20.00", "category": Category.SNACKS,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MenuItem.objects.count(), 1)
