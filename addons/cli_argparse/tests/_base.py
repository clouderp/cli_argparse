# -*- coding: utf-8 -*-

import json
import os
import subprocess

from odoo.tests.common import SavepointCase


class TestCLI(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestCLI, cls).setUpClass()

    @property
    def _db_args(self):
        db = self.env.registry._db.dsn
        return [
            '-d', self.env.cr.dbname,
            '--db_host', db['host'],
            '--db_password', db['password'],
            '--log-level=critical']

    @property
    def _odoo_cmd(self):
        paths = (
            '%s,%s/addons'
            % (os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(__file__)))),
               os.path.dirname(__file__)))
        return ('odoo', '--addons-path=%s' % paths)

    def _run(self, *args):
        result = subprocess.getoutput(
            ' '.join(list(self._odoo_cmd + args)))
        return json.loads(result)

    def _run_with_db(self, *args):
        return self._run(
            *args + tuple(self._db_args))
