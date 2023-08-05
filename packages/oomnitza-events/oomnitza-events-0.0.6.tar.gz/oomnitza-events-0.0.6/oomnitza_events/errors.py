# -*- coding: utf-8 -*-
"""Errors module

This module defines custom exceptions for the project.
"""


class Error(Exception):
    """Base class for exceptions in this project."""


class InvalidCredentialsError(Error):
    """Exception raised for missing required credentials info."""


class InvalidDatabaseInfoError(Error):
    """Exception raised for missing required db config info."""


class InvalidTrackersError(Error):
    """Exception raised for invalid tracker."""


class InvalidPropertiesError(Error):
    """Exception raised for missing required fields or incorrect data type."""
