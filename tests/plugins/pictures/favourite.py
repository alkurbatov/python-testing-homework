from typing import Callable, Protocol, TypeAlias, TypedDict, final

import pytest
from mimesis.random import Random
from mimesis.schema import Field, Schema
from typing_extensions import Unpack

from server.apps.identity.models import User
from server.apps.pictures.models import FavouritePicture


@final
class PictureData(TypedDict, total=False):
    """Represent data of a picture loaded from side service."""

    foreign_id: int
    url: str


@final
class PictureDataFactory(Protocol):  # type: ignore[misc]
    """Picture data factory protocol."""

    def __call__(self, **fields: Unpack[PictureData]) -> PictureData:
        """Create instance of ``PictureData`` with overwritten fields."""


@pytest.fixture(scope='session')
def picture_data_factory(mf: Field) -> PictureDataFactory:
    """Returns factory for fake random data of a picture."""

    def factory(**fields: Unpack[PictureData]) -> PictureData:
        schema = Schema(
            schema=lambda: {
                'foreign_id': Random().randints(amount=1)[0],
                'url': mf('url'),
            },
            iterations=1,
        )

        return {
            **schema.create()[0],  # type: ignore[typeddict-item]
            **fields,
        }

    return factory


FavouritePictureFactory: TypeAlias = Callable[[User], FavouritePicture]


@pytest.fixture(scope='session')
def favourite_picture_factory(
    picture_data_factory: PictureDataFactory,
) -> FavouritePictureFactory:
    """Create a ``FavouritePicture`` directly in database."""

    def factory(user: User) -> FavouritePicture:
        return FavouritePicture.objects.create(
            **picture_data_factory(),
            user=user,
        )

    return factory


FavouritePictureAssertion: TypeAlias = Callable[[User, PictureData], None]


@pytest.fixture(scope='session')
def assert_picture_is_users_favourite() -> FavouritePictureAssertion:
    """Verify that provided picture is favourite in user's list."""

    def factory(user: User, picture: PictureData) -> None:
        rv = user.pictures.filter(foreign_id=picture['foreign_id'])
        assert rv.exists()

    return factory
