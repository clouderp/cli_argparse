# -*- coding: utf-8 -*-

from odoo.cli.command import Command

from ._base import SubdummiesCommandMixin


class SubdummiesComplex(SubdummiesCommandMixin, Command):
    subcommand_args = (
        ('foo',
         (('subarg',
           (('nargs', '+'), )),
          ('-x', '--xxx',
           (('dest', 'ex'), )))),
        ('bar',
         (('otherarg',
           (('default', 'z-e-d'),
            ('nargs', '?'))),
          ('-z', '--zzz',
           (('dest', 'zed'), )))))

    def run_foo(self, env, options):
        self.print_args(env, options)

    def run_bar(self, env, options):
        self.print_args(env, options)
