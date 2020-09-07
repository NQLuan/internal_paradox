from api_workday.models import RequestOff
from api_workday.test.factories import TypeOffFactory
import factory
from faker import Factory

faker = Factory.create()


class RequestOffFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RequestOff

    reason = faker.word()
    type_off = factory.SubFactory(TypeOffFactory)
