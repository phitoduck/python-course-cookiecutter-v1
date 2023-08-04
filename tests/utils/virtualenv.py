from dataclasses import dataclass
from pathlib import Path
from contextlib import contextmanager
from tempfile import TemporaryDirectory

from pathlib import Path
import venv
import os
from typing import Dict, Type, Optional, List
import subprocess


@dataclass
class Virtualenv:
    directory: Path

    def get_activated_env_vars(self) -> Dict[str, str]:
        env: Dict[str, str] = os.environ.copy()
        env["VIRTUAL_ENV"] = str(self.directory)
        env["PATH"] = str(self.directory / "bin") + ":" + env["PATH"]
        return env

    @classmethod
    @contextmanager
    def create(cls: Type["Virtualenv"], parent_dir: Path, cleanup_on_exit: bool = True) -> "Virtualenv":
        """
        Create a virtualenv at `{parent_dir}/venv` or `{parent_dir}/<random>/venv` if `cleanup_on_exit` is True.

        :param parent_dir: directory where a folder called `venv` will be created (or `<random>/venv`; see `cleanup_on_exit`)
        :param cleanup_on_exit: if `True`, the virtualenv will be deleted when the context manager exits.
        """
        venv_dir = Path(parent_dir) / "venv"
        temp_dir: Optional[TemporaryDirectory] = None
        if cleanup_on_exit:
            temp_dir = TemporaryDirectory(dir=parent_dir)
            venv_dir = Path(temp_dir.name) / "venv"

        try:
            # create the venv
            venv_dir.mkdir(parents=True, exist_ok=True)
            venv.create(
                clear=False, # delete contents of venv if already present
                with_pip=True, # ensure pip is installed inside the venv
                system_site_packages=False, # whether to use packages in system python
                env_dir=venv_dir, # where to create the venv
            )
            virtualenv = cls(directory=venv_dir)
            yield virtualenv
        finally:
            if cleanup_on_exit:
                temp_dir.cleanup()
