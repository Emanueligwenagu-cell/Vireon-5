from rest_framework.routers import DefaultRouter

from .views import PromoCodeViewSet

router = DefaultRouter()
router.register("", PromoCodeViewSet, basename="promocode")

urlpatterns = router.urls
