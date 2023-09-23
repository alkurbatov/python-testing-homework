from typing import cast

import pytest
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse
from plugins.pictures.favourite import FavouritePictureFactory
from pytest_django.asserts import assertContains, assertTemplateUsed

from server.apps.identity.models import User
from server.apps.pictures.models import FavouritePicture


@pytest.fixture()
def picture(
    logged_in_user: User,
    favourite_picture_factory: FavouritePictureFactory,
) -> FavouritePicture:
    """Create instance of FavouritePicture attached to user."""
    return favourite_picture_factory(logged_in_user)


@pytest.fixture()
def user_with_favourite_pictures(
    logged_in_user: User,
    picture: FavouritePicture,
) -> User:
    """Inject a favourite picture into user's data."""
    logged_in_user.pictures.add(picture)

    return logged_in_user


@pytest.mark.django_db()
@pytest.mark.usefixtures('user_with_favourite_pictures')
def test_render_favourites_pictures_view(
    client: Client,
) -> None:
    """Test that correct template used to render favourites pictures page."""
    response = cast(HttpResponse, client.get(reverse('pictures:favourites')))

    assertTemplateUsed(
        response,
        'pictures/pages/favourites.html',
    )
    assertContains(
        response,
        'data-test-id="favourites-picture-db"',
        1,
    )
