"""
Django settings for web project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import logging
from pathlib import Path

from decouple import Csv, config
from dj_database_url import parse as db_url

from libs.ibge import City, CityABC
from libs.querido_diario import QueridoDiario, QueridoDiarioABC
from libs.services import services

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("QD_BACKEND_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("QD_BACKEND_DEBUG", cast=bool, default=False)


ALLOWED_HOSTS = config("QD_BACKEND_ALLOWED_HOSTS", cast=Csv())
FRONT_BASE_URL = config("FRONT_BASE_URL")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "django_rest_passwordreset",
    "corsheaders",
    "anymail",
    "accounts.apps.AccountsConfig",
    "alerts.apps.AlertsConfig",
    "querido_diario.apps.QueridoDiarioConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": db_url(config("QD_BACKEND_DB_URL"), conn_max_age=600),
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = config("STATIC_URL", default="api/static/")
STATIC_ROOT = Path(BASE_DIR, "static")
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = "media/"
MEDIA_ROOT = Path(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 30,
}

CORS_ALLOWED_ORIGINS = config("QD_BACKEND_ALLOWED_ORIGINS", cast=Csv())

CORS_ALLOWED_ORIGIN_REGEXES = config("QD_BACKEND_ALLOWED_ORIGIN_REGEXES", cast=Csv())

CSRF_TRUSTED_ORIGINS = config("QD_BACKEND_CSRF_TRUSTED_ORIGINS", cast=Csv())

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CELERY_BROKER_URL = config("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "America/Sao_Paulo"

QD_API_URL = config("QD_API_URL")

QD_API_THEME = config("QD_API_THEME")

services.register(
    QueridoDiarioABC,
    QueridoDiario(
        api_url=QD_API_URL,
        theme=QD_API_THEME,
    ),
)

services.register(CityABC, City())


EMAIL_BACKEND = "anymail.backends.mailjet.EmailBackend"
MAILJET_API_URL = "https://api.mailjet.com/v3.1/"

MAILJET_API_KEY = config("MAILJET_API_KEY")
MAILJET_SECRET_KEY = config("MAILJET_SECRET_KEY")

EMAIL_FILE_PATH = Path(BASE_DIR, "emails")

EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")
SERVER_EMAIL = config("SERVER_EMAIL")
QUOTATION_TO_EMAIL = config("QUOTATION_TO_EMAIL")

ANYMAIL = {
    "MAILJET_API_KEY": MAILJET_API_KEY,
    "MAILJET_SECRET_KEY": MAILJET_SECRET_KEY,
}

PROJECT_TITLE = config("PROJECT_TITLE")
ALERT_HOUR = config("ALERT_HOUR", cast=int, default=1)
ALERT_MINUTE = config("ALERT_MINUTE", cast=int, default=0)

logging.basicConfig(level=logging.DEBUG)