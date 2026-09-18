from django.conf import settings
from django.db import models

from orders.models import Order


class Payment(models.Model):
    class Method(models.TextChoices):
        CARD = "card", "Card"
        CAMPUS_WALLET = "campus_wallet", "Campus Wallet"
        CASH_ON_PICKUP = "cash_on_pickup", "Cash on pickup"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCEEDED = "succeeded", "Succeeded"
        FAILED = "failed", "Failed"
        REFUNDED = "refunded", "Refunded"

    order = models.OneToOneField(Order, on_delete=models.PROTECT, related_name="payment")
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="payments")
    method = models.CharField(max_length=20, choices=Method.choices)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)

    # Amount is always copied from order.total server-side - never accepted from the client.
    amount = models.DecimalField(max_digits=9, decimal_places=2)

    # Opaque reference from whatever gateway processed this (or blank for cash/pending).
    provider_reference = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for order #{self.order_id} - {self.status}"
