from django.urls import path

from .views import (
    JWTLoginAPIView,
    JWTRefreshAPIView,
    JWTVerifyAPIView,
    LogoutAPIView,
    PasswordChangeAPIView,
    PasswordResetAPIView,
    PasswordResetConfirmAPIView,
    RegisterAPIView,
    RegisterEmailVerifyAPIView,
    RegisterEmailResendAPIView
)

urlpatterns = [
    path('auth/token/', JWTLoginAPIView.as_view(), name='token'),
    path('auth/token/refresh/', JWTRefreshAPIView.as_view(), name='token_refresh'),
    path('auth/token/verify/', JWTVerifyAPIView.as_view(), name='token_verify'),

    path('auth/logout/', LogoutAPIView.as_view(), name='logout'),

    path('auth/register/', RegisterAPIView.as_view(), name='register'),
    path('auth/register/verify-email/', RegisterEmailVerifyAPIView.as_view(), name='register_verify_email'),
    path('auth/register/resend-email/', RegisterEmailResendAPIView.as_view(), name='register_resend_email'),

    path('auth/password/change/', PasswordChangeAPIView.as_view(), name='password_change'),

    path('auth/password/reset/', PasswordResetAPIView.as_view(), name='password_reset'),
    path('auth/password/reset/confirm/', PasswordResetConfirmAPIView.as_view(), name='password_reset_confirm'),
]
