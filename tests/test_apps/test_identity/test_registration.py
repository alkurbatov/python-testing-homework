from http import HTTPStatus
from typing import Callable, TypeAlias

import pytest
from django.test import Client
from django.urls import reverse
from plugins.identity.user import (
    RegistrationData,
    RegistrationDataFactory,
    UserAssertion,
    UserData,
)

from server.apps.identity.models import User

UserDataExtractor: TypeAlias = Callable[[RegistrationData], UserData]


@pytest.fixture()
def user_registration_data(
    registration_data_factory: RegistrationDataFactory,
) -> RegistrationData:
    """Create instance of ordinary user (not staff or admin)."""
    return registration_data_factory()


@pytest.fixture()
def user_data() -> UserDataExtractor:
    """
    We need to extract user data from registration data.

    Basically, it is the same as ``registration_data``, but without passwords.
    """
    def factory(registration_data: RegistrationData) -> UserData:
        return {
            key_name: value_part
            for key_name, value_part in registration_data.items()
            if not key_name.startswith('password')
        }

    return factory


@pytest.mark.django_db()
def test_valid_registration(
    client: Client,
    user_registration_data: RegistrationData,
    user_data: UserDataExtractor,
    assert_correct_user: UserAssertion,
) -> None:
    """Test that registration works with correct user data."""
    response = client.post(
        reverse('identity:registration'),
        data=user_registration_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == reverse('identity:login')
    assert_correct_user(
        user_registration_data['email'],
        user_data(user_registration_data),
    )


@pytest.mark.django_db()
def test_registration_missing_required_field(
    client: Client,
    registration_data_factory: RegistrationDataFactory,
) -> None:
    """Test that missing required will fail the registration."""
    post_data = registration_data_factory(email='')

    response = client.post(
        reverse('identity:registration'),
        data=post_data,
    )

    assert response.status_code == HTTPStatus.OK
    assert not User.objects.filter(email=post_data['email'])
