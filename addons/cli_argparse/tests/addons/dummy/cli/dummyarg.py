# -*- coding: utf-8 -*-

from odoo.cli.command import Command

from ._base import DummyCommandMixin


class DummyArg(DummyCommandMixin, Command):
    command_args = (
        DummyCommandMixin.command_args
        + (('somearg', ), ))
