from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from api_admin.views import AdminViewSet
from api_base.views import ActionViewSet, LoginViewSet
from api_team.views import TeamViewSet
from api_user.views import ProfileViewSet, UserViewSet, PhotoViewSet
from api_workday.views import DateViewSet, LunchViewSet
from api_workday.views.propose_leave import ProposeLeaveViewSet

router = DefaultRouter()

# Define url in here
router.register(r'actions', ActionViewSet, basename="actions")
router.register(r'admin', AdminViewSet, basename="admin")
router.register(r'date', DateViewSet, basename="date")
router.register(r'login', LoginViewSet, basename="login")
router.register(r'lunch', LunchViewSet, basename="lunch")
router.register(r'photo', PhotoViewSet, basename="photo")
router.register(r'profile', ProfileViewSet, basename="profile")
router.register(r'leave', ProposeLeaveViewSet, basename="leave")
router.register(r'team', TeamViewSet, basename="team")
router.register(r'user', UserViewSet, basename="user")

urlpatterns = [
    url(r'^', include(router.urls))
]
