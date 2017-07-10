"""The list command"""
from __future__ import print_function
from os_tornado.commands import Command
from os_tornado.component_manager import ComponentManager
from os_tornado.exceptions import UsageError


_TYPE = set(['ext', 'req', 'all'])


class ListCommand(Command):
    """Command for listing extensions and request handlers."""

    def syntax(self):
        return "[ext/req/all]"

    def short_desc(self):
        return "List available extensions and request handlers."

    def _show_ext(self, manager):
        exts = self.settings['EXTENSIONS']
        if not exts:
            print('No available extensions')
            return
        manager.load_extensions()
        print('Extensions:')
        for ext in manager.iter_extensions():
            print("  %-18s %s" %
                  (ext.name, '.'.join((ext.__module__, ext.__class__.__name__))))

    def _show_req(self, manager):
        handlers = self.settings['REQUEST_HANDLERS']
        if not handlers:
            print('No available request handlers')
            return
        manager.load_request_handlers()
        print('RequestHandlers:')
        for pattern, handler, _ in manager.iter_request_handlers():
            print("  %-18s %s" %
                  (pattern, '.'.join((handler.__module__, handler.__name__))))

    def run(self, args, opts):
        cm = _TYPE.intersection(args)
        if len(cm) <= 0:
            raise UsageError()
        if 'all' in cm:
            cm.remove('all')
            cm.update(['ext', 'req'])
        method = {'ext': self._show_ext, 'req': self._show_req}
        manager = ComponentManager(self.settings)
        for m in cm:
            method[m](manager)
            print('\n')
