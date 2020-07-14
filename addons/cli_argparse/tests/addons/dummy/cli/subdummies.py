# -*- coding: utf-8 -*-

from odoo.cli.command import Command

from ._base import SubdummiesCommandMixin


class Subdummies(SubdummiesCommandMixin, Command):

    def run_foo(self, env, options):
        self.print_args(env, options)

    def run_bar(self, env, options):
        self.print_args(env, options)
