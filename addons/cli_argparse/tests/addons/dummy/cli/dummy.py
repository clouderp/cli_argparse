# -*- coding: utf-8 -*-

from odoo.cli.command import Command

from ._base import DummyCommandMixin


class Dummy(DummyCommandMixin, Command):
    pass
