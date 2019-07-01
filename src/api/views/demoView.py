from api.serializers import DemoSerializer
from api.views import BaseViewSet


class DemoViewSet(BaseViewSet):

    view_set = 'demo'
    serializer_class = DemoSerializer

    def list(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
