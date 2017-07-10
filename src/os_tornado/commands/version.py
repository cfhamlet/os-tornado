from __future__ import print_function
from os_tornado.commands import Command
import os_tornado


class VersionCommand(Command):
    """Command for showing version"""

    def short_desc(self):
        return 'Print os-tornado version.'

    def run(self, args, opts):
        print("os-tornado %s" % os_tornado.__version__)
