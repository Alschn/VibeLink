import typing

from rest_framework_simplejwt.tokens import RefreshToken

if typing.TYPE_CHECKING:
    from rest_framework_simplejwt.serializers import AuthUser
    from rest_framework_simplejwt.tokens import Token


def get_token_for_user(user: 'AuthUser') -> 'Token':
    token = RefreshToken.for_user(user)
    token['email'] = user.email
    token['username'] = user.username
    return token


def get_tokens_for_user(user: 'AuthUser') -> tuple[str, str]:
    """
    Returns access and refresh token pair.
    access, refresh = get_tokens_for_user(user)
    """
    token = get_token_for_user(user)
    access = str(token.access_token)  # type: ignore
    refresh = str(token)
    return access, refresh
