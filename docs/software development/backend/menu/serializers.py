from rest_framework import serializers

from .models import MenuItem


class MenuItemSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source="vendor.name", read_only=True)

    class Meta:
        model = MenuItem
        fields = [
            "id", "vendor", "vendor_name", "name", "description", "price",
            "prep_time_minutes", "category", "image", "is_available",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_vendor(self, vendor):
        request = self.context["request"]
        if request.user.role != "admin" and vendor.owner_id != request.user.id:
            raise serializers.ValidationError("You can only add items to your own vendor profile.")
        return vendor
