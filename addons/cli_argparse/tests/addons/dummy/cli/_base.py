# -*- coding: utf-8 -*-

import json

from odoo.addons.cli_argparse import (
    CommandMixin, SubcommandsMixin)


class DummyCommandMixin(CommandMixin):

    def run_cmd(self, env, options):
        print(
            json.dumps(
                dict(env=str(env) if env else None,
                     options=options.__dict__)))


class SubdummiesCommandMixin(SubcommandsMixin):

    def print_args(self, env, options):
        print(
            json.dumps(
                dict(env=str(env) if env else None,
                     options=options.__dict__)))
