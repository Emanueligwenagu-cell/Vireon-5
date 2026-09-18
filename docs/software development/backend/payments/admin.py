from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "student", "method", "status", "amount", "created_at"]
    list_filter = ["method", "status"]
    readonly_fields = ["amount", "provider_reference", "created_at", "updated_at"]
