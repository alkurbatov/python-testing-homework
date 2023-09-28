import json
from typing import TypeAlias

import httpretty
import pytest
from httpretty.core import HTTPrettyRequest

from server.apps.identity.infrastructure.services.placeholder import LeadUpdate
from server.apps.identity.models import User

HTTPHeaders: TypeAlias = dict[str, str]


def verify_update_user_request(
    request: HTTPrettyRequest,
    _url: str,
    headers: HTTPHeaders,
) -> tuple[int, HTTPHeaders, str]:
    """Verify request body and return fake result."""
    body = json.loads(request.body)

    assert body['birthday'] == ''

    headers['Content-Type'] = 'application/json'
    return (200, headers, '{"id": 1}')


@pytest.mark.django_db()
@httpretty.activate(allow_net_connect=False)  # type: ignore[misc]
def test_lead_update_without_date_of_birth(
    logged_in_user: User,
) -> None:
    """Test update of user without date_of_birth."""
    httpretty.register_uri(
        httpretty.PATCH,
        'https://farfaraway.com/users/{id}'.format(id=logged_in_user.lead_id),
        body=verify_update_user_request,
    )

    logged_in_user.date_of_birth = None
    sut = LeadUpdate('https://farfaraway.com', 5)

    sut(user=logged_in_user)
