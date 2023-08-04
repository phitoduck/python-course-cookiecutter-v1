from pathlib import Path
from tests.utils.virtualenv import Virtualenv
from typing import Tuple, Dict
import subprocess

def test__tests_pass_wheel_local(project: Tuple[Path, Dict[str, str]], virtualenv: Virtualenv):
    outdir, _ = project
    env: Dict[str, str] = virtualenv.get_activated_env_vars()

    # same, but fail if subprocess exits with non-zero exit code
    subprocess.run(["bash", f"{outdir}/run.sh", "clean"], cwd=outdir, env=env, check=True)
    subprocess.run(["bash", f"{outdir}/run.sh", "test:wheel-locally"], cwd=outdir, env=env, check=True)


def test__tests_pass(project: Tuple[Path, Dict[str, str]], virtualenv: Virtualenv):
    outdir, _ = project
    env: Dict[str, str] = virtualenv.get_activated_env_vars()

    # same, but fail if subprocess exits with non-zero exit code
    subprocess.run(["bash", f"{outdir}/run.sh", "clean"], cwd=outdir, env=env, check=True)
    subprocess.run(["bash", f"{outdir}/run.sh", "test"], cwd=outdir, env=env, check=True)


def test__linting_passes(project: Tuple[Path, Dict[str, str]], virtualenv: Virtualenv):
    """"""
    outdir, _ = project
    env: Dict[str, str] = virtualenv.get_activated_env_vars()

    # same, but fail if subprocess exits with non-zero exit code
    subprocess.run(["bash", f"{outdir}/run.sh", "clean"], cwd=outdir, env=env, check=True)
    subprocess.run(["bash", f"{outdir}/run.sh", "lint"], cwd=outdir, env=env, check=False)
    subprocess.run(["bash", f"{outdir}/run.sh", "lint:ci"], cwd=outdir, env=env, check=True)
