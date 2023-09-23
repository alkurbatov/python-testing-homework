import random
from unittest.mock import MagicMock

import pytest
from plugins.datagen import SEED_RAND_BITS, pytest_configure
from pytest_mock import MockerFixture


@pytest.fixture()
def last_seed() -> int:
    """Seed that was used in last test session."""
    return random.Random().getrandbits(SEED_RAND_BITS)


@pytest.fixture()
def config(
    mocker: MockerFixture,
    last_seed: int,
    randomly_seed: int | str,
) -> MagicMock:
    """Create mock instance of pytest.Config."""
    cfg = mocker.patch.object(pytest, 'Config')
    cfg.getoption.return_value = randomly_seed
    cfg.cache.get.return_value = last_seed
    return cfg


@pytest.mark.parametrize('randomly_seed', ['default'])
def test_pytest_configure_with_default(
    mocker: MockerFixture,
    config: MagicMock,
) -> None:
    """Test default behavior."""
    mocker.patch('random.Random.getrandbits', return_value=10)
    pytest_configure(config)

    assert config.option.randomly_seed == 10


@pytest.mark.parametrize('randomly_seed', ['last'])
def test_pytest_configure_with_last_seed(
    config: MagicMock,
    last_seed: int,
) -> None:
    """Test that last randomly seed can be used in ``pytest.Config``."""
    pytest_configure(config)

    assert config.option.randomly_seed == last_seed


@pytest.mark.parametrize('randomly_seed', [123])
def test_pytest_configure_with_specified_seed(
    config: MagicMock,
    randomly_seed: int,
) -> None:
    """Test that custom randomly seed can be used in ``pytest.Config``."""
    pytest_configure(config)

    assert config.option.randomly_seed == randomly_seed
