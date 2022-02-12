"""
Django settings for pets project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
from starlette.config import Config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# upload env variables from .env
CONFIG = Config(BASE_DIR / ".env")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CONFIG.get("SECRET_KEY", cast=str, default="")

# upload debug option from environment file, default is False
DEBUG = CONFIG.get("PROJECT_DEBUG", cast=bool , default=False)

# open the project for all
ALLOWED_HOSTS = [CONFIG.get("ALLOED_HOSTS", cast=str , default="127.0.0.1")]


# Application definition
# adding the rest_frame work
# adding api to the list of installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'api.apps.ApiConfig',


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pets.urls'

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

WSGI_APPLICATION = 'pets.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
# using postgres database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': CONFIG.get("DATABASE_HOST",cast=str),
        'PORT': CONFIG.get("DATABASE_PORT",cast=int),
        'USER': CONFIG.get("DATABASE_USER",cast=str),
        'PASSWORD': CONFIG.get("DATABASE_PASS",cast=str),
        'NAME': CONFIG.get("DATABASE_NAME",cast=str), 
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

# django rest framework settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20
}

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# setting the api_key in the env file
API_KEY = CONFIG.get("API_KEY", cast=str, default="api-key")
API_HOST = CONFIG.get("API_HOST", cast=str, default="localhost")
API_PORT = CONFIG.get("API_PORT", cast=str, default="localhost")
API_PROTOCOL = CONFIG.get("API_PROTOCOL", cast=str, default="http")
# define the domain url
DOMAIN_URL = f"{API_PROTOCOL}://{API_HOST}:{API_PORT}"
# define the media folder
MEDIA_ROOT = BASE_DIR / "img"
Path(MEDIA_ROOT).mkdir(parents=True, exist_ok=True)
# define the media root url
MEDIA_URL = '/'
