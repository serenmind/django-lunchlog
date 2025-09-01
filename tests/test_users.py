import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_signup_creates_user():
    client = APIClient()
    resp = client.post('/auth/signup/', {'username': 'alice', 'password': 'secret', 'email': 'a@example.com'}, format='json')
    assert resp.status_code == 201
    data = resp.json()
    assert 'id' in data and 'username' in data
    User = get_user_model()
    assert User.objects.filter(username='alice').exists()
