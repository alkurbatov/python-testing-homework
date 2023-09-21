from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse
from plugins.pictures.favourite import (
    FavouritePictureAssertion,
    PictureData,
    PictureDataFactory,
)

from server.apps.identity.models import User


@pytest.fixture()
def add_picture_data(
    picture_data_factory: PictureDataFactory,
) -> PictureData:
    """Create data for add to favorite operation."""
    return picture_data_factory()


@pytest.mark.django_db()
@pytest.mark.usefixtures('logged_in_user')
def test_add_picture_to_favorites(
    client: Client,
    logged_in_user: User,
    add_picture_data: PictureData,
    assert_picture_is_users_favourite: FavouritePictureAssertion,
) -> None:
    """Test that add to favorites works with correct picture data."""
    response = client.post(
        reverse('pictures:dashboard'),
        data=add_picture_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == reverse('pictures:dashboard')
    assert_picture_is_users_favourite(
        logged_in_user,
        add_picture_data,
    )
