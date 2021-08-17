import pytest

from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture()
def resource(client):
    User.objects.create(username='admin', email='admin@admin.com', password='admin', is_staff=True)
    User.objects.create(username='user', email='user@user.com', password='user')
    yield


@pytest.fixture
def api_client_user(resource):
    client = APIClient()
    refresh = RefreshToken.for_user(User.objects.get(username='user'))
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.fixture
def api_client_admin(resource):
    client = APIClient()
    refresh = RefreshToken.for_user(User.objects.get(username='admin'))
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client
