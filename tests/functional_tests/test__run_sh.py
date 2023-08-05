import subprocess
from pathlib import Path
from typing import (
    Dict,
    Tuple,
)

from tests.utils.virtualenv import Virtualenv


def test__tests_pass_wheel_local(project: Tuple[Path, Dict[str, str]], virtualenv: Virtualenv):
    """
    Test that the tests pass when run on a locally built wheel.

    Can catch issues such as binary files not being included in the wheel.
    """
    outdir, _ = project
    env: Dict[str, str] = virtualenv.get_activated_env_vars()

    # same, but fail if subprocess exits with non-zero exit code
    subprocess.run(["bash", "run.sh", "clean"], cwd=outdir, env=env, check=True)
    subprocess.run(["bash", "run.sh", "test:wheel-locally"], cwd=outdir, env=env, check=True)


def test__tests_pass(project: Tuple[Path, Dict[str, str]], virtualenv: Virtualenv):
    """Test that the tests pass in a generated project when run on the src/ folder."""
    outdir, _ = project
    env: Dict[str, str] = virtualenv.get_activated_env_vars()

    # same, but fail if subprocess exits with non-zero exit code
    subprocess.run(["bash", "run.sh", "clean"], cwd=outdir, env=env, check=True)
    subprocess.run(["bash", "run.sh", "test"], cwd=outdir, env=env, check=True)


def test__linting_passes(project: Tuple[Path, Dict[str, str]], virtualenv: Virtualenv):
    """
    Test that linting passes in a generated project.

    Note: we run linting twice, since we do not mind if automatically-fixable
    errors such as trailing whitespace make it through.

    This makes it easier
    to develop the template, because we often cannot lint the template files
    directly, e.g. when python files contain Jinja2 templating syntax making them
    syntactically invalid python files.
    """
    outdir, _ = project
    env: Dict[str, str] = virtualenv.get_activated_env_vars()

    # same, but fail if subprocess exits with non-zero exit code
    subprocess.run(["bash", "run.sh", "clean"], cwd=outdir, env=env, check=True)
    subprocess.run(["bash", "run.sh", "lint"], cwd=outdir, env=env, check=False)
    subprocess.run(["bash", "run.sh", "lint:ci"], cwd=outdir, env=env, check=True)
