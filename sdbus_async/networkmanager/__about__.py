# SPDX-License-Identifier: LGPL-2.1-or-later
"""Module providing package metadata such as __version__"""
#
# Rationale: It is common that python packages export package.__version__
#
# Usage:
# - sdbus_block/networkmanager/__about_.py symlinks here.
# - sdbus_block/networkmanager/__init__.py re-exports __version__.
# - sdbus_async/networkmanager/__init__.py re-exports __version__.
# - setup.py reads the varables into a dict and uses them for metadata
#   (it should not attempt to import this file directly)
#
# This is tested by tests/async/test_version_async.py for async and a symlink
# to it in tests/block (which tests sdbus_block.networkmanager.__version__)
#
# Other metadata like __author__, __url__ can be placed here
# and red by setup.py by (and other packages as well, like this):
#
# from sdbus_async.networkmanager import __about__ as sdbus_networkmanager
# print(sdbus_networkmanager.__version__, sdbus_networkmanager.__url__)
#
# This is only one of of many ways of sourcing the package version,
# but it is standard, fast(e.g. pkg_resources is slow), works also when packaged
# in archvies such as pyinstaller and does not require additional packages:
# https://packaging.python.org/en/latest/guides/single-sourcing-package-version/
#
# In case the project would switch to pyproject.toml and poetry, e.g.
# this plugin can be used to update the python module providing __version__:
# https://github.com/monim67/poetry-bumpversion

__version__ = '1.2.0'