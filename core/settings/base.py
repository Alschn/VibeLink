"""
Django settings for VibeLink backend project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path

from environ import Env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = Env()
env.read_env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'corsheaders',
    'django_extensions',
    'drf_spectacular',
    'django_jsonform',
    'django_filters',

    'rest_framework',

    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'dj_rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',

    'django_q',

    'friendship',

    # apps
    'core',
    'accounts',
    'links',
    'tracks',
    'emails',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

ASGI_APPLICATION = 'core.asgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

IS_GITHUB_WORKFLOW = env('GITHUB_WORKFLOW', default=None)

USE_LOCAL_SQLITE_DB = env.bool('USE_LOCAL_SQLITE_DB', default=False)

DATABASE_URL = env('DATABASE_URL', default=None)

if IS_GITHUB_WORKFLOW:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'github_actions',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }

elif USE_LOCAL_SQLITE_DB:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
            'TEST': {
                'NAME': BASE_DIR / 'test_db.sqlite3',
            }
        }
    }

elif DATABASE_URL:
    db_from_env = dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=500,
        conn_health_checks=True,
        ssl_require=True
    )
    DATABASES = {
        'default': db_from_env
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': env('DB_ENGINE'),
            'NAME': env('DB_NAME'),
            'USER': env('DB_USER'),
            'PASSWORD': env('DB_PASSWORD'),
            'HOST': env('DB_HOST'),
            'PORT': env.int('DB_PORT'),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

USE_AWS_S3 = env('USE_AWS_S3', cast=bool, default=False)

if USE_AWS_S3:
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    AWS_DEFAULT_ACL = None
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': f'max-age={24 * 3600}'
    }

    STATIC_LOCATION = 'static'
    PUBLIC_MEDIA_LOCATION = 'uploads'

    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'

    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'

    STORAGES = {
        'default': {
            'BACKEND': 'core.storages.PublicMediaStorage'
        },
        'staticfiles': {
            'BACKEND': 'core.storages.StaticStorage'
        },
    }

else:
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'staticfiles'

    MEDIA_URL = '/uploads/'
    MEDIA_ROOT = BASE_DIR / 'uploads'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework settings
# https://www.django-rest-framework.org/api-guide/settings/

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),

    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# Authentication backends
# https://docs.allauth.org/en/latest/account/configuration.html

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# JWT settings
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html

access_token_lifetime_seconds = env.int('SIMPLE_JWT_ACCESS_TOKEN_SECONDS', default=60 * 60)  # 1 hour
refresh_token_lifetime_seconds = env.int('SIMPLE_JWT_REFRESH_TOKEN_SECONDS', default=60 * 60 * 24)  # 1 day

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(seconds=access_token_lifetime_seconds),
    'REFRESH_TOKEN_LIFETIME': timedelta(seconds=refresh_token_lifetime_seconds),
    'UPDATE_LAST_LOGIN': False,

    'AUDIENCE': env.list('SIMPLE_JWT_AUDIENCE', default=None),
    'ISSUER': env.str('SIMPLE_JWT_ISSUER', default=None),
}

# django-allauth settings
# https://docs.allauth.org/en/latest/account/configuration.html

ACCOUNT_ADAPTER = 'accounts.adapters.AccountAdapter'
SOCIALACCOUNT_ADAPTER = 'accounts.adapters.SocialAccountAdapter'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = env.int('ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN', default=1 * 60)
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = env.int('ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS', default=1)
ACCOUNT_EMAIL_CONFIRMATION_HMAC = True

ACCOUNT_MAX_EMAIL_ADDRESSES = None

ACCOUNT_LOGIN_ATTEMPTS_LIMIT = env.int('ACCOUNT_LOGIN_ATTEMPTS_LIMIT', default=5)
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = env.int('ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT', default=1 * 60)

OLD_PASSWORD_FIELD_ENABLED = True

# dj-rest-auth settings
# https://dj-rest-auth.readthedocs.io/en/latest/configuration.html#configuration

REST_AUTH = {
    'TOKEN_MODEL': None,
    'SESSION_LOGIN': False,

    'PASSWORD_RESET_SERIALIZER': 'accounts.serializers.PasswordResetSerializer',

    'USE_JWT': True,
    'JWT_AUTH_RETURN_EXPIRATION': False,
    'JWT_AUTH_COOKIE': None,
    'JWT_AUTH_REFRESH_COOKIE': None,
    'JWT_AUTH_HTTPONLY': False,
    'JWT_TOKEN_CLAIMS_SERIALIZER': 'accounts.serializers.JWTClaimsSerializer',
}

# drf-spectacular settings
# https://drf-spectacular.readthedocs.io/en/latest/settings.html

SPECTACULAR_SETTINGS = {
    'TITLE': 'VibeLink API',
    'DESCRIPTION': 'VibeLink REST API provided by Alschn',
    'VERSION': '0.1.0',
    'CONTACT': {
        'name': 'Alschn',
        'url': 'https://github.com/Alschn/',
    },
    'SCHEMA_PATH_PREFIX': '/api/',
    'SERVE_PERMISSIONS': ['rest_framework.permissions.AllowAny'],
}

# django-cors-headers settings
# https://pypi.org/project/django-cors-headers/

CORS_ALLOW_ALL_ORIGINS = env.bool('CORS_ALLOW_ALL_ORIGINS', default=False)

CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])

CORS_ORIGIN_WHITELIST = env.list('CORS_ORIGIN_WHITELIST', default=[])

CORS_ORIGIN_REGEX_WHITELIST = env.list('CORS_ORIGIN_REGEX_WHITELIST', default=[])

# Django Q configuration
# https://django-q2.readthedocs.io/en/master/configure.html

REDIS_HOST = env('REDIS_HOST', default='redis_db')
REDIS_PORT = env.int('REDIS_PORT', default=6379)

# default values taken from the documentation
Q_CLUSTER_NAME = env('Q_CLUSTER_NAME', default='vibelink')
Q_CLUSTER_WORKERS = env.int('Q_CLUSTER_WORKERS', default=4)
Q_CLUSTER_DAEMONIZE_WORKERS = env.bool('Q_CLUSTER_DAEMONIZE_WORKERS', default=False)
Q_CLUSTER_RECYCLE = env.int('Q_CLUSTER_RECYCLE', default=500)
Q_CLUSTER_TIMEOUT = env.int('Q_CLUSTER_TIMEOUT', default=60)
Q_CLUSTER_COMPRESS = env.bool('Q_CLUSTER_COMPRESS', default=True)
Q_CLUSTER_MAX_ATTEMPTS = env.int('Q_CLUSTER_MAX_ATTEMPTS', default=0)
Q_CLUSTER_RETRY = env.int('Q_CLUSTER_RETRY', default=60)
Q_CLUSTER_SAVE_LIMIT = env.int('Q_CLUSTER_SAVE_LIMIT', default=250)
Q_CLUSTER_QUEUE_LIMIT = env.int('Q_CLUSTER_QUEUE_LIMIT', default=500)
Q_CLUSTER_CPU_AFFINITY = env.int('Q_CLUSTER_CPU_AFFINITY', default=1)
Q_CLUSTER_SYNC = False
Q_CLUSTER_CATCH_UP = True

Q_CLUSTER = {
    'name': Q_CLUSTER_NAME,
    'workers': Q_CLUSTER_WORKERS,
    'daemonize_workers': Q_CLUSTER_DAEMONIZE_WORKERS,
    'recycle': Q_CLUSTER_RECYCLE,
    'timeout': Q_CLUSTER_TIMEOUT,
    'compress': Q_CLUSTER_COMPRESS,
    'max_attempts': Q_CLUSTER_MAX_ATTEMPTS,
    'retry': Q_CLUSTER_RETRY,
    'save_limit': Q_CLUSTER_SAVE_LIMIT,
    'queue_limit': Q_CLUSTER_QUEUE_LIMIT,
    'cpu_affinity': Q_CLUSTER_CPU_AFFINITY,
    'sync': Q_CLUSTER_SYNC,
    'catch_up': Q_CLUSTER_CATCH_UP,
    'label': 'Django Q2',
    'redis': {
        'host': REDIS_HOST,
        'port': REDIS_PORT,
        'db': 0,
    }
}

# Django cache settings
# https://docs.djangoproject.com/en/4.2/topics/cache/

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f'redis://{REDIS_HOST}:{REDIS_PORT}',
    },
}

# django.contrib.sites settings
# https://docs.djangoproject.com/en/4.2/ref/contrib/sites/

SITE_ID = 1

FRONTEND_SITE_NAME = env('FRONTEND_SITE_NAME', default='VibeLink')

# Emails config
# https://docs.djangoproject.com/en/4.2/topics/email/#smtp-backend

USE_SMTP = env.bool('USE_SMTP', default=False)

if USE_SMTP:
    EMAIL_BACKEND = 'emails.backends.DjangoQBackend'
    DJANGO_Q_EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    EMAIL_HOST = env('EMAIL_HOST')
    EMAIL_PORT = env('EMAIL_PORT', cast=int)
    EMAIL_HOST_USER = env('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
    EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=False)
    EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL', default=False)
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
else:
    EMAIL_BACKEND = 'emails.backends.DjangoQBackend'
    DJANGO_Q_EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Custom user
# https://docs.djangoproject.com/en/4.2/topics/auth/customizing/

AUTH_USER_MODEL = 'accounts.User'

# Spotipy settings
# https://spotipy.readthedocs.io/en/2.22.1/#

SPOTIPY_CLIENT_ID = env('SPOTIPY_CLIENT_ID', default=None)
SPOTIPY_CLIENT_SECRET = env('SPOTIPY_CLIENT_SECRET', default=None)

# Google API Python Client settings
# https://googleapis.github.io/google-api-python-client/docs/dyn/

GOOGLE_CLOUD_API_KEY = env('GOOGLE_CLOUD_API_KEY', default=None)
