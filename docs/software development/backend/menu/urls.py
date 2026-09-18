from rest_framework.routers import DefaultRouter

from .views import MenuItemViewSet

router = DefaultRouter()
router.register("", MenuItemViewSet, basename="menuitem")

urlpatterns = router.urls
