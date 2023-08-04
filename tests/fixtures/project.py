import pytest
from tests.utils.project import generate_temporary_project
from typing import Tuple, Dict
from pathlib import Path

@pytest.fixture(scope="session")
def project() -> Tuple[Path, Dict[str, str]]:
    template_values = {
        "repo_name": "sample-repo",
        "package_import_name": "sample_package",
    }
    with generate_temporary_project(
        template_values=template_values, cleanup_on_exit=False
    ) as project_dir:
        yield project_dir, template_values