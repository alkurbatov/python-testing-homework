from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse
from mimesis.schema import Field
from plugins.identity.user import LoginData, UserFactory


@pytest.fixture()
def login_data(
    mf: Field,
    user_factory: UserFactory,
) -> LoginData:
    """Returns factory for fake random data for login."""
    password = mf('password')
    user = user_factory(password)

    return {
        'username': user.email,
        'password': password,
    }


@pytest.mark.django_db()
def test_valid_login(
    client: Client,
    login_data: LoginData,
) -> None:
    """Test that login works with correct user data."""
    response = client.post(
        reverse('identity:login'),
        data=login_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == reverse('pictures:dashboard')


@pytest.mark.django_db()
def test_invalid_login(
    mf: Field,
    client: Client,
    login_data: LoginData,
) -> None:
    """Test that login does not works with invalid data."""
    login_data['password'] = mf('password')

    response = client.post(
        reverse('identity:login'),
        data=login_data,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.get('Location') is None
