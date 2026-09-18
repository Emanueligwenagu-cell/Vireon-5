from django.conf import settings
from django.db import models


class GameScore(models.Model):
    """One row per play session of the loyalty mini-game on the 'Play' page."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="game_scores")
    score = models.PositiveIntegerField()
    points_awarded = models.PositiveIntegerField(default=0)
    played_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["user", "-score"])]
        ordering = ["-score"]

    def __str__(self):
        return f"{self.user.email}: {self.score}"
