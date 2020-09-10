from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from api_company.views import CreateCompanyView

urlpatterns = [
    url(r'^api/v1/', include(('api.router', 'api'), namespace='v1')),
    url(r'^api/v1/user/', include('api_user.urls')),
    url(r'^api/v1/workday/', include('api_workday.urls')),
    url(r'^api/v1/company', CreateCompanyView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
