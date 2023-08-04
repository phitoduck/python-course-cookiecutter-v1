import pytest
from typing import Tuple, Dict
from pathlib import Path
import subprocess

from tests.utils.virtualenv import Virtualenv
from tests.consts import TEST_ARTIFACTS_DIR


@pytest.fixture()
def virtualenv(project: Tuple[Path, Dict[str, str]]) -> Virtualenv:
    outdir, _ = project
    with Virtualenv.create(
        parent_dir=TEST_ARTIFACTS_DIR,
        cleanup_on_exit=True,
    ) as virtualenv:
        env: Dict[str, str] = virtualenv.get_activated_env_vars()
        subprocess.run(["bash", f"{outdir}/run.sh", "install"], cwd=outdir, env=env, check=True)
        yield virtualenv
