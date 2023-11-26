from dj_rest_auth.serializers import PasswordResetSerializer as BasePasswordResetSerializer

from accounts.forms.password_reset import PasswordResetForm


class PasswordResetSerializer(BasePasswordResetSerializer):

    @property
    def password_reset_form_class(self):
        return PasswordResetForm
