"""
Command line
"""
from __future__ import print_function
import sys
import os
import optparse
import os_tornado
from os_tornado.exceptions import UsageError
from os_tornado.settings import Settings
from os_tornado.commands import Command
from os_tornado.utils.module_utils import iter_classes

ENVVAR = 'OS_TORNADO_SETTINGS_MODULE'


def _get_settings():
    settings = Settings()
    settings.update_from_module('os_tornado.settings.default_settings')
    if ENVVAR in os.environ:
        settings.update_from_module(os.environ.get(ENVVAR))
    return settings


def _get_commands_from_module(module, settings):
    d = {}
    for cmd in iter_classes(module, Command):
        cmd_name = cmd.__module__.split('.')[-1]
        d[cmd_name] = cmd(settings)
    return d


def _get_commands_dict(settings):
    cmds = _get_commands_from_module('os_tornado.commands', settings)
    cmds_module = settings['COMMANDS_MODULE']
    if cmds_module:
        cmds.update(_get_commands_from_module(cmds_module, settings))
    return cmds


def _pop_command_name(argv):
    for arg in argv[1:]:
        if not arg.startswith('-'):
            return arg


def _print_header(settings):
    print("os-tornado %s\n" % os_tornado.__version__)


def _print_commands(settings):
    _print_header(settings)
    print("Usage:")
    print("  %s <command> [options] [args]\n" % sys.argv[0])
    print("Available commands:")
    cmds = _get_commands_dict(settings)
    for cmdname, cmdclass in sorted(cmds.items()):
        print("  %-18s %s" % (cmdname, cmdclass.short_desc()))
    print()
    print('Use "%s <command> -h" to see more info about a command' %
          sys.argv[0])


def _print_unknown_command(settings, cmd_name):
    _print_header(settings)
    print("Unknown command: %s\n" % cmd_name)
    print('Use "%s" to see available commands' % sys.argv[0])


def _run_print_help(parser, func, *a, **kw):
    try:
        func(*a, **kw)
    except UsageError as e:
        if str(e):
            parser.error(str(e))
        if e.print_help:
            parser.print_help()
        sys.exit(2)


def execute(argv=None):
    argv = argv or sys.argv
    settings = _get_settings()
    cmds = _get_commands_dict(settings)
    cmd_name = _pop_command_name(argv)
    parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(),
                                   conflict_handler='resolve')
    if not cmd_name:
        _print_commands(settings)
        sys.exit(0)
    elif cmd_name not in cmds:
        _print_unknown_command(settings, cmd_name)
        sys.exit(2)
    cmd = cmds[cmd_name]
    parser.usage = "%s %s %s" % (argv[0], cmd_name, cmd.syntax())
    parser.description = cmd.long_desc()
    cmd.add_options(parser)
    opts, args = parser.parse_args(args=argv[2:])
    _run_print_help(parser, cmd.process_options, args, opts)
    _run_print_help(parser, cmd.run, args, opts)


if __name__ == '__main__':
    execute()
