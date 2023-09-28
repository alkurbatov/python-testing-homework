import pytest
from django.shortcuts import render
from django.test import RequestFactory
from pytest_django.asserts import assertContains


@pytest.mark.django_db()
def test_base_template() -> None:
    """Test base template rendering."""
    page = render(RequestFactory().get('/'), 'common/_base.html')

    for element in ('footer', 'header'):
        assertContains(page, 'data-testid="{element}"'.format(element=element))


def test_messages():
    """Test messages template rendering."""
    page = render(RequestFactory().get('/'), 'common/includes/messages.html', {
        'messages': ['First', 'second'],
    })

    assertContains(page, 'data-testid="message"', 2)
