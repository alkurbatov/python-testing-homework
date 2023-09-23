import pytest

from server.apps.identity.models import User
from server.apps.pictures.infrastructure.django.forms import FavouritesForm


@pytest.mark.django_db()
def test_favourites_form_without_saving(
    logged_in_user: User,
) -> None:
    """Test favourite pictures form.

    If commit happens, the test throws.
    """
    form = FavouritesForm(user=logged_in_user)

    form.save(commit=False)
