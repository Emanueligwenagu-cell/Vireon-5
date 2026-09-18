from django.core.validators import MinValueValidator
from django.db import models


class PromoCode(models.Model):
    class DiscountType(models.TextChoices):
        PERCENT = "percent", "Percent off"
        FIXED = "fixed", "Fixed amount off"

    code = models.CharField(max_length=30, unique=True, db_index=True)
    discount_type = models.CharField(max_length=10, choices=DiscountType.choices, default=DiscountType.PERCENT)
    discount_value = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    max_percent_cap = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True,
        help_text="Optional cap on a percent discount, in currency.",
        validators=[MinValueValidator(0)],
    )
    min_order_value = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    max_redemptions = models.PositiveIntegerField(null=True, blank=True, help_text="Blank = unlimited")
    times_redeemed = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.code
