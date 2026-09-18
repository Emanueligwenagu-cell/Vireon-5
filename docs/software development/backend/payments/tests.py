from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from menu.models import Category, MenuItem
from orders.models import Order
from vendors.models import Vendor


class PaymentAmountTests(APITestCase):
    def setUp(self):
        self.vendor_user = User.objects.create_user(
            email="vendor@wsu.ac.za", password="StrongPassw0rd!", full_name="V", role=User.Role.VENDOR
        )
        self.vendor = Vendor.objects.create(owner=self.vendor_user, name="Stall", location="B1", is_approved=True)
        self.item = MenuItem.objects.create(vendor=self.vendor, name="Wrap", price="45.00", category=Category.SNACKS)
        self.student = User.objects.create_user(email="student@wsu.ac.za", password="StrongPassw0rd!", full_name="S")
        self.client.force_authenticate(self.student)
        self.order = self.client.post(reverse("order-list"), {
            "items": [{"menu_item": self.item.id, "quantity": 1}], "fulfillment_type": "pickup",
        }, format="json").data

    def test_payment_amount_ignores_client_supplied_value(self):
        response = self.client.post(reverse("payment-list"), {
            "order": self.order["id"], "method": "cash_on_pickup", "amount": "0.01",
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["amount"], "45.00")
