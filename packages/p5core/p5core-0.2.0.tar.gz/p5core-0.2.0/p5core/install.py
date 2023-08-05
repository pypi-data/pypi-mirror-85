"""Root script for CI."""

import os
from pathlib import Path

import p5core.install_helpers
from p5core.install_helpers import copy_file

workspace = os.environ.get("GITHUB_WORKSPACE")
if workspace:
    workspace = Path(workspace)
else:
    workspace = Path(".")


def install():
    """Installation entry point."""
    p5core.install_helpers.installation_directory = workspace

    copy_file(Path("README_user.md"), Path("README.md"))
