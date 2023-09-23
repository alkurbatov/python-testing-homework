from typing import cast

import pytest
from django.http import HttpResponse
from django.test import Client
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db()
@pytest.mark.usefixtures('logged_in_user')
def test_render_index_view(client: Client) -> None:
    """Test that correct template used to render / page."""
    response = cast(HttpResponse, client.get('/'))

    assertTemplateUsed(
        response,
        'pictures/pages/index.html',
    )
