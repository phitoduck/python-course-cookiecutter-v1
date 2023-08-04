import pytest
from tests.utils.project import generate_temporary_project
from typing import Tuple, Dict
from pathlib import Path
import subprocess


@pytest.fixture()
def project() -> Tuple[Path, Dict[str, str]]:
    template_values = {
        "repo_name": "sample-repo",
        "package_import_name": "sample_package",
    }
    with generate_temporary_project(
        template_values=template_values,
        cleanup_on_exit=True,
    ) as project_dir:
        subprocess.run(["git", "init"], cwd=project_dir, check=True)
        subprocess.run(["git", "add", "--all"], cwd=project_dir, check=True)
        subprocess.run(
            ["git", "commit", "-m", "first-commit-during-tests"],
            cwd=project_dir,
            check=True,
        )
        yield project_dir, template_values
