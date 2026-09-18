from django.conf import settings
from django.contrib.auth import get_user_model
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    ChangePasswordSerializer,
    EmailTokenObtainPairSerializer,
    GoogleLoginSerializer,
    RegisterSerializer,
    UserSerializer,
)

User = get_user_model()


def _tokens_for(user):
    refresh = RefreshToken.for_user(user)
    refresh["role"] = user.role
    refresh["full_name"] = user.full_name
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


class RegisterView(generics.CreateAPIView):
    """POST /api/auth/register/ - create a normal (email+password) account."""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"user": UserSerializer(user).data, "tokens": _tokens_for(user)},
            status=status.HTTP_201_CREATED,
        )


class EmailLoginView(TokenObtainPairView):
    """POST /api/auth/login/ - email + password login."""

    serializer_class = EmailTokenObtainPairSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"


class GoogleLoginView(APIView):
    """
    POST /api/auth/google/ {"id_token": "..."}

    Verifies the ID token directly with Google's servers (never trusts the
    client's claims about who they are), then finds or creates the matching
    local account and returns our own JWTs for it.
    """

    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"

    def post(self, request):
        serializer = GoogleLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            payload = google_id_token.verify_oauth2_token(
                serializer.validated_data["id_token"],
                google_requests.Request(),
                settings.GOOGLE_OAUTH_CLIENT_ID,
            )
        except ValueError:
            return Response({"detail": "Invalid Google token."}, status=status.HTTP_401_UNAUTHORIZED)

        if not payload.get("email_verified", False):
            return Response({"detail": "Google email is not verified."}, status=status.HTTP_401_UNAUTHORIZED)

        google_sub = payload["sub"]
        email = payload["email"]

        user = User.objects.filter(google_sub=google_sub).first() or User.objects.filter(email=email).first()
        created = False
        if user is None:
            user = User.objects.create_user(
                email=email,
                full_name=payload.get("name", email.split("@")[0]),
                role=User.Role.STUDENT,
                google_sub=google_sub,
            )
            created = True
        elif not user.google_sub:
            user.google_sub = google_sub
            user.save(update_fields=["google_sub"])

        return Response(
            {"user": UserSerializer(user).data, "tokens": _tokens_for(user), "created": created},
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    """POST /api/auth/logout/ {"refresh": "..."} - blacklists the refresh token."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            token = RefreshToken(request.data.get("refresh", ""))
            token.blacklist()
        except TokenError:
            return Response({"detail": "Invalid or already-expired token."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_205_RESET_CONTENT)


class MeView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/auth/me/ - the logged-in user's own profile."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data["old_password"]):
            return Response({"old_password": "Incorrect password."}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password"])
        return Response({"detail": "Password updated."})
