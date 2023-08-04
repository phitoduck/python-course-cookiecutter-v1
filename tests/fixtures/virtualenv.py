import pytest
from tests.utils.virtualenv import Virtualenv
from tests.consts import TEST_ARTIFACTS_DIR


@pytest.fixture(scope="session")
def virtualenv() -> Virtualenv:
    with Virtualenv.create(
        parent_dir=TEST_ARTIFACTS_DIR,
        cleanup_on_exit=False,
    ) as virtualenv:
        yield virtualenv
