from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """Users log in with email, not username."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        extra_fields.setdefault("role", User.Role.STUDENT)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            # Accounts created via Google OAuth have no usable password.
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", User.Role.ADMIN)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user. Students order food, vendors sell it, admins manage the
    platform. A user can sign up with a password OR via Google OAuth
    (in which case has_usable_password() is False and google_sub is set).
    """

    class Role(models.TextChoices):
        STUDENT = "student", "Student"
        VENDOR = "vendor", "Vendor"
        ADMIN = "admin", "Admin"

    email = models.EmailField(unique=True, db_index=True)
    full_name = models.CharField(max_length=150)
    student_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)

    # Google OAuth - the stable subject id Google gives us for this account
    google_sub = models.CharField(max_length=255, blank=True, null=True, unique=True)

    loyalty_points = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        indexes = [models.Index(fields=["role"])]

    def __str__(self):
        return f"{self.full_name} <{self.email}>"

    @property
    def is_vendor(self):
        return self.role == self.Role.VENDOR

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT
