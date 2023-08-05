#!/usr/bin/env python3

"""Tests for `fcust` service module."""

from pathlib import Path
from fcust.service import create_user_unit_path


class TestFcustService:
    def setup_class(cls):
        """
        Setting up the objects to test functionality.

        Note:
        User running the tests must be a member of group 'family'.
        """
        cls.home = Path.home()
        cls.exp_unit_path = str(cls.home) + "/.config/systemd/user/fcust.service"

    def test_create_user_unit_path(self):
        """(trivially test) unit path construction"""
        assert self.exp_unit_path == str(create_user_unit_path())
