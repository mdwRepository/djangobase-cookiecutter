from .base import *  # noqa
from .base import env

# ---------------------------------------------------------------------------#
# Setup                                                                      #
# ---------------------------------------------------------------------------#

# SECURITY
# ----------------------------------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True

