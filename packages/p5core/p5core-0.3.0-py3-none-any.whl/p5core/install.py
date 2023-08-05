"""Root script for CI."""

import os
import importlib.resources as pkg_resources
from pathlib import Path


import p5core
from p5core.install_helpers import copy_file

workspace = os.environ.get("GITHUB_WORKSPACE")
if workspace:
    workspace = Path(workspace)
else:
    workspace = Path(".")


def install():
    """Installation entry point."""
    p5core.install_helpers.installation_directory = workspace

    with pkg_resources.path(p5core, "README_user.md") as file_path:
        copy_file(file_path, Path("README.md"))
