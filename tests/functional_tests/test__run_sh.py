from pathlib import Path
from tests.utils.virtualenv import Virtualenv
from typing import Tuple, Dict
import subprocess

def test__tests_pass(project: Tuple[Path, Dict[str, str]], virtualenv: Virtualenv):
    outdir, template_values = project
    env: Dict[str, str] = virtualenv.get_activated_env_vars()

    # same, but fail if subprocess exits with non-zero exit code
    subprocess.run(["bash", "run.sh", "install"], cwd=outdir, env=env, check=True)
    subprocess.run(["bash", "run.sh", "test"], cwd=outdir, env=env, check=True)
    