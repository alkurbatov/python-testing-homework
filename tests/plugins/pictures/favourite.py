from typing import Callable, Protocol, TypeAlias, TypedDict, final

import pytest
from django_fakery import factory as fakery
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
                'foreign_id': mf('numeric.increment'),
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
def favourite_picture_factory() -> FavouritePictureFactory:
    """Create instance of ``FavouritePicture``."""

    def factory(user: User) -> FavouritePicture:
        rv = fakery.m(FavouritePicture)  # type: ignore[attr-defined]
        return rv(user=user)

    return factory


FavouritePictureAssertion: TypeAlias = Callable[[User, PictureData], None]


@pytest.fixture(scope='session')
def assert_picture_is_users_favourite() -> FavouritePictureAssertion:
    """Verify that provided picture is favourite in user's list."""

    def factory(user: User, picture: PictureData) -> None:
        rv = user.pictures.filter(foreign_id=picture['foreign_id'])
        assert rv.count() == 1

    return factory
