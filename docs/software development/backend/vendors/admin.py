from django.contrib import admin

from .models import Vendor


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "location", "is_approved", "is_open"]
    list_filter = ["is_approved", "is_open"]
    search_fields = ["name", "owner__email"]
