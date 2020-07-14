# -*- coding: utf-8 -*-

from collections import OrderedDict
from unittest.mock import MagicMock, patch, PropertyMock

from odoo import SUPERUSER_ID
from odoo.tests.common import SavepointCase

from odoo.addons.cli_argparse import CommandMixin


class ExampleCommand(CommandMixin):
    """Example arg parsing command"""
    name = 'example-command'


class TestCommand(SavepointCase):

    def _command(self):
        return ExampleCommand()

    def test_parser(self):
        command = self._command()
        command.add_arguments = MagicMock()
        parser = command.parser
        assert (
            parser.prog
            == 'odoo example-command')
        assert (
            parser.description
            == 'Example arg parsing command')
        assert (
            list(command.add_arguments.call_args)
            == [(parser, ), {}])
        command.add_arguments.reset_mock()
        assert command.parser is parser
        assert not command.add_arguments.called

    def test_add_arguments(self):
        command = self._command()
        parser = MagicMock()
        command.add_arguments(parser)
        assert (
            list(list(c) for c in parser.add_argument.call_args_list)
            == [[('--database', '-d'),
                 {'dest': 'dbname',
                  'type': str}]])
        parser.reset_mock()

        extra_args = (
            ('--foo', '-f',
             (('dest', 'foox'),
              ('type', list))), )
        command.command_args = (
            CommandMixin.command_args
            + extra_args)
        command.add_arguments(parser)
        assert (
            list(list(c) for c in parser.add_argument.call_args_list)
            == [[('--database', '-d'),
                 {'dest': 'dbname',
                  'type': str}],
                [('--foo', '-f'),
                 {'dest': 'foox',
                  'type': list}]])
        parser.reset_mock()

        extra_args = (
            ('--bar', '-b'), )
        command.command_args = (
            CommandMixin.command_args
            + extra_args)
        command.add_arguments(parser)
        assert (
            list(list(c) for c in parser.add_argument.call_args_list)
            == [[('--database', '-d'),
                 {'dest': 'dbname',
                  'type': str}],
                [('--bar', '-b'), {}]])

    def test_parse_args(self):
        command = self._command()
        args = ["ARG1", "ARG2", "ARG3"]
        command._extract_odoo_args = MagicMock(
            return_value=(
                'EXTRACTED_ODOO_ARGS',
                'EXTRACTED_ARGS'))
        command._parser = MagicMock(new_callable=PropertyMock)
        command._parser.parse_known_args = MagicMock(
            return_value=("PARSED_ARGS", "REMAINING_ARGS"))
        command._append_odoo_args = MagicMock(
            return_value="APPENDED_ODOO_ARGS")
        newargs, remaining = command.parse_args(args)
        assert newargs == "PARSED_ARGS"
        assert remaining == "APPENDED_ODOO_ARGS"
        assert (
            list(command._extract_odoo_args.call_args)
            == [(['ARG1', 'ARG2', 'ARG3'],), {}])
        assert (
            list(command._parser.parse_known_args.call_args)
            == [('EXTRACTED_ARGS',), {}])
        assert (
            list(command._append_odoo_args.call_args)
            == [('REMAINING_ARGS', 'EXTRACTED_ODOO_ARGS'), {}])

    def test_run(self):
        command = self._command()
        command.parse_args = MagicMock(
            return_value=(
                "PARSED_ARGS",
                "REMAINING"))
        command._run_with_env = MagicMock()
        with patch('odoo.addons.cli_argparse.command.service') as service_mock:
            with patch('odoo.addons.cli_argparse.command.tools') as tools_mock:
                command.run(["RUN", "ARGS"])
        assert (
            list(service_mock.server.start.call_args)
            == [(), {'preload': [], 'stop': True}])
        assert (
            list(tools_mock.config.parse_config.call_args)
            == [('REMAINING',), {}])
        assert (
            list(command.parse_args.call_args)
            == [(['RUN', 'ARGS'],), {}])
        assert (
            list(command._run_with_env.call_args)
            == [('PARSED_ARGS',), {}])

    def test_append_odoo_args(self):
        command = self._command()
        result = command._append_odoo_args(
            ["a", "b", "c"],
            OrderedDict((("d", 1), ("e", 2), ("f", 3))))
        assert result == ['a', 'b', 'c', 'd', 1, 'e', 2, 'f', 3]

    def test_extract_odoo_args(self):
        command = self._command()
        command._odoo_args = ('d', 'e', 'f')
        odoo_args, args = command._extract_odoo_args(
            ['a', 'b', 'c', 'd', 1, 'e', 2, 'f', 3])
        assert args == ['a', 'b', 'c']
        assert (
            list(odoo_args.keys())
            == ['d', 'e', 'f'])
        assert (
            list(odoo_args.values())
            == [1, 2, 3])

    def test_run_with_env_nodb(self):
        command = self._command()
        command.run_cmd = MagicMock()
        parsed = object()
        api = 'odoo.addons.cli_argparse.command.api'
        registry = 'odoo.addons.cli_argparse.command.registry'
        with patch(api) as api_mock:
            with patch(registry) as registry_mock:
                command._run_with_env(parsed)
        assert not api_mock.Environment.manage.called
        assert not registry_mock.called
        assert (
            list(command.run_cmd.call_args)
            == [(None, parsed),
                {}])

    def test_run_with_env_db_unset(self):
        command = self._command()
        command.run_cmd = MagicMock()

        class _object(object):
            pass

        parsed = _object()
        parsed.dbname = None
        api = 'odoo.addons.cli_argparse.command.api'
        registry = 'odoo.addons.cli_argparse.command.registry'
        with patch(api) as api_mock:
            with patch(registry) as registry_mock:
                command._run_with_env(parsed)
        assert not api_mock.Environment.manage.called
        assert not registry_mock.called
        assert (
            list(command.run_cmd.call_args)
            == [(None, parsed),
                {}])

    def test_run_with_env(self):
        command = self._command()
        command.run_cmd = MagicMock()

        class _object(object):
            pass

        parsed = _object()
        parsed.dbname = 'somedb'
        api = 'odoo.addons.cli_argparse.command.api'
        registry = 'odoo.addons.cli_argparse.command.registry'
        with patch(api) as api_mock:
            with patch(registry) as registry_mock:
                command._run_with_env(parsed)
        assert api_mock.Environment.manage.called
        assert api_mock.Environment.manage.return_value.__enter__.called
        assert api_mock.Environment.manage.return_value.__exit__.called
        assert (
            list(registry_mock.call_args)
            == [('somedb',), {}])
        assert registry_mock.return_value.cursor.called
        _cursor = registry_mock.return_value.cursor.return_value
        cursor = _cursor.__enter__.return_value
        environment = api_mock.Environment.return_value
        _env = environment.__getitem__
        assert (
            list(_env.call_args)
            == [('res.users',), {}])
        assert (
            list(list(c) for c in api_mock.Environment.call_args_list)
            == [[(cursor,
                  SUPERUSER_ID,
                  {}),
                 {}],
                [(cursor,
                  SUPERUSER_ID,
                  _env.return_value.context_get.return_value),
                 {}]])
        assert (
            list(command.run_cmd.call_args)
            == [(environment, parsed),
                {}])
        assert cursor.rollback.called
