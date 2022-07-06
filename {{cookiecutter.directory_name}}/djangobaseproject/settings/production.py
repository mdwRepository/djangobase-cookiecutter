from .base import *  # noqa
from .base import env

# ---------------------------------------------------------------------------#
# Setup                                                                      #
# ---------------------------------------------------------------------------#

# GENERAL
# ----------------------------------------------------------------------------

# add context (path) to app in django environments where we do not have access to a proxy / webserver
USE_X_FORWARDED_HOST = True
FORCE_SCRIPT_NAME = env('FORCE_SCRIPT_NAME', default="/")
SESSION_COOKIE_PATH = env('FORCE_SCRIPT_NAME', default="/")
# APPEND_SLASH = False


# SECURITY
# ----------------------------------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True

DEBUG = False
DEBUG_SQL = False

# ---------------------------------------------------------------------------#
# Files                                                                      #
# ---------------------------------------------------------------------------#

# STATIC
# ----------------------------------------------------------------------------

MEDIA_URL = env('FORCE_SCRIPT_NAME', default="/") + 'media/'
STATIC_URL = env('FORCE_SCRIPT_NAME', default="/") + 'static/'
