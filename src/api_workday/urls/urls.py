from django.urls import path

from api_workday.views.date_off import DateOffView
from api_workday.views.request_off import RequestOffDetail, GetMyRequest
from api_workday.views.type_off import TypeOffView, CreateTypeOffView, EditandDeleteTypeOffView
from api_workday.views.action_request import ActionRequest, GetRequestDetail
from api_workday.views.send_mail import SendMailToUser

urlpatterns = [
    path('type', TypeOffView.as_view(), name='type'),
    path('type/create', CreateTypeOffView.as_view(), name='create-type'),
    path('type/edit/<uuid:pk>', EditandDeleteTypeOffView.as_view(), name='modify-type'),

    path('request/<uuid:pk>', RequestOffDetail.as_view(), name='request-detail'),
    path('request/create', RequestOffDetail.as_view(), name='create-request'),

    path('date', DateOffView.as_view()),

    path('action', ActionRequest.as_view(), name='action'),
    path('request/management', GetRequestDetail.as_view(), name='management-request'),
    path('request/user', GetMyRequest.as_view(), name='request-user'),
    path('request/sendmail', SendMailToUser.as_view()),
]
