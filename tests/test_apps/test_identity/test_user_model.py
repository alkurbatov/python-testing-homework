import pytest
from mimesis.schema import Field
from plugins.identity.user import UserDataFactory

from server.apps.identity.models import User


@pytest.mark.django_db()
def test_invalid_user_creation(
    mf: Field,
    user_data_factory: UserDataFactory,
) -> None:
    """Test that ``User`` model cannot be created with invalid data."""
    user_data = user_data_factory(email='', password=mf('password'))

    with pytest.raises(ValueError, match='Users must have an email address'):
        User.objects.create_user(**user_data)
