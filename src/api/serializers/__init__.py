from rest_framework import serializers


class ServiceSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        raise NotImplementedError('create must be implemented')

    def update(self, instance, validated_data):
        raise NotImplementedError('update must be implemented')

    def destroy(self):
        raise NotImplementedError('destroy must be implemented')


from api.serializers.demo import DemoSerializer
