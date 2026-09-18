from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from menu.models import MenuItem
from vendors.models import Vendor


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        PREPARING = "preparing", "Preparing"
        READY = "ready", "Ready for pickup"
        OUT_FOR_DELIVERY = "out_for_delivery", "Out for delivery"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    class FulfillmentType(models.TextChoices):
        PICKUP = "pickup", "Pickup"
        DELIVERY = "delivery", "Delivery"

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders")
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, related_name="orders")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    fulfillment_type = models.CharField(max_length=10, choices=FulfillmentType.choices, default=FulfillmentType.PICKUP)
    delivery_location = models.CharField(max_length=200, blank=True)

    # Snapshotted server-side at creation time - never trust a client-supplied total.
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    promo_code = models.ForeignKey(
        "promos.PromoCode", on_delete=models.SET_NULL, null=True, blank=True, related_name="orders"
    )

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["student", "status"]), models.Index(fields=["vendor", "status"])]
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} - {self.student.email} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT, related_name="order_items")
    # Snapshot the name/price at order time so later menu edits don't rewrite history.
    item_name = models.CharField(max_length=150)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    @property
    def line_total(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.item_name}"
