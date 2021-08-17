import pytest
from user_poll.models import Poll

from .fixtures import *


class TestPollAPI:

    @pytest.mark.django_db(transaction=True)
    def test_poll_list(self, client):
        response = client.get('/api/v1/poll/')

        assert response.status_code == 200

    @pytest.mark.django_db(transaction=True)
    def test_create_poll_without_auth(self, client, create_poll_data):
        response = client.post('/api/v1/poll/', create_poll_data)

        assert response.status_code == 401

    @pytest.mark.django_db(transaction=True)
    def test_create_poll_for_user(self, api_client_user, create_poll_data):
        response = api_client_user.post('/api/v1/poll/', create_poll_data)

        assert response.status_code == 403

    @pytest.mark.django_db(transaction=True)
    def test_create_poll_for_admin(self, api_client_admin, create_poll_data):
        response = api_client_admin.post('/api/v1/poll/', create_poll_data)
        assert response.status_code == 201

    @pytest.mark.django_db(transaction=True)
    def test_edit_poll(self, api_client_admin, create_poll_data):
        r = api_client_admin.post('/api/v1/poll/', create_poll_data)
        poll_id = r.json()['id']
        response = api_client_admin.patch(f'/api/v1/poll/{poll_id}/', {'description': 'новое описание'})
        assert response.json()['description'] == 'новое описание'

    @pytest.mark.django_db(transaction=True)
    def test_delete_poll(self, api_client_admin, create_poll_data):
        r = api_client_admin.post('/api/v1/poll/', create_poll_data)
        poll_id = r.json()['id']
        response = api_client_admin.delete(f'/api/v1/poll/{poll_id}/')
        assert response.status_code == 204
