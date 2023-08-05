# -*- coding: utf-8 -*-
"""Utility module

This is the place for utilities which will be used among the project.
"""


class Validator:

    @classmethod
    def verify_subdomain(cls, subdomain):
        if not subdomain:
            err_msg = "'subdomain' is required."
            raise AssertionError(err_msg)

        if not isinstance(subdomain, str):
            err_msg = "'subdomain' has to be a string."
            raise TypeError(err_msg)

    @classmethod
    def verify_system_type(cls, system_type):
        if not system_type:
            err_msg = "'system_type' is required."
            raise AssertionError(err_msg)

        if not isinstance(system_type, str):
            err_msg = "'system_type' has to be a string."
            raise TypeError(err_msg)

    @classmethod
    def verify_enabled(cls, enabled):
        if not isinstance(enabled, bool):
            err_msg = "'enabled' has to be a bool value."
            raise TypeError(err_msg)
