import pytest
from django.test import Client
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db()
@pytest.mark.usefixtures('logged_in_user')
def test_render_index_view(client: Client) -> None:
    """Test that correct template used to render / page."""
    response = client.get('/')

    assertTemplateUsed(
        response,  # type: ignore[arg-type]
        'pictures/pages/index.html',
    )
