"""Fixture with a project folder populated by the cookiecutter template."""

from pathlib import Path

from pathlib import Path
import sys
from uuid import uuid4
from shutil import rmtree

THIS_DIR = Path(__file__).parent
PROJECT_ROOT_DIR = THIS_DIR / "../../"

sys.path.insert(0, str(PROJECT_ROOT_DIR))

import subprocess

import pytest
from typing import Dict
from copy import deepcopy
import json
from tempfile import TemporaryFile, TemporaryDirectory
from contextlib import contextmanager

from tests.consts import TEST_ARTIFACTS_DIR, PROJECT_ROOT_DIR


@contextmanager
def generate_temporary_project(
    template_values: Dict[str, str], cleanup_on_exit: bool = True
) -> Path:
    outdir = TEST_ARTIFACTS_DIR / str(uuid4())[:6]
    outdir.mkdir(parents=True, exist_ok=True)

    try:
        yield generate_project(outdir=outdir, template_values=template_values)
    finally:
        if cleanup_on_exit:
            rmtree(outdir)


def generate_project(outdir: Path, template_values: Dict[str, str]) -> Path:
    config_file_fpath: Path = make_cookiecutter_config_json_file(
        parent_dir=outdir,
        template_values=template_values,
    )
    cmd = [
        "cookiecutter",
        str(PROJECT_ROOT_DIR),
        "--no-input",
        "--config-file",
        str(config_file_fpath),
        "--output-dir",
        str(outdir),
        "--verbose"
    ]
    print(" ".join(cmd))
    subprocess.run(
        cmd,
        cwd=outdir,
    )


def make_cookiecutter_config_json_file(
    parent_dir: Path, template_values: Dict[str, str]
) -> Path:
    cookiecutter_conf_fpath = parent_dir / "cookiecutter.json"
    cookiecutter_conf_contents: str = template_values_to_cookiecutter_json(
        template_values
    )
    cookiecutter_conf_fpath.write_text(cookiecutter_conf_contents)
    return cookiecutter_conf_fpath


def template_values_to_cookiecutter_json(template_values: Dict[str, str]) -> str:
    json_contents = {"default_context": deepcopy(template_values)}
    return json.dumps(json_contents, indent=4)


if __name__ == "__main__":
    template_values = {
        "repo_name": "sample-repo",
        "package_import_name": "sample_package",
    }
    with generate_temporary_project(
        template_values=template_values, cleanup_on_exit=False
    ) as project_dir:
        ...
