from rest_framework import serializers
from api_workday.models.date_off import DateOff

class DateOffSerizlizer(serializers.ModelSerializer):

    class Meta:
        model = DateOff
        fields = ['date', 'type', 'lunch', 'request_off']

