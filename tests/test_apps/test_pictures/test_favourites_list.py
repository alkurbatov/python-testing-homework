import pytest
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db()
@pytest.mark.usefixtures('logged_in_user')
def test_render_favourites_pictures_view(client: Client) -> None:
    """Test that correct template used to render favourites pictures page."""
    response = client.get(reverse('pictures:favourites'))

    assertTemplateUsed(
        response,  # type: ignore[arg-type]
        'pictures/pages/favourites.html',
    )
