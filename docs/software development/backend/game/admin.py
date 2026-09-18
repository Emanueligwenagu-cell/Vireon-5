from django.contrib import admin

from .models import GameScore


@admin.register(GameScore)
class GameScoreAdmin(admin.ModelAdmin):
    list_display = ["user", "score", "points_awarded", "played_at"]
    search_fields = ["user__email"]
