"""The runserver command"""
from __future__ import print_function
from os_tornado.commands import Command
from os_tornado.component_manager import ComponentManager
from os_tornado.runner import Runner


class RunserverCommand(Command):
    """Command for starting server"""

    def short_desc(self):
        return "run server."

    def add_options(self, parser):
        super(RunserverCommand, self).add_options(parser)
        default_port = self.settings["PORT"]
        parser.add_option("-p", "--port", action="store", dest="port",
                          type=int, help="set listen port (default: %s)" % str(default_port))

    def process_options(self, args, opts):
        super(RunserverCommand, self).process_options(args, opts)
        if opts.port:
            self.settings["PORT"] = opts.port

    def run(self, args, opts):
        manager = ComponentManager(self.settings)
        runner = Runner(manager)
        runner.run()
