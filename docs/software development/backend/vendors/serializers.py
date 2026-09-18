from rest_framework import serializers

from .models import Vendor


class VendorSerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(source="owner.email", read_only=True)

    class Meta:
        model = Vendor
        fields = [
            "id", "owner", "owner_email", "name", "description", "location", "logo",
            "is_approved", "is_open", "opens_at", "closes_at", "created_at",
        ]
        read_only_fields = ["id", "owner", "is_approved", "created_at"]
