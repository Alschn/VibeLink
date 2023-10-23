import factory
from factory.django import DjangoModelFactory

DEFAULT_USER_FACTORY_PASSWORD = 'test'


class UserFactory(DjangoModelFactory):
    class Meta:
        model = 'accounts.User'

    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall(
        'set_password',
        DEFAULT_USER_FACTORY_PASSWORD
    )
