from rest_framework import serializers

from .models import GameScore

MAX_POINTS_PER_PLAY = 50
SCORE_TO_POINTS_DIVISOR = 10


class GameScoreSerializer(serializers.ModelSerializer):
    player = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = GameScore
        fields = ["id", "player", "score", "points_awarded", "played_at"]
        read_only_fields = ["id", "player", "points_awarded", "played_at"]


class SubmitScoreSerializer(serializers.Serializer):
    # The score itself is just gameplay data; only the points it converts to
    # touch loyalty_points, and that conversion is computed server-side and
    # capped, so a client can't hand itself unlimited loyalty points.
    score = serializers.IntegerField(min_value=0, max_value=100000)
