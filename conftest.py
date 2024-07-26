import os
import pytest
from django.conf import settings
import django
from rest_framework.test import APIClient
from moviecollection.models import User


os.environ["DJANGO_SETTINGS_MODULE"] = "MovieCollectionApp.settings"
django.setup()
pytest_plugins = [
    "django.contrib.auth",
    "django.contrib.sessions",
]


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client():
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.auth = {'user_id': user.id}
    client.force_authenticate(user=user)
    return client