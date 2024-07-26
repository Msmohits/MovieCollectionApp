import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_register_user_with_email(api_client):
    url = reverse('register')
    user_data = {
        "username": "testuser1",
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    response = api_client.post(url, user_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert 'access_token' in response.json()