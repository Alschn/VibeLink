import factory
from factory.django import DjangoModelFactory

from links.models import Link

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


class LinkFactory(DjangoModelFactory):
    class Meta:
        model = 'links.Link'

    title = factory.Faker('sentence')
    description = factory.Faker('paragraph')
    url = factory.Faker('url')
    source_type = Link.SourceType.UNKNOWN
    user = factory.SubFactory(UserFactory)
    track = None
    # todo: track, author factories


class LinkRequestFactory(DjangoModelFactory):
    class Meta:
        model = 'links.LinkRequest'

    user = factory.SubFactory(UserFactory)

    has_link = False

    class Params:
        has_link = factory.Trait(
            link=factory.SubFactory(
                'core.shared.factories.LinkFactory',
                user=factory.SelfAttribute('..user')
            ),
            fulfilled_at=factory.LazyAttribute(
                lambda o: o.link.created_at
            )
        )
