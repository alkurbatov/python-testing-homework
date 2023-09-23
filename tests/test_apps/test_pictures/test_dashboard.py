from typing import cast

import pytest
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db()
@pytest.mark.usefixtures('logged_in_user')
def test_render_dashboard_view(client: Client) -> None:
    """Test that correct template used to render pictures dashboard page."""
    response = cast(HttpResponse, client.get(reverse('pictures:dashboard')))

    assertTemplateUsed(
        response,
        'pictures/pages/dashboard.html',
    )
