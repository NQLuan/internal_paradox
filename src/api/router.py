from django.conf.urls import url, include
from rest_framework import routers

from api.views import *

router = routers.SimpleRouter(trailing_slash=False)

# Define url in here
router.register(r'demo', DemoViewSet, base_name="demo")

urlpatterns = [
    url(r'^', include(router.urls))
]
