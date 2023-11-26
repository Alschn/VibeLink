from typing import Any

from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.forms import default_token_generator
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from allauth.account.utils import user_pk_to_url_str, user_username
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

EmailConfirmationType = EmailConfirmation | EmailConfirmationHMAC

User = get_user_model()


class AccountAdapter(DefaultAccountAdapter):
    # todo: make paths and templates more configurable, not hardcoded
    # frontend paths
    email_confirmation_url_path = '/auth/register/confirm/?key={key}'
    password_reset_url_path = '/auth/password/reset/confirm/?uid={uid}&token={token}'

    # todo: custom html templates
    # templates
    email_confirmation_signup_template = 'account/email/email_confirmation_signup'
    email_confirmation_template = 'account/email/email_confirmation'
    password_reset_template = 'account/email/password_reset_key'

    def send_password_reset_mail(
        self,
        request: Any,
        email: str,
        user: User,
        token_generator: Any = None
    ) -> None:
        """
        Sends an email with a link to password reset page.
        Password reset email logic is based on AllAuthPasswordResetForm.save().
        """

        token_generator = token_generator or default_token_generator
        temp_key = token_generator.make_token(user)

        # (optionally) save it to the password reset model
        # password_reset = PasswordReset(user=user, temp_key=temp_key)
        # password_reset.save()

        uid = user_pk_to_url_str(user)
        url = self.get_password_reset_url(request, uid, temp_key)

        # todo: frontend url
        frontend_site = get_current_site(request)
        context = {
            'current_site': frontend_site,
            'user': user,
            'password_reset_url': url,
            'request': request,
        }
        if (
            allauth_settings.AUTHENTICATION_METHOD
            != allauth_settings.AuthenticationMethod.EMAIL
        ):
            context['username'] = user_username(user)

        self.send_mail(self.password_reset_template, email, context)

    def send_confirmation_mail(
        self,
        request: Any,
        emailconfirmation: EmailConfirmationType,
        signup: bool
    ) -> None:
        # todo: frontend url
        current_site = get_current_site(request)
        activate_url = self.get_email_confirmation_url(request, emailconfirmation)
        ctx = {
            "user": emailconfirmation.email_address.user,
            "activate_url": activate_url,
            "current_site": current_site,
            "key": emailconfirmation.key,
        }
        if signup:
            email_template = self.email_confirmation_signup_template
        else:
            email_template = self.email_confirmation_template

        self.send_mail(email_template, emailconfirmation.email_address.email, ctx)

    def get_password_reset_url(
        self, request: Any, uid: str, token: str
    ) -> str:
        """Constructs the password reset (frontend) url."""

        # todo: build frontend url
        return self.password_reset_url_path.format(uid=uid, token=token)

    def get_email_confirmation_url(
        self,
        request: Any,
        emailconfirmation: EmailConfirmationType
    ) -> str:
        """Constructs the email confirmation (activation) (frontend) url."""

        # todo: build frontend url
        return self.email_confirmation_url_path.format(key=emailconfirmation.key)

    def get_email_confirmation_redirect_url(self, request: Any) -> None:
        """
        Returns None so that API response is not redirected after email confirmation.
        """
        return None

    def respond_email_verification_sent(self, request: Any, user: User) -> None:
        """
        Returns None so that API response is not overriden by the adapter
        after the email verification has been sent.
        """
        return None


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    pass
