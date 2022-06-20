import environ
import logging
import os
import traceback
import uuid

from pathlib import Path

# ---------------------------------------------------------------------------#
# Setup                                                                      #
# ---------------------------------------------------------------------------#

# GENERAL
# ----------------------------------------------------------------------------

PROJECT_NAME = "{{cookiecutter.project_abbr}}"
SITE_ID = 1

# PATHS
# ------------------------------------------------------------------------------

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
APPS_DIR = BASE_DIR / "{{ cookiecutter.directory_name }}"

# URLS
# ------------------------------------------------------------------------------

SHARED_URL = "{{cookiecutter.shared_url}}"
IMPRINT_URL = SHARED_URL + "imprint"
ROOT_URLCONF = 'djangobaseproject.urls'
WSGI_APPLICATION = 'djangobaseproject.wsgi.application'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'

# ENVIRONMENT
# ----------------------------------------------------------------------------

env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(BASE_DIR / ".env"))

# DEBUG
# ----------------------------------------------------------------------------

# SECURITY WARNING: don't run with debug turned on in production!
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)

# debug SQL statements (logs all SQL statements to a dedicated log file defined in the respective LOGGING handler)
{% if cookiecutter.debug_sql == 'y' -%}
DEBUG_SQL = True
{%- else %}
DEBUG_SQL = False
{%- endif %}

# SECURITY
# ----------------------------------------------------------------------------

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(uuid.uuid4())

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
]
ADD_ALLOWED_HOST = env.list('ALLOWED_HOST', default="127.0.0.1")
ALLOWED_HOSTS += ADD_ALLOWED_HOST


# corsheaders settings
CORS_ORIGIN_ALLOW_ALL = False
ADD_CORS_ORIGIN_WHITELIST = env('CORS_ORIGIN_WHITELIST', default="http://127.0.0.1")
CORS_ORIGIN_WHITELIST = [
    ADD_CORS_ORIGIN_WHITELIST,
]

# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# FORM LAYOUT
# ----------------------------------------------------------------------------

# Crispy Forms UI Library
CRISPY_ALLOWED_TEMPLATE_PACKS = ('bootstrap', 'uni_form', 'bootstrap3', 'bootstrap4',)
CRISPY_TEMPLATE_PACK = "bootstrap4"

# FIELD TYPE
# ----------------------------------------------------------------------------

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------------------------------------------------#
# Application(s)                                                             #
# ---------------------------------------------------------------------------#

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
]

THIRD_PARTY_APPS = [
    'corsheaders',
    'guardian',
    'crispy_forms',
    'django_filters',
    'django_tables2',
    'django_spaghetti',
    'fsm_admin',
]

LOCAL_APPS = [
    'core',
    'users',
    'webpage',
    'browsing',
    'infos',
]

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ---------------------------------------------------------------------------#
# Middleware                                                                 #
# ---------------------------------------------------------------------------#

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

# ---------------------------------------------------------------------------#
# Templates                                                                  #
# ---------------------------------------------------------------------------#

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(APPS_DIR / "templates")
        ],
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
            'NAME': env('POSTGRES_DB', default="{{cookiecutter.project_slug}}"),
            'USER': env('POSTGRES_USER', default='postgres'),
            'PASSWORD': env('POSTGRES_PASSWORD', default='postgres'),
            'HOST': env('POSTGRES_HOST', default='localhost'),
            'PORT': env('POSTEGRES_PORT', default='5432')
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

# custom user model
AUTH_USER_MODEL = 'users.CustomUser'

# anonymous user for guardianed content (public content)
GUARDIAN_GET_INIT_ANONYMOUS_USER = 'users.models.get_custom_anon_user'

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

# LDAP authentication if activated
{% if cookiecutter.ldap_authentication == 'y' -%}
try:
    import ldap
    from django_auth_ldap.config import LDAPSearch

    AUTH_LDAP_SERVER_URI = env('LDAP_SERVER_URI', default="ldap://")
    AUTH_LDAP_BIND_DN = env('LDAP_BIND_DN', default="cn=xxx")
    AUTH_LDAP_BIND_PASSWORD = env('LDAP_BIND_PASSWORD', default="password")
    AUTH_LDAP_USER_ATTR_MAP = env.dict('LDAP_USER_ATTR_MAP', default={"last_name":"sn"})
    AUTH_LDAP_USER_SEARCH = LDAPSearch(env('LDAP_USER_SEARCH', default="o="),
                                       ldap.SCOPE_SUBTREE, env('LDAP_USER_SEARCH_SCOPE', default="cn=%(user)s)"))

    AUTHENTICATION_BACKENDS = (
        'users.models.CustomLDAPBackend',
        'django.contrib.auth.backends.ModelBackend',
        'guardian.backends.ObjectPermissionBackend',
    )
except Exception as error:
    traceback.print_exc(f"Error: {error}, {traceback.format_exc()}")

{%- else %}
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)
{%- endif %}
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

# STATIC
# ----------------------------------------------------------------------------

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')
STATIC_URL = '/static/'

# MEDIA
# ----------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------#
# Logging                                                                    #
# ---------------------------------------------------------------------------#

LOG_DIR = str(BASE_DIR) + '/log/{{cookiecutter.project_slug}}'

if not os.path.exists(LOG_DIR):
    try:
        os.makedirs(LOG_DIR)
    except Exception as error:
        traceback.print_exc(f"Error: {error}, {traceback.format_exc()}")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'server.log'),
            'formatter': 'verbose',
        },
        'sql': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'sql.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file', ],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console', 'file', ],
            'propagate': True,
            'level': 'INFO',
        },
        'django.db.backends': {
            'handlers': ['console', 'sql', ],
            'propagate': True,
            'level': 'DEBUG',
        }
    },
}

if DEBUG_SQL is True:
    INSTALLED_APPS.append('django_extensions')
    logger = logging.getLogger('django.db.backends')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
