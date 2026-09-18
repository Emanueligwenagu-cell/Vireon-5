from django.conf import settings
from django.db import models


class Vendor(models.Model):
    """A cafeteria / food stall on campus, owned by one 'vendor' role user."""

    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="vendor_profile"
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=150, help_text="e.g. 'Building 6, Ground Floor'")
    logo = models.ImageField(upload_to="vendor_logos/", blank=True, null=True)

    is_approved = models.BooleanField(default=False, help_text="Admin must approve before vendor can sell.")
    is_open = models.BooleanField(default=True)

    opens_at = models.TimeField(default="08:00")
    closes_at = models.TimeField(default="17:00")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["is_approved", "is_open"])]

    def __str__(self):
        return self.name

    @property
    def can_sell(self):
        return self.is_approved and self.is_open
