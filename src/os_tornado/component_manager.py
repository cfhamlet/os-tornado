"""Component Manager"""
from os_tornado.extension import ExtensionManager
from os_tornado.request_handler_manager import RequestHandlerManager


class ComponentManager(object):
    """Component Manager

    Access to extensions and request handlers
    """
    def __init__(self, settings):
        self._settings = settings
        self._ext_manager = ExtensionManager(self)
        self._request_handler_manager = RequestHandlerManager(self)

    def load_extensions(self):
        self._ext_manager.load()

    def load_request_handlers(self):
        self._request_handler_manager.load()

    def get_extension(self, name):
        return self._ext_manager.get_extension(name)

    @property
    def settings(self):
        return self._settings

    def iter_extensions(self):
        return self._ext_manager.iter_extensions()

    def iter_request_handlers(self):
        return self._request_handler_manager.iter_handlers()

    def get_all_request_handlers(self):
        return self._request_handler_manager.get_all_handlers()

    def setup_extensions(self):
        self._ext_manager.setup()

    def cleanup_extensions(self):
        self._ext_manager.cleanup()

    def run_extensions(self):
        self._ext_manager.run()
