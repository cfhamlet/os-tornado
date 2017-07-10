"""Base class for Scrapy commands"""
from optparse import OptionGroup

from os_tornado.exceptions import UsageError


def arglist_to_dict(arglist):
    """Convert a list of arguments like ['arg1=val1', 'arg2=val2', ...] to a
    dict
    """
    return dict(x.split('=', 1) for x in arglist)


class Command(object):

    def __init__(self, settings=None):
        self.settings = settings

    def syntax(self):
        """
        Command syntax (preferably one-line). Do not include command name.
        """
        return ""

    def short_desc(self):
        """
        A short description of the command
        """
        return ""

    def long_desc(self):
        """A long description of the command. Return short description when not
        available. It cannot contain newlines, since contents will be formatted
        by optparser which removes newlines and wraps text.
        """
        return self.short_desc()

    def help(self):
        """An extensive help for the command. It will be shown when using the
        "help" command. It can contain newlines, since not post-formatting will
        be applied to its contents.
        """
        return self.long_desc()

    def add_options(self, parser):
        """
        Populate option parse with options available for this command
        """
        group = OptionGroup(parser, "Global Options")
        group.add_option("-L", "--loglevel", metavar="LEVEL", default=None,
                         help="log level (default: %s)" % self.settings['LOG_LEVEL'])
        group.add_option("-s", "--settings", action="append", default=[], metavar="NAME=VALUE",
                         help="set/override setting (may be repeated)")

        parser.add_option_group(group)

    def process_options(self, args, opts):
        try:
            self.settings.update(arglist_to_dict(opts.settings))
        except ValueError:
            raise UsageError(
                "Invalid -s value, use -s NAME=VALUE", print_help=False)

        if opts.loglevel:
            self.settings.set('LOG_LEVEL', opts.loglevel)

    def run(self, args, opts):
        """
        Entry point for running commands
        """
        raise NotImplementedError
