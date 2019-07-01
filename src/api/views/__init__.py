from rest_framework import viewsets


class BaseViewSet(viewsets.ViewSet):
    activity_log = True


from api.views.demoView import DemoViewSet
