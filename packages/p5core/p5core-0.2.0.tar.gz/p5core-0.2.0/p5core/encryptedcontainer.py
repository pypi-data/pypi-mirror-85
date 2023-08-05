"""Management of encrypted container."""
from pathlib import Path
from shutil import copy, copytree
from tempfile import mkdtemp, mkstemp
from typing import final

from py7zr import SevenZipFile


class CompressionError(Exception):
    """Compression error during container management."""


class DecompressionError(Exception):
    """Decompression error during container management."""


_DEFAULT_PASSWORD: final = "«»()@+-/="


class EncryptedContainer:
    """Encrypted file container."""

    def __init__(self, path: Path, password: str = _DEFAULT_PASSWORD) -> None:
        """Create an empty container.

        Args:
            path (Path): Path of the archive
            password (str): Password for encryption. Defaults to "«»()@+-/="
        """
        self._path = path
        self._password = password
        if not path.exists():
            self._create_empty_container()

    def add(self, src: Path, dst: str) -> None:
        """Add content to container.

        Args:
            src (Path): Content to be added (file or directory)
            dst (str): Name in the container

        Raises:
            CompressionError: Something went wrong while adding content
        """
        extract_dir = self.extract(self._password)
        print("add in", extract_dir, ":", src)
        if not src.exists():
            raise CompressionError(msg="Given path doesn't exist")
        if src.is_file():
            print("    ", extract_dir / dst)
            copy(src, extract_dir / dst)
        elif src.is_dir():
            copytree(src, extract_dir / dst, dirs_exist_ok=True, copy_function=copy)

        with SevenZipFile(self._path, mode="w", password=self._password) as arc:
            arc.writeall(extract_dir, ".")

    def extract(self, password: str) -> Path:
        """Extract the archive into a directory. Return the path of it.

        Args:
            password (str): Password for decryption

        Raises:
            DecompressionError: Something went wrong while getting content

        Returns:
            Path: Path of the directory where the content is extracted
        """
        extract_dir = Path(mkdtemp(prefix="p5_"))
        try:
            with SevenZipFile(self._path, mode="r", password=password) as arc:
                arc.extractall(extract_dir)
        except Exception:
            # Don't give any hint on the caught exception
            raise DecompressionError()
        return extract_dir

    def _create_empty_container(self) -> None:
        with SevenZipFile(self._path, mode="w", password=self._password) as arc:
            fd, file_path = mkstemp(prefix="p5_")
            with open(fd, "wb") as tmp_file:
                tmp_file.write(b"www.lecalamar.fr")
            file_path = Path(file_path)
            arc.writeall(file_path, ".lecalamar")
            file_path.unlink()
