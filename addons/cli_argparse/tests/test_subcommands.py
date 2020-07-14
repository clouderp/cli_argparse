# -*- coding: utf-8 -*-

from unittest.mock import MagicMock, patch, PropertyMock

from odoo import exceptions
from odoo.tests.common import SavepointCase

from odoo.addons.cli_argparse import SubcommandsMixin


class ExampleSubcommands(SubcommandsMixin):
    """Example arg parsing command"""
    name = 'example-subcommands'


class TestSubcommands(SavepointCase):

    def _command(self):
        return ExampleSubcommands()

    def test_parse_args_no_sub(self):
        command = self._command()

        class _object(object):
            pass

        args = _object()
        _parsed = _object()
        _parsed.subcommand = None
        subargs = _object()
        subargs.__dict__ = dict(a=1, b=2, c=3)
        command.parse_subcommand_args = MagicMock(
            return_value=(subargs, 'REMAINING_SUBARGS'))
        command._extract_odoo_args = MagicMock(
            return_value=(
                'EXTRACTED_ODOO_ARGS',
                'EXTRACTED_ARGS'))
        command._parser = MagicMock(new_callable=PropertyMock)
        command._parser.parse_known_args = MagicMock(
            return_value=(_parsed, "REMAINING_ARGS"))
        command._append_odoo_args = MagicMock(
            return_value="APPENDED_ODOO_ARGS")
        newargs, remaining = command.parse_args(args)
        assert (
            newargs.__dict__
            == {'subcommand': None})
        assert newargs is _parsed
        assert remaining == "APPENDED_ODOO_ARGS"
        assert not command.parse_subcommand_args.called
        assert (
            list(command._extract_odoo_args.call_args)
            == [(args,), {}])
        assert (
            list(command._parser.parse_known_args.call_args)
            == [('EXTRACTED_ARGS',), {}])
        assert (
            list(command._append_odoo_args.call_args)
            == [('REMAINING_ARGS', 'EXTRACTED_ODOO_ARGS'), {}])

    def test_parse_args_sub(self):
        command = self._command()

        class _object(object):
            pass

        args = _object()
        _parsed = _object()
        _parsed.subcommand = 'SUBCOMMAND'
        subargs = _object()
        subargs.__dict__ = dict(a=1, b=2, c=3)
        command.parse_subcommand_args = MagicMock(
            return_value=(subargs, 'REMAINING_SUBARGS'))
        command._extract_odoo_args = MagicMock(
            return_value=(
                'EXTRACTED_ODOO_ARGS',
                'EXTRACTED_ARGS'))
        command._parser = MagicMock(new_callable=PropertyMock)
        command._parser.parse_known_args = MagicMock(
            return_value=(_parsed, "REMAINING_ARGS"))
        command._append_odoo_args = MagicMock(
            return_value="APPENDED_ODOO_ARGS")

        newargs, remaining = command.parse_args(args)

        assert (
            newargs.__dict__
            == {'subcommand': 'SUBCOMMAND',
                'a': 1, 'b': 2, 'c': 3})
        assert newargs is _parsed
        assert remaining == "APPENDED_ODOO_ARGS"
        assert (
            list(command.parse_subcommand_args.call_args)
            == [('SUBCOMMAND', 'REMAINING_ARGS'), {}])
        assert (
            list(command._extract_odoo_args.call_args)
            == [(args,), {}])
        assert (
            list(command._parser.parse_known_args.call_args)
            == [('EXTRACTED_ARGS',), {}])
        assert (
            list(command._append_odoo_args.call_args)
            == [('REMAINING_SUBARGS', 'EXTRACTED_ODOO_ARGS'), {}])

    def test_parse_subcommand_args(self):
        command = self._command()
        command.add_arguments = MagicMock()
        subcommand = "SUBCOMMAND"
        args = object()
        command.subcommand_args = (
            (subcommand, 'SUBCOMMAND_ARGS'), )

        with patch('odoo.addons.cli_argparse.command.argparse') as argp_mock:
            result = command.parse_subcommand_args(subcommand, args)

        arg_parser = argp_mock.ArgumentParser.return_value
        assert (
            result
            is arg_parser.parse_known_args.return_value)
        assert (
            list(arg_parser.parse_known_args.call_args)
            == [(args, ), {}])
        assert (
            list(command.add_arguments.call_args)
            == [(arg_parser, 'SUBCOMMAND_ARGS'), {}])

    def test_parse_subcommand_noargs(self):
        command = self._command()
        command.add_arguments = MagicMock()
        subcommand = "SUBCOMMAND"
        args = object()
        command.subcommand_args = (
            (subcommand, 'SUBCOMMAND_ARGS'), )

        with patch('odoo.addons.cli_argparse.command.argparse') as argp_mock:
            result = command.parse_subcommand_args("NOT SUBCOMMAND", args)

        arg_parser = argp_mock.ArgumentParser.return_value
        assert (
            result
            is arg_parser.parse_known_args.return_value)
        assert (
            list(arg_parser.parse_known_args.call_args)
            == [(args, ), {}])
        assert (
            list(command.add_arguments.call_args)
            == [(arg_parser, ()), {}])

    def test_parse_subcommand_run_cmd(self):
        command = self._command()
        command.run_foo_bar = MagicMock(return_value="RESULT")

        class _object(object):
            pass

        parsed = _object()
        parsed.subcommand = 'foo_bar'
        env = object()

        assert (
            command.run_cmd(env, parsed)
            == "RESULT")

        assert (
            list(command.run_foo_bar.call_args)
            == [(env, parsed), {}])

    def test_parse_subcommand_run_cmd_hyphen(self):
        command = self._command()
        command.run_foo_bar = MagicMock(return_value="RESULT")

        class _object(object):
            pass

        parsed = _object()
        parsed.subcommand = 'foo-bar'
        env = object()

        assert (
            command.run_cmd(env, parsed)
            == "RESULT")

        assert (
            list(command.run_foo_bar.call_args)
            == [(env, parsed), {}])

    def test_parse_subcommand_run_cmd_missing(self):
        command = self._command()
        command.run_foo_bar = MagicMock(return_value="RESULT")

        class _object(object):
            pass

        parsed = _object()
        parsed.subcommand = 'foo-bar-baz'
        env = object()

        error = None
        result = None

        try:
            result = command.run_cmd(env, parsed)
        except exceptions.Warning as err:
            error = err

        assert result is None
        assert not command.run_foo_bar.called
        assert (
            str(error)
            == "('Unrecognized command: foo-bar-baz', '')")
