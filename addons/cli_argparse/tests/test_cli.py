# -*- coding: utf-8 -*-

from ._base import TestCLI


class TestCLIArgparse(TestCLI):

    def test_dummy_cmd_noargs(self):
        response = self._run('dummy')
        assert (
            response
            == {'env': None,
                'options': {
                    'dbname': None}})

    def test_dummy_cmd_arg(self):
        response = self._run('dummyarg', 'foo')
        assert (
            response
            == {'env': None,
                'options': {
                    'somearg': 'foo',
                    'dbname': None}})

    def test_dummy_cmd_db_noargs(self):
        response = self._run_with_db('dummy')
        assert response['env'].startswith(
            '<odoo.api.Environment object ')
        assert (
            response['options']
            == {'dbname': self.env.cr.dbname})

    def test_subdummies_cmd_noargs_foo(self):
        response = self._run('subdummies', 'foo')
        assert (
            response
            == {'env': None,
                'options': {
                    'subcommand': 'foo',
                    'dbname': None}})

    def test_subdummies_cmd_noargs_bar(self):
        response = self._run('subdummies', 'bar')
        assert (
            response
            == {'env': None,
                'options': {
                    'subcommand': 'bar',
                    'dbname': None}})

    def test_subdummies_cmd_arg_foo(self):
        response = self._run('subdummiesarg', 'foo', 'baz')
        assert (
            response
            == {'env': None,
                'options': {
                    'subcommand': 'foo',
                    'subarg': 'baz',
                    'dbname': None}})

    def test_subdummies_cmd_arg_bar(self):
        response = self._run('subdummiesarg', 'bar')
        assert (
            response
            == {'env': None,
                'options': {
                    'subcommand': 'bar',
                    'dbname': None}})

    def test_subdummies_complex_foo(self):
        response = self._run('subdummiescomplex', 'foo', 'baz')
        assert (
            response
            == {'env': None,
                'options': {
                    'subcommand': 'foo',
                    'subarg': ['baz'],
                    'ex': None,
                    'dbname': None}})

    def test_subdummies_complex_bar(self):
        response = self._run('subdummiescomplex', 'bar')
        assert (
            response
            == {'env': None,
                'options': {
                    'subcommand': 'bar',
                    'otherarg': 'z-e-d',
                    'zed': None,
                    'dbname': None}})

    def test_subdummies_complex_foo_args(self):
        response = self._run(
            'subdummiescomplex', 'foo',
            'baz', 'x', 'y', 'z',
            '-x', 'excellent')
        assert (
            response
            == {'env': None,
                'options': {
                    'subcommand': 'foo',
                    'subarg': ['baz', 'x', 'y', 'z'],
                    'ex': 'excellent',
                    'dbname': None}})

    def test_subdummies_complex_bar_arg(self):
        response = self._run('subdummiescomplex', 'bar', 'baz')
        assert (
            response
            == {'env': None,
                'options': {
                    'subcommand': 'bar',
                    'otherarg': 'baz',
                    'zed': None,
                    'dbname': None}})

    def test_subdummies_complex_bar_args(self):
        response = self._run(
            'subdummiescomplex', 'bar',
            'baz',
            '--zzz', 'ZEDS')
        assert (
            response
            == {'env': None,
                'options': {
                    'subcommand': 'bar',
                    'otherarg': 'baz',
                    'zed': 'ZEDS',
                    'dbname': None}})

    def test_subdummies_complex_foo_args_env(self):
        response = self._run_with_db(
            'subdummiescomplex', 'foo',
            'baz', 'x', 'y', 'z',
            '-x', 'excellent')
        assert response['env'].startswith(
            '<odoo.api.Environment object ')
        assert (
            response['options']
            == {'subcommand': 'foo',
                'subarg': ['baz', 'x', 'y', 'z'],
                'ex': 'excellent',
                'dbname': self.env.cr.dbname})

    def test_subdummies_complex_bar_args_env(self):
        response = self._run_with_db(
            'subdummiescomplex', 'bar',
            'baz',
            '--zzz', 'ZEDS')
        assert response['env'].startswith(
            '<odoo.api.Environment object ')
        assert (
            response['options']
            == {'subcommand': 'bar',
                'otherarg': 'baz',
                'zed': 'ZEDS',
                'dbname': self.env.cr.dbname})
