from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Safe, read-mostly representation of the logged-in user."""

    class Meta:
        model = User
        fields = [
            "id", "email", "full_name", "student_number", "phone_number",
            "role", "loyalty_points", "date_joined",
        ]
        read_only_fields = ["id", "role", "loyalty_points", "date_joined"]


class RegisterSerializer(serializers.ModelSerializer):
    """
    Self-service account creation. Passwords are validated against Django's
    validators (min length, not too common, not all-numeric, not too similar
    to the user's own info) and are always stored hashed - set_password()
    hashes on save(), the raw password is never persisted.
    """

    password = serializers.CharField(write_only=True, min_length=10)
    password_confirm = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.Role.choices, required=False, write_only=True)

    class Meta:
        model = User
        fields = [
            "id", "email", "full_name", "student_number", "phone_number",
            "role", "password", "password_confirm",
        ]

    def validate_role(self, value):
        if value != User.Role.STUDENT:
            raise serializers.ValidationError("Only student accounts can self-register.")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("password_confirm"):
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        # Run Django's full password-strength validation.
        validate_password(attrs["password"])
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)


class GoogleLoginSerializer(serializers.Serializer):
    """Frontend sends the Google ID token it received from Google Identity Services."""

    id_token = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=10)

    def validate_new_password(self, value):
        validate_password(value, user=self.context["request"].user)
        return value


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Adds a couple of non-sensitive claims so the frontend doesn't need an extra round trip."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        token["full_name"] = user.full_name
        return token
