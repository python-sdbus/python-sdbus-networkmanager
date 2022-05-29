#!/usr/bin/env python
# SPDX-License-Identifier: LGPL-2.1-or-later

def test_version_attribute() -> None:
    """Test module.__version__ matching python setup.py --version"""
    from importlib import import_module
    from pathlib import PurePath
    from subprocess import check_output
    from sys import executable as python, path
    from unittest import TestCase

    module = import_module(f"sdbus_{PurePath(path[0]).name}.networkmanager")
    setup_version = check_output([python, "setup.py", "--version"])

    TestCase().assertEqual(module.__version__ + '\n', setup_version.decode())

if __name__ == "__main__":
    """Main function to run all tests when not run by pytest"""
    test_version_attribute()
