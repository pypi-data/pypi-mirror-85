#!/usr/bin/env python3

"""Tests for `fcust` main module."""

import pytest

# import mock
import tempfile
from pathlib import Path, PurePath
from shutil import chown
from click.testing import CliRunner
from fcust.fcust import CommonFolder
from fcust import cli


class TestCommonFolder:
    def setup_class(cls):
        """
        Setting up the objects to test functionality.

        Note:
        User running the tests must be a member of group 'family'.
        """
        cls.folder = Path(tempfile.mkdtemp())
        # populate folder
        f1 = PurePath.joinpath(cls.folder, "file1.txt")
        with f1.open(mode="w") as fh:
            fh.write("file1")
        chown(f1, group="family")
        f1.chmod(0o40400)
        f2 = PurePath.joinpath(cls.folder, "file2.txt")
        with f2.open(mode="w") as fh:
            fh.write("file2")
        f4 = PurePath.joinpath(cls.folder, "folder")
        f4.mkdir()
        chown(f4, group="family")
        f4.chmod(0o40750)
        f3 = PurePath.joinpath(cls.folder, "folder", "file3.txt")
        with f3.open(mode="w") as fh:
            fh.write("file3")
        cls.group = cls.folder.group()
        cls.owner = cls.folder.owner()
        cls.o1 = f1
        cls.o2 = f4

    def test_init_folder_type(self):
        """
        Basic testing.
        """

        with pytest.raises(TypeError) as exc:
            test_path = "hi"
            CommonFolder(folder_path=test_path)

        assert str(exc.value) == (
            f"Expected PosixPath object instead of {type(test_path)}"
        )

    def test_init_folder_exists(self):
        """
        Basic testing.
        """

        with pytest.raises(FileNotFoundError) as exc:
            test_path = Path("nothere")
            CommonFolder(folder_path=test_path)

        assert str(exc.value) == (
            "Folder is expected to be present when the class is initialized."
        )

    def test_enforce_permissions(self):
        """
        Testing permision and group membership enforcement.
        """

        cf = CommonFolder(self.folder)
        assert cf.group == self.group

        cf.enforce_permissions()

        assert oct(self.o1.stat().st_mode)[-4:] == "0664"
        assert self.o1.group() == self.group
        assert oct(self.o2.stat().st_mode)[-4:] == "2775"
        assert self.o2.group() == self.group


class TestCommonFolderCLI:
    def setup_class(cls):
        """
        Setting up the objects to test functionality.

        Note:
        User running the tests must be a member of group 'family'.
        """
        cls.folder = Path(tempfile.mkdtemp())
        # populate folder
        f1 = PurePath.joinpath(cls.folder, "file1.txt")
        with f1.open(mode="w") as fh:
            fh.write("file1")
        chown(f1, group="family")
        f1.chmod(0o40400)
        f2 = PurePath.joinpath(cls.folder, "file2.txt")
        with f2.open(mode="w") as fh:
            fh.write("file2")
        f4 = PurePath.joinpath(cls.folder, "folder")
        f4.mkdir()
        chown(f4, group="family")
        f4.chmod(0o40750)
        f3 = PurePath.joinpath(cls.folder, "folder", "file3.txt")
        with f3.open(mode="w") as fh:
            fh.write("file3")
        cls.group = cls.folder.group()
        cls.owner = cls.folder.owner()
        cls.o1 = f1
        cls.o2 = f4

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main, ["run", str(self.folder)])
        assert result.exit_code == 0
        assert oct(self.o1.stat().st_mode)[-4:] == "0664"
        assert self.o1.group() == self.group
        assert oct(self.o2.stat().st_mode)[-4:] == "2775"
        assert self.o2.group() == self.group

        help_result = runner.invoke(cli.main, ["run", "--help"])
        assert help_result.exit_code == 0
        assert "--help  Show this message and exit." in help_result.output
        assert "Usage: main run [OPTIONS] FOLDER_PATH" in help_result.output
