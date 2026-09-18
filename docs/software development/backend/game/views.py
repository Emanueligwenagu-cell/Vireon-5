from django.db import transaction
from django.db.models import F
from rest_framework import permissions, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import GameScore
from .serializers import (
    MAX_POINTS_PER_PLAY,
    SCORE_TO_POINTS_DIVISOR,
    GameScoreSerializer,
    SubmitScoreSerializer,
)


class SubmitScoreView(APIView):
    """POST /api/game/submit/ {"score": 230} - records a play and awards capped loyalty points."""

    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = SubmitScoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        score = serializer.validated_data["score"]
        points = min(score // SCORE_TO_POINTS_DIVISOR, MAX_POINTS_PER_PLAY)

        game_score = GameScore.objects.create(user=request.user, score=score, points_awarded=points)
        request.user.__class__.objects.filter(pk=request.user.pk).update(loyalty_points=F("loyalty_points") + points)

        return Response(GameScoreSerializer(game_score).data, status=status.HTTP_201_CREATED)


class LeaderboardView(ListAPIView):
    """GET /api/game/leaderboard/ - top 10 scores of all time."""

    serializer_class = GameScoreSerializer
    permission_classes = [permissions.AllowAny]
    queryset = GameScore.objects.select_related("user").order_by("-score")[:10]


class MyScoresView(ListAPIView):
    serializer_class = GameScoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GameScore.objects.filter(user=self.request.user).order_by("-played_at")
