import os
import pytest
from django.conf import settings
import django


os.environ['DJANGO_SETTINGS_MODULE'] = 'MovieCollectionApp.settings'
django.setup()
pytest_plugins = [
    'django.contrib.auth',
    'django.contrib.sessions',
]
