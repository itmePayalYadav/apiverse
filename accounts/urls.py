from django.urls import path
from django.conf import settings
from .views import (
    RegisterView,
    VerifyEmailView,
    LoginView,
    LogoutView,
    RefreshTokenView,
    ForgotPasswordView,
    ResetPasswordView,
    ChangePasswordView,
    ResendEmailVerificationView,
    CurrentUserView,
    UpdateAvatarView,
    GoogleLoginView,
    GoogleLoginCallbackView,
    GitHubLoginView,
    GitHubLoginCallbackView,
    ChangeRoleView,
)
from django.conf.urls.static import static

# ----------------------------
# Authentication URLs
# ----------------------------
urlpatterns = [
    # Registration & Email Verification
    path("register/", RegisterView.as_view(), name="register"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify_email"),
    path("resend-email-verification/", ResendEmailVerificationView.as_view(), name="resend_email_verification"),

    # Authentication
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("refresh-token/", RefreshTokenView.as_view(), name="refresh_token"),

    # Password Management
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot_password"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset_password"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),

    # User Management
    path("current/", CurrentUserView.as_view(), name="current_user"),
    path("update-avatar/", UpdateAvatarView.as_view(), name="update_avatar"),
    path("change-role/", ChangeRoleView.as_view(), name="change_role"),

    # Google OAuth
    path("google/", GoogleLoginView.as_view(), name="google_login"),
    path("google/callback/", GoogleLoginCallbackView.as_view(), name="google_callback"),

    # GitHub OAuth
    path("github/", GitHubLoginView.as_view(), name="github_login"),
    path("github/callback/", GitHubLoginCallbackView.as_view(), name="github_callback"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    