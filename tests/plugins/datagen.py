import pytest
from mimesis.locales import Locale
from mimesis.schema import Field


@pytest.fixture(scope='session')
def mf() -> Field:
    """Random data provider."""
    return Field(locale=Locale.RU)
