from rest_framework import serializers
from api_workday.models.request_off import RequestOff
from api_workday.serializers.date_off import DateOffSerizlizer
from api_workday.models.date_off import DateOff
# from api_workday.serializers.action_request import RequestDetailSerializer


from api_workday.models.request_detail import RequestDetail

class RequestOffSerializer(serializers.ModelSerializer):
    queryset = RequestDetail.objects.filter().exclude(comment=None)
    date_off = DateOffSerizlizer(many=True, read_only=True)
    type_off = serializers.SerializerMethodField("get_type")
    profile = serializers.SerializerMethodField("get_profile")

    request_detail = serializers.SlugRelatedField(many=True, slug_field='comment', read_only=True)
    def get_type(self, obj):
        return {'id': obj.type_off.id,
                'label': obj.type_off.label,
                'title': obj.type_off.title,
                'descriptions': obj.type_off.descriptions,
                'add_sub_day_off': obj.type_off.add_sub_day_off
                }

    def get_profile(self, obj):
        return {'id': obj.profile.id,
                'name': obj.profile.name
                }

    class Meta:
        model = RequestOff
        fields = '__all__'
        read_only_fields = ['type_off', 'profile']
