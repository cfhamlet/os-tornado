"""Request Handler Manager"""
import logging
import copy
import tornado.web
from os_tornado.utils.module_utils import load_class


class RequestHandlerManager(object):
    """Request Handler Manager"""

    def __init__(self, manager):
        self._manager = manager
        self._handlers = []
        self._logger = logging.getLogger('RequestHanlderManager')
        self._loaded = False

    def load(self):
        if self._loaded:
            return
        handlers = self._manager.settings['REQUEST_HANDLERS']
        if not handlers:
            return
        for h_settings in handlers:
            h_settings = copy.deepcopy(h_settings)
            if 'pattern' not in h_settings:
                self._logger.error(
                    '[LOAD] no pattern, %s' % str(h_settings))
                continue

            handler_cls = self._load_cls(h_settings)
            if not handler_cls:
                continue

            pattern = h_settings.pop('pattern')
            h_settings.pop('handler_class')

            self._handlers.append(
                (pattern, handler_cls, h_settings))
            self._logger.info(
                '[LOAD] SUCC %s %s.%s %s',
                pattern, handler_cls.__module__, handler_cls.__name__,
                str(h_settings) if h_settings else "")
        self._loaded = True

    def _load_cls(self, handler_settings):
        handler_class = None
        if 'handler_class' not in handler_settings:
            self._logger.error(
                '[LOAD] no handler_class, %s' % str(handler_settings))
            return handler_class
        try:
            handler_class_str = handler_settings['handler_class']
            _cls = load_class(handler_class_str, tornado.web.RequestHandler)
            if _cls:
                handler_class = _cls
            else:
                self._logger.error('[LOAD] invalid, %s', handler_class_str)

        except Exception as e:
            self._logger.error('[LOAD] %s, %s' %
                               (e, str(handler_settings)))
        return handler_class

    def iter_handlers(self):
        return iter(self._handlers)

    def get_all_handlers(self):
        return self._handlers
