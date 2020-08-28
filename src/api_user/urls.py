from rest_framework import routers
from .views import ProfileViewSet, UserViewSet, PhotoViewSet

router = routers.DefaultRouter()
router.register(r'photo', PhotoViewSet, basename="photo")
router.register(r'profile', ProfileViewSet, basename="profile")
router.register(r'', UserViewSet, basename="user")

urlpatterns = router.urls
