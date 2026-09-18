from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["menu_item", "item_name", "unit_price", "quantity"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "student", "vendor", "status", "total", "created_at"]
    list_filter = ["status", "fulfillment_type"]
    search_fields = ["student__email", "vendor__name"]
    inlines = [OrderItemInline]
    readonly_fields = ["subtotal", "discount_amount", "total", "created_at", "updated_at"]
