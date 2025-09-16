from pathlib import Path
from decouple import config
import dj_database_url
import os

# ----------------------------
# Base Directory
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------
# Security & Debug
# ----------------------------
SECRET_KEY = config(
    "SECRET_KEY",
    default="%msg!8p+m5(%l$ljg6n7)b7opv&-1w%a@ao)_vb-s%tvcl6lu=",
    cast=str
)
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="").split(",")

# ----------------------------
# Installed Applications
# ----------------------------
INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party apps
    "rest_framework",
    "drf_spectacular",

    # Local apps
    "accounts",
    "todos",
    "socials",
    "chats",
    "ecommerce"
]

# ----------------------------
# User Accounts
# ----------------------------
AUTH_USER_MODEL = "accounts.User"

# ----------------------------
# Middleware
# ----------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ----------------------------
# REST FRAMEWORK & SPECTACULAR
# ----------------------------
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "accounts.authentication.JWTAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,

    # API Docs
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "APIVerse",
    "DESCRIPTION": "API documentation for your social media backend",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SECURITY": [{"JWTAuth": []}],
}

# ----------------------------
# URL & WSGI Configuration
# ----------------------------
ROOT_URLCONF = "apiverse.urls"
WSGI_APPLICATION = "apiverse.wsgi.application"

# ----------------------------
# Templates
# ----------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ----------------------------
# EMAIL SETTINGS (SendGrid)
# ----------------------------
EMAIL_BACKEND = config("EMAIL_BACKEND", default="core.emails.SendGridBackend")
SENDGRID_API_KEY = config("SENDGRID_API_KEY")
EMAIL_FROM = config("EMAIL_FROM")

# ----------------------------
# FRONTEND URL
# ----------------------------
FRONTEND_URL = config("FRONTEND_URL")

# ----------------------------
# GOOGLE AUTH
# ----------------------------
GOOGLE_CLIENT_ID = config("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = config("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = config("GOOGLE_REDIRECT_URI")

# ----------------------------
# GITHUB AUTH
# ----------------------------
GITHUB_CLIENT_ID = config("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = config("GITHUB_CLIENT_SECRET")
GITHUB_REDIRECT_URI = config("GITHUB_REDIRECT_URI")

# ----------------------------
# Database
# ----------------------------
ENV = config("ENV", default="local")

if ENV == "local":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": dj_database_url.parse(
            config("DATABASE_URL"),
            conn_max_age=600,
            ssl_require=True,
        )
    }

# ----------------------------
# Authentication & Passwords
# ----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ----------------------------
# Internationalization
# ----------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ----------------------------
# Media Upload
# ----------------------------
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# ----------------------------
# Static Files
# ----------------------------
STATIC_URL = "static/"

# ----------------------------
# Default Primary Key Field
# ----------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
