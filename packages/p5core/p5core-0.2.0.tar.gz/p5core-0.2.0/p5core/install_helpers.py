"""Helpers for the installation procedure."""
import shutil
from pathlib import Path
from typing import Optional

from p5core.html import Tag

installation_directory: Path = Path(".")
source_directory: Path = Path(".")


def write_html(tag: Tag, path: Path):
    """Write an HTML tag in a file.

    Args:
        tag (Tag): HTML tag to write
        path (Path): path of the file to write

    Raises:
        TypeError: path is not a pathlib.Path
    """
    if not isinstance(path, Path):
        raise TypeError("path is not a pathlib.Path")
    with open(path, "w", encoding="utf-8") as writer:
        writer.write(str(tag))


def copy_file(src: Path, dst: Optional[Path] = None):
    """Copy a file in another file.

    Args:
        src (Path): source file
        dst (Optional[Path]): destination file, same path as src if not provided

    Raises:
        TypeError: Provided paths are not pathlib.Path
        ValueError: Provided paths are not relative
    """
    if not isinstance(src, Path):
        raise TypeError("src is not a pathlib.Path")
    if src.is_absolute():
        raise ValueError("Source path must be relative to exercice directory")

    if dst is None:
        dst = src
    elif not isinstance(dst, Path):
        raise TypeError("dst is not a pathlib.Path")
    elif dst.is_absolute():
        raise ValueError("Destination path must be relative to installation directory")

    # TODO créer le dossier destination s'il n'existe pas
    shutil.copy(source_directory / src, installation_directory / dst)
