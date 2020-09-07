from api_base.services import BaseService

class RequestOffServices(BaseService):

    @classmethod
    def check_date(cls, data, obj):
        for date in data["date"]:
            date_off = obj.objects.filter(date=date["date"]).first()
            if date_off is not None:
                return date_off

    @classmethod
    def get_date_off_by_request_id(cls, pk, obj, serializer_name):
        data = obj.objects.filter(request_off_id=pk)
        date_off = []
        for date in data:
            serializer = serializer_name(date)
            if serializer is not None:
                date_off.append(serializer.data)
        return date_off
