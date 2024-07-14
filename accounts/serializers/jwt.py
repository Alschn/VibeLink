import typing

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.tokens import get_token_for_user

if typing.TYPE_CHECKING:
    from rest_framework_simplejwt.serializers import AuthUser
    from rest_framework_simplejwt.tokens import Token


class JWTClaimsSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user: 'AuthUser') -> 'Token':
        return get_token_for_user(user)
