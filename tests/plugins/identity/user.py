from datetime import date
from typing import Callable, Protocol, TypeAlias, TypedDict, final

import pytest
from django.test import Client
from mimesis.schema import Field, Schema
from typing_extensions import Unpack

from server.apps.identity.models import User


class UserData(TypedDict, total=False):
    """
    Represent the simplified user data that is required to create a new user.

    It does not include ``password``, because it is very special in django.
    """

    email: str
    first_name: str
    last_name: str
    date_of_birth: date
    address: str
    job_title: str
    phone: str


@final
class UserDataFactory(Protocol):  # type: ignore[misc]
    """User data factory protocol."""

    def __call__(self, **fields: Unpack[UserData]) -> UserData:
        """Create instance of ``UserData`` with overwritten fields."""


@pytest.fixture(scope='session')
def user_data_factory(mf: Field) -> UserDataFactory:
    """Returns factory for fake random data of a user."""

    def factory(**fields: Unpack[UserData]) -> UserData:
        schema = Schema(
            schema=lambda: {
                'email': mf('person.email'),
                'first_name': mf('person.first_name'),
                'last_name': mf('person.last_name'),
                'date_of_birth': mf('datetime.date'),
                'address': mf('address.city'),
                'job_title': mf('person.occupation'),
                'phone': mf('person.telephone'),
            },
            iterations=1,
        )

        return {
            **schema.create()[0],  # type: ignore[typeddict-item]
            **fields,
        }

    return factory


@final
class RegistrationData(UserData, total=False):
    """Represent the registration data that is required to create a new user."""

    password1: str
    password2: str


@final
class RegistrationDataFactory(Protocol):  # type: ignore[misc]
    """User data factory protocol."""

    def __call__(self, **fields: Unpack[RegistrationData]) -> RegistrationData:
        """Create instance of ``RegistrationData`` with overwritten fields."""


@pytest.fixture(scope='session')
def registration_data_factory(
    mf: Field,
    user_data_factory: UserDataFactory,
) -> RegistrationDataFactory:
    """Returns factory for fake random data for registration."""

    def factory(**fields: Unpack[RegistrationData]) -> RegistrationData:
        password = mf('password')  # by default passwords are equal
        user_data = user_data_factory()

        return {
            **user_data,
            **{'password1': password, 'password2': password},
            **fields,
        }

    return factory


@final
class LoginData(TypedDict, total=False):
    """Represent the login data that is required to authenticate a user."""

    username: str
    password: str


UserFactory: TypeAlias = Callable[[str], User]


@pytest.fixture()
def user_factory(
    user_data_factory: UserDataFactory,
) -> UserFactory:
    """Create a user directly in database."""
    def factory(password: str) -> User:
        return User.objects.create_user(
            **user_data_factory(),
            password=password,
        )

    return factory


@pytest.fixture()
def logged_in_user(
    mf: Field,
    client: Client,
    user_factory: UserFactory,
) -> User:
    """Provide authenticated user to be used in tests."""
    user = user_factory(mf('password'))
    client.force_login(user)

    return user


UserAssertion: TypeAlias = Callable[[str, UserData], None]


@pytest.fixture(scope='session')
def assert_correct_user() -> UserAssertion:
    """Verify that user with provided email exists and valid."""

    def factory(email: str, expected: UserData) -> None:
        user = User.objects.get(email=email)

        # Special fields:
        assert user.id
        assert user.is_active
        assert not user.is_superuser
        assert not user.is_staff

        # All other fields:
        for field_name, data_value in expected.items():
            assert getattr(user, field_name) == data_value

    return factory
