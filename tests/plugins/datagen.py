import pytest
from mimesis.locales import Locale
from mimesis.random import Random
from mimesis.schema import Field


@pytest.fixture(scope='session')
def seed() -> int:
    """Create random value to be used as seed in mimesis."""
    max_int = 1000000
    return Random().randint(a=1, b=max_int)


@pytest.fixture(scope='session')
def mf(seed: int) -> Field:
    """Random data provider."""
    return Field(locale=Locale.RU, seed=seed)
