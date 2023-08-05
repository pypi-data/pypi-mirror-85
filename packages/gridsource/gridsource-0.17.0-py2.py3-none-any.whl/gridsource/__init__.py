# -*- coding: utf-8 -*-

"""Top-level package for GridSource."""

from gridsource.io import IOMixin
from gridsource.validation import ValidatorMixin

__author__ = """Nicolas Cordier"""
__email__ = "nicolas.cordier@numeric-gmbh.ch"
__version__ = "0.17.0"


class _Base:
    def __init__(self):
        self._data = {}
        possible_mixins_init = ("validator_mixin_init", "io_mixin_init")
        for f in possible_mixins_init:
            if hasattr(self, f):
                getattr(self, f)()


class Data(_Base, IOMixin, ValidatorMixin):
    pass


class ValidData(_Base, ValidatorMixin):
    pass


class IOData(_Base, IOMixin):
    pass
