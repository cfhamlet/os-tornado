"""
Extension
"""
import collections
import logging
from os_tornado.utils.module_utils import load_class


class ExtensionManager(object):
    def __init__(self, manager):
        self._manager = manager
        self._extensions = collections.OrderedDict()
        self._logger = logging.getLogger('ExtensionManager')
        self._loaded = False

    def load(self):
        if self._loaded:
            return
        exts = self._manager.settings['EXTENSIONS']
        if not exts:
            return
        for ext_settings in exts:
            extension_cls = self._load_extension(ext_settings)
            if not extension_cls:
                continue

            name = extension_cls.name
            if 'name' not in ext_settings:
                self._logger.warn('[LOAD] no name, will use %s' % name)
            else:
                name = ext_settings['name']

            ext_settings.pop('extension_class')
            if name not in self._extensions:
                self._extensions[name] = extension_cls
                self._logger.info('[LOAD] SUCC %s %s.%s %s',
                                  name, extension_cls.__module__,
                                  extension_cls.__class__.__name__,
                                  str(ext_settings) if ext_settings else '')
            else:
                self._logger.warn(
                    '[LOAD] SKIP already exist: %s, %s', name, str(ext_settings))
        self._loaded = True

    def _load_extension(self, ext_settings):
        ext = None
        if 'extension_class' not in ext_settings:
            self._logger.error(
                '[LOAD] no extension_class, %s' % str(ext_settings))
            return ext

        try:
            extension_class_str = ext_settings['extension_class']
            _cls = load_class(extension_class_str, Extension)
            if _cls:
                ext = _cls(self._manager, ext_settings)
            else:
                self._logger.error('[LOAD] invalid, %s', extension_class_str)

        except Exception, e:
            self._logger.error('[LOAD] %s, %s' % (e, str(ext_settings)))
        return ext

    def iter_extensions(self):
        for name in self._extensions:
            yield self._extensions[name]

    def setup(self):
        for ext in self._extensions.values():
            try:
                ext.setup()
            except Exception as e:
                self._logger.error('[SETUP] %s %s' % (ext.name, e))

    def cleanup(self):
        for ext in reversed(self._extensions.values()):
            try:
                ext.cleanup()
            except Exception as e:
                self._logger.error('[CLEANUP] %s %s' % (ext.name, e))
        self._extensions.clear()

    def run(self):
        for ext in self._extensions.values():
            try:
                ext.run()
            except Exception as e:
                self._logger.error('[RUN] %s %s' % (ext.name, e))

    def get_extension(self, name):
        return self._extensions.get(name, None)


class Extension(object):
    def __init__(self, manager, ext_settings):
        self._manager = manager
        self._ext_settings = ext_settings
        self._name = ext_settings.get('name', self.__class__.__name__).strip()
        self._logger = logging.getLogger('Extension/%s' % self._name)

    @property
    def name(self):
        return self._name

    @property
    def ext_settings(self):
        return self._ext_settings

    @property
    def settings(self):
        return self._manager.settigns

    def run(self):
        pass

    def setup(self):
        pass

    def cleanup(self):
        pass
