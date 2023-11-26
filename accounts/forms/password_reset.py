from typing import Any

from allauth.account.adapter import get_adapter
from dj_rest_auth.forms import AllAuthPasswordResetForm


class PasswordResetForm(AllAuthPasswordResetForm):
    # used in PasswordResetSerializer (dynamically imported from dj-rest-auth settings)

    def save(self, request: Any, **kwargs: Any) -> str:
        email = self.cleaned_data['email']

        adapter = get_adapter(request)
        assert (
            hasattr(adapter, 'send_password_reset_mail'),
            'send_password_reset_mail(request, email, user, token_generator=None) must be implemented in Adapter'
        )

        for user in self.users:
            adapter.send_password_reset_mail(request, email, user)

        return self.cleaned_data['email']
