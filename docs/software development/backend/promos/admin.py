from django.contrib import admin

from .models import PromoCode


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ["code", "discount_type", "discount_value", "is_active", "valid_from", "valid_until", "times_redeemed"]
    list_filter = ["discount_type", "is_active"]
    search_fields = ["code"]
