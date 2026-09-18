from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from vendors.models import Vendor


class Category(models.TextChoices):
    TRADITIONAL = "traditional", "Traditional"
    FAST_FOOD = "fast-food", "Fast Food"
    HEALTHY = "healthy", "Healthy"
    SNACKS = "snacks", "Snacks"
    DRINKS = "drinks", "Drinks"
    PIZZA = "pizza", "Pizza"


class MenuItem(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="menu_items")
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    prep_time_minutes = models.PositiveSmallIntegerField(default=15)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.TRADITIONAL)
    image = models.ImageField(upload_to="menu_items/", blank=True, null=True)
    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["vendor", "category", "is_available"])]
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.vendor.name})"
