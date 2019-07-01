from api.models import Demo
from api.serializers import ServiceSerializer
from api.services import DemoService


class DemoSerializer(ServiceSerializer):

    def validate(self, data):
        pass

    def create(self, validated_data):
        return DemoService.save(validated_data)

    def update(self, instance, validated_data):
        return DemoService.save(validated_data, instance)

    class Meta:
        model = Demo
