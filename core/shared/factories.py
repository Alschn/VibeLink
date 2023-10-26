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


class FriendFactory(DjangoModelFactory):
    class Meta:
        model = 'friendship.Friend'

    to_user = factory.SubFactory(UserFactory)
    from_user = factory.SubFactory(UserFactory)


class FriendshipRequestFactory(DjangoModelFactory):
    class Meta:
        model = 'friendship.FriendshipRequest'

    to_user = factory.SubFactory(UserFactory)
    from_user = factory.SubFactory(UserFactory)
