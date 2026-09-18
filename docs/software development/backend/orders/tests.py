from django.urls import reverse
from decimal import Decimal
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from menu.models import Category, MenuItem
from vendors.models import Vendor

from .models import Order


class OrderCreationTests(APITestCase):
    def setUp(self):
        self.vendor_user = User.objects.create_user(
            email="vendor@wsu.ac.za", password="StrongPassw0rd!", full_name="V", role=User.Role.VENDOR
        )
        self.vendor = Vendor.objects.create(owner=self.vendor_user, name="Stall", location="B1", is_approved=True)
        self.item = MenuItem.objects.create(vendor=self.vendor, name="Wrap", price="45.00", category=Category.SNACKS)
        self.student = User.objects.create_user(
            email="student@wsu.ac.za", password="StrongPassw0rd!", full_name="S"
        )

    def test_total_is_computed_server_side_not_trusted_from_client(self):
        """A client cannot lower the price by sending a fake unit_price/total in the payload."""
        self.client.force_authenticate(self.student)
        payload = {
            "items": [{"menu_item": self.item.id, "quantity": 2, "unit_price": "1.00", "total": "1.00"}],
            "fulfillment_type": "pickup",
        }
        response = self.client.post(reverse("order-list"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get(pk=response.data["id"])
        self.assertEqual(order.total, Decimal("90.00"))

    def test_vendor_cannot_skip_order_status_stages(self):
        self.client.force_authenticate(self.student)
        create = self.client.post(reverse("order-list"), {
            "items": [{"menu_item": self.item.id, "quantity": 1}], "fulfillment_type": "pickup",
        }, format="json")
        order_id = create.data["id"]

        self.client.force_authenticate(self.vendor_user)
        response = self.client.post(reverse("order-set-status", args=[order_id]), {"status": "completed"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_vendor_cannot_create_orders(self):
        self.client.force_authenticate(self.vendor_user)
        response = self.client.post(reverse("order-list"), {
            "items": [{"menu_item": self.item.id, "quantity": 1}], "fulfillment_type": "pickup",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
