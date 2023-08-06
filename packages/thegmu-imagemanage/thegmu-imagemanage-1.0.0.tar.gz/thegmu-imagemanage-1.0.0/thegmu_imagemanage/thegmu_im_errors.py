#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

    thegmu_im_errors.py
    ~~~~~~~~~~~~~~~~~~~

    Library of simple errors with only distinct names as a feature.

"""


class TheGMUImageManageError(Exception):
    """Base exception."""


class TheGMUImageManageBadCommandError(TheGMUImageManageError):
    """Command Exception."""


class TheGMUImageManageCatalogError(TheGMUImageManageError):
    """Catalog Exception"""


class TheGMUImageManageConvertError(TheGMUImageManageError):
    """Imagemagick format convert error."""
