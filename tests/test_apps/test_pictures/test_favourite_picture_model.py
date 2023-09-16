import pytest
from plugins.pictures.favourite import FavouritePictureFactory

from server.apps.identity.models import User


@pytest.mark.django_db()
def test_favoured_picture_as_string(
    logged_in_user: User,
    favourite_picture_factory: FavouritePictureFactory,
) -> None:
    """Test that ``FavouritePicture`` can be serialized to string."""
    picture = favourite_picture_factory(logged_in_user)

    expected = '<Picture {picture_id} by {user_id}>'.format(
        picture_id=picture.foreign_id,
        user_id=logged_in_user.id,
    )

    assert str(picture) == expected
