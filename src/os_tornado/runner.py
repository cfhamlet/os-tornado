import logging
import tornado
from tornado.autoreload import add_reload_hook
from os_tornado.log import configure_logging
from os_tornado.settings import get_tornado_app_settings, get_tornado_server_settings
from os_tornado.utils.signal_utils import install_shutdown_handlers


class Runner(object):
    def __init__(self, manager):
        self._manager = manager
        self._logger = logging.getLogger('Runner')
        install_shutdown_handlers(self._cleanup_and_stop)
        add_reload_hook(self._cleanup)

    @property
    def settings(self):
        return self._manager.settings

    def _cleanup_and_stop(self, signum, frame):
        self._logger.debug('Recieve stop signal %d', signum)
        self._cleanup()
        tornado.ioloop.IOLoop.current().add_callback_from_signal(
            self._do_stop, signum, frame)

    def _cleanup(self):
        self._logger.info('[CLEANUP] Extensions')
        self._manager.cleanup_extensions()

    def _do_stop(self, signum, frame):
        self._logger.info('stop')
        tornado.ioloop.IOLoop.current().stop()

    def run(self):
        self.settings.freeze()
        configure_logging(self.settings)
        self._logger.info('[LOAD] extensions')
        self._manager.load_extensions()
        self._logger.info('[SETUP] extensions')
        self._manager.setup_extensions()

        if self.settings["HTTP_PORT"]:
            self._logger.info('[LOAD] request handlers')
            self._manager.load_request_handlers()
            app = tornado.web.Application(
                self._manager.get_all_request_handlers(),
                default_host=self.settings.get('DEFAULT_HOST', ''),
                transforms=None,
                **get_tornado_app_settings(self.settings))
            app.manager = self._manager
            port = self.settings.get_int("HTTP_PORT")
            bind_address = self.settings.get('BIND_ADDRESS', '')
            server_settings = get_tornado_server_settings(self.settings)
            app.listen(port, bind_address, **server_settings)
            self._logger.info('listen port %d', port)
        else:
            self._logger.warn('no http interface, HTTP_PORT: %s',
                              str(self.settings['HTTP_PORT']))
        self._logger.info('[RUN] extensions')
        self._manager.run_extensions()

        tornado.ioloop.IOLoop.current().start()
