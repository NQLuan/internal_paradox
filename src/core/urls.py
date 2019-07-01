from django.contrib import admin
from django.conf.urls import include, url

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include(('api.router', 'api'), namespace='v1')),
]