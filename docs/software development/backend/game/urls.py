from django.urls import path

from .views import LeaderboardView, MyScoresView, SubmitScoreView

urlpatterns = [
    path("submit/", SubmitScoreView.as_view(), name="game-submit"),
    path("leaderboard/", LeaderboardView.as_view(), name="game-leaderboard"),
    path("my-scores/", MyScoresView.as_view(), name="game-my-scores"),
]
