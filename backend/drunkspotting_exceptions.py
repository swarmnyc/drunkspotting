#!/usr/bin/python
"""Exceptions throw by the server and kicked up by the gateway
"""


class NotFoundException(Exception):
    def moo(self):
        return 'moo'


class UnknownMethodException(Exception):
    def moo(self):
        return 'moo'


class AcccessDeniedException(Exception):
    def moo(self):
        return 'moo'
