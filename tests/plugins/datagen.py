import random
from typing import Final

import pytest
from mimesis.locales import Locale
from mimesis.schema import Field

SEED_RAND_BITS: Final = 32


def pytest_configure(config: pytest.Config) -> None:
    """Create or restore random value to be used as seed during tests."""
    seed_value = config.getoption('randomly_seed')
    default_seed = random.Random().getrandbits(SEED_RAND_BITS)

    if seed_value == 'last':
        seed = config.cache.get(  # type: ignore[union-attr]
            'randomly_seed',
            default_seed,
        )
    elif seed_value == 'default':
        seed = default_seed
    else:
        seed = seed_value

    config.cache.set('randomly_seed', seed)  # type: ignore[union-attr]

    config.option.randomly_seed = seed


@pytest.fixture(scope='session')
def mf() -> Field:
    """Random data provider."""
    return Field(locale=Locale.RU)
