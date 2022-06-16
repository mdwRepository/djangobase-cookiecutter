"""
Django settings for djangobaseproject project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
import traceback
import uuid

from pathlib import Path

# ---------------------------------------------------------------------------#
# Setup                                                                      #
# ---------------------------------------------------------------------------#

# project configuration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SHARED_URL = "{{cookiecutter.shared_url}}"
PROJECT_NAME = "{{cookiecutter.project_abbr}}"
IMPRINT_URL = SHARED_URL + "imprint"
ROOT_URLCONF = 'djangobaseproject.urls'
WSGI_APPLICATION = 'djangobaseproject.wsgi.application'
SITE_ID = 1

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(uuid.uuid4())

# SECURITY WARNING: don't run with debug turned on in production!
# debug SQL statements (logs all SQL statements to a dedicated log file defined in the respective LOGGING handler)
if os.environ.get('DEBUG'):
    DEBUG = True
else:
    DEBUG = False

ADD_ALLOWED_HOST = os.environ.get('ALLOWED_HOST', '*')

ALLOWED_HOSTS = [
    "127.0.0.1",
    ADD_ALLOWED_HOST,
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms UI Library
CRISPY_ALLOWED_TEMPLATE_PACKS = ('bootstrap', 'uni_form', 'bootstrap3', 'bootstrap4',)
CRISPY_TEMPLATE_PACK = "bootstrap4"

# ---------------------------------------------------------------------------#
# Application(s)                                                             #
# ---------------------------------------------------------------------------#

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'guardian',
    'crispy_forms',
    'django_filters',
    'django_tables2',
    'django_spaghetti',
    'webpage',
    'browsing',
    'infos',
]

# ---------------------------------------------------------------------------#
# Middleware                                                                 #
# ---------------------------------------------------------------------------#

# Middleware definition

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------------------------------------------------------------------------#
# Templates                                                                  #
# ---------------------------------------------------------------------------#

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
                'webpage.webpage_content_processors.installed_apps',
                'webpage.webpage_content_processors.is_dev_version',
                'webpage.webpage_content_processors.get_db_name',
                "webpage.webpage_content_processors.shared_url",
                "webpage.webpage_content_processors.my_app_name",
            ],
        },
    },
]

# ---------------------------------------------------------------------------#
# Database                                                                   #
# ---------------------------------------------------------------------------#

if os.environ.get('POSTGRES_DB'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB'),
            'USER': os.environ.get('POSTGRES_USER', 'postgres'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
            'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
            'PORT': os.environ.get('POSTEGRES_PORT', '5432')
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ---------------------------------------------------------------------------#
# Authentication                                                             #
# ---------------------------------------------------------------------------#

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

# ---------------------------------------------------------------------------#
# Internationalization                                                       #
# ---------------------------------------------------------------------------#

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

USE_I18N = True

LANGUAGE_CODE = "{{cookiecutter.language_code}}"

USE_L10N = True

USE_TZ = True

TIME_ZONE = "{{cookiecutter.timezone}}"

# ---------------------------------------------------------------------------#
# Files                                                                      #
# ---------------------------------------------------------------------------#

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

# ---------------------------------------------------------------------------#
# django Spaghetti                                                           #
# ---------------------------------------------------------------------------#

SPAGHETTI_SAUCE = {
    'apps': [
        'infos',
    ],
    'show_fields': False,
    'exclude': {'auth': ['user']},
}
