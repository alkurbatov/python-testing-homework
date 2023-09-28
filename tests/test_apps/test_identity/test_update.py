from http import HTTPStatus
from typing import cast

import pytest
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse
from plugins.identity.user import UserAssertion, UserData, UserDataFactory
from pytest_django.asserts import assertTemplateUsed

from server.apps.identity.models import User


@pytest.fixture()
def user_update_data(
    logged_in_user: User,
    user_data_factory: UserDataFactory,
) -> UserData:
    """Create data for update user operation."""
    return user_data_factory(email=logged_in_user.email)


@pytest.mark.django_db()
def test_valid_update(
    client: Client,
    user_update_data: UserData,
    assert_correct_user: UserAssertion,
) -> None:
    """Test that update works with correct user data."""
    response = client.post(
        reverse('identity:user_update'),
        data=user_update_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == reverse('identity:user_update')
    assert_correct_user(
        user_update_data['email'],
        user_update_data,
    )


@pytest.mark.django_db()
@pytest.mark.usefixtures('logged_in_user')
def test_render_update_view(client: Client) -> None:
    """Test that correct template used to render update user page."""
    response = cast(HttpResponse, client.get(reverse('identity:user_update')))

    assertTemplateUsed(
        response,
        'identity/pages/user_update.html',
    )
