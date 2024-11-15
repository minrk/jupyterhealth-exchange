"""
Django settings for jhe project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--4r1=)&2xj1u&sfj7*$jfzdp@*pyr*^n4l*n1p^inne@ulzn1f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    'whitebrick.ngrok.app',
    'jhe.fly.dev'
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'https://whitebrick.ngrok.app',
    'https://jhe.fly.dev'
]


SITE_TITLE = os.getenv('SITE_TITLE')
SITE_URL = os.getenv('SITE_URL')
CH_INVITATION_LINK_PREFIX = os.getenv('CH_INVITATION_LINK_PREFIX')
OIDC_CLIENT_AUTHORITY = SITE_URL + os.getenv('OIDC_CLIENT_AUTHORITY_PATH')
OIDC_CLIENT_ID = os.getenv('OIDC_CLIENT_ID') # TBD: Multi-tenancy lookup based on client entry URI
OIDC_CLIENT_REDIRECT_URI = SITE_URL + os.getenv('OIDC_CLIENT_REDIRECT_URI_PATH')



# https://stackoverflow.com/questions/62047354/build-absolute-uri-with-https-behind-reverse-proxy
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

INSTALLED_APPS = [
    'core',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'oauth2_provider',
    'rest_framework',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 1000,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
     ),
     'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ),
    'JSON_UNDERSCOREIZE': {
        'ignore_keys': ('response_type','client_id','redirect_uri','code_challenge','code_challenge_method','grant_type','code_verifier')
    },
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'djangorestframework_camel_case.middleware.CamelCaseMiddleWare'
]

ROOT_URLCONF = 'jhe.urls'

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
                "core.context_processors.constants",
            ],
        },
    },
]

WSGI_APPLICATION = 'jhe.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DB_USER_SECRET_NAME = os.environ.get('DATABASE_USER_SECRET_NAME', 'DATABASE_USER')
DB_PASSWORD_SECRET_NAME = os.environ.get('DATABASE_PASSWORD_SECRET_NAME', 'DATABASE_PASSWORD')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# https://django-oauth-toolkit.readthedocs.io/en/latest/getting_started.html
AUTH_USER_MODEL = 'core.JheUser'
REGISTRATION_INVITE_CODE = 'jhe2024'

# LOGIN_URL = '/admin/login/' for staff accounts
LOGIN_URL = '/accounts/login/'
OAUTH2_PROVIDER = {
    "OIDC_ENABLED": True,
    "OIDC_RSA_PRIVATE_KEY": os.getenv('OIDC_RSA_PRIVATE_KEY'),
    "SCOPES": {
        "openid": "OpenID Connect scope"
    }
}
ACCESS_TOKEN_EXPIRE_SECONDS = 1209600 # 2 weeks

PATIENT_AUTHORIZATION_CODE_EXPIRE_SECONDS = 1209600 # 2 weeks
PATIENT_AUTHORIZATION_CODE_CHALLENGE= '-2FUJ5UCa7NK9hZWS0bc0W9uJ-Zr_-Pngd4on69oxpU'
PATIENT_AUTHORIZATION_CODE_VERIFIER = 'f28984eaebcf41d881223399fc8eab27eaa374a9a8134eb3a900a3b7c0e6feab5b427479f3284ebe9c15b698849b0de2'

X_FRAME_OPTIONS = "SAMEORIGIN"


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = "smtp.gmail.com"
#EMAIL_HOST_USER = "youremail@gmail.com"
#EMAIL_HOST_PASSWORD = "your email password"
#EMAIL_PORT = 587
#EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'JHE Support <support@jhe.org>'



CODE_VERIFIER = 'N0hHRVk2WDNCUUFPQTIwVDNZWEpFSjI4UElNV1pSTlpRUFBXNTEzU0QzRTMzRE85WDFWTzU2WU9ESw=='

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'core/static/')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
