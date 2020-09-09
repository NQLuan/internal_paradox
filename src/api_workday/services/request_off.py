from api_base.services import BaseService

class RequestOffServices(BaseService):

    @classmethod
    def check_overlap_date(cls, data, dateOff, profileId, requestOff):
        list_id_request = requestOff.objects.filter(profile_id=profileId).values_list('id', flat=True)
        if len(list_id_request) == 0:
            return False
        for id_request in list_id_request:
            for date in data["date"]:
                date_off = dateOff.objects.filter(date=date['date']).filter(request_off_id=id_request)
                if len(date_off) == 1:
                    return True
