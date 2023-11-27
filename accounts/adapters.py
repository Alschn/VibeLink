from typing import Any

from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.forms import default_token_generator
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from allauth.account.utils import user_pk_to_url_str, user_username
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.utils.encoding import force_str

from core.shared.frontend import get_frontend_site, build_frontend_url

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

        frontend_site = get_frontend_site()
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
        frontend_site = get_frontend_site()
        activate_url = self.get_email_confirmation_url(request, emailconfirmation)
        ctx = {
            "user": emailconfirmation.email_address.user,
            "activate_url": activate_url,
            "current_site": frontend_site,
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

        frontend_path = self.password_reset_url_path.format(uid=uid, token=token)
        return build_frontend_url(frontend_path)

    def get_email_confirmation_url(
        self,
        request: Any,
        emailconfirmation: EmailConfirmationType
    ) -> str:
        """Constructs the email confirmation (activation) (frontend) url."""

        key = emailconfirmation.key
        frontend_path = self.email_confirmation_url_path.format(key=key)
        return build_frontend_url(frontend_path)

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

    def format_email_subject(self, subject: str) -> str:
        prefix = allauth_settings.EMAIL_SUBJECT_PREFIX
        if prefix is None:
            site = get_frontend_site()
            prefix = "[{name}] ".format(name=site.name)
        return prefix + force_str(subject)

    def render_mail(
        self,
        template_prefix: str,
        email: str,
        context: dict,
        headers: dict = None
    ) -> EmailMultiAlternatives | EmailMessage:
        return super().render_mail(template_prefix, email, context, headers)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    pass
