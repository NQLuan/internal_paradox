from api_workday.models import TypeOff
import factory
from faker import Factory

faker = Factory.create()

class TypeOffFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TypeOff
        django_get_or_create = ('title', 'label', 'descriptions')

    title = faker.word()
    label = faker.word()
    descriptions = faker.text()
