"""Utility module for compatibility between Django and Python versions."""
from __future__ import unicode_literals

from django.conf import settings
try:
    from django.contrib.auth import get_user_model
except ImportError: # pragma: no cover
    # Django < 1.5
    from django.contrib.auth.models import User
    User.USERNAME_FIELD = 'username'
    get_user_model = lambda: User