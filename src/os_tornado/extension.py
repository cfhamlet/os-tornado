"""
Extension
"""
import collections
import logging
from os_tornado.utils.module_utils import load_class


class ExtensionManager(object):
    def __init__(self, manager):
        self._manager = manager
        self._exts = collections.OrderedDict()
        self._logger = logging.getLogger('ExtManager')
        self._loaded = False

    def load(self):
        if self._loaded:
            return
        exts = self._manager.settings['EXTENSIONS']
        if not exts:
            return
        for ext_settings in exts:
            ext = self._load_extension(ext_settings)
            c_path = ext_settings['extension_class']
            if not ext:
                continue
            if ext.name not in self._exts:
                self._exts[ext.name] = ext
                self._logger.info('[LOAD] [SUCC] %s %s.%s',
                                  ext.name, ext.__module__, ext.__class__.__name__)
            else:
                self._logger.warn(
                    '[LOAD] [SKIP] already exist: %s, %s', ext.name, c_path)
        self._loaded = True

    def _load_extension(self, ext_settings):
        ext = None
        try:
            _cls = load_class(ext_settings['extension_class'], Extension)
            if _cls:
                ext = _cls(self._manager, ext_settings)
            else:
                self._logger.warn('[LOAD] [FAIL] invalid: %s',
                                  ext_settings['extension_class'])
        except Exception, e:
            self._logger.error('[LOAD] [FAIL] %s', e)
        return ext

    def iter_extensions(self):
        for name in self._exts:
            yield self._exts[name]

    def setup(self):
        for ext in self._exts.values():
            try:
                ext.setup()
            except Exception as e:
                self._logger.error('[SETUP] %s %s' % (ext.name, e))

    def cleanup(self):
        for ext in reversed(self._exts.values()):
            try:
                ext.cleanup()
            except Exception as e:
                self._logger.error('[CLEANUP] %s %s' % (ext.name, e))

    def run(self):
        for ext in self._exts.values():
            try:
                ext.run()
            except Exception as e:
                self._logger.error('[RUN] %s %s' % (ext.name, e))

    def get_extension(self, name):
        return self._exts.get(name, None)


class Extension(object):
    def __init__(self, manager, ext_settings):
        self._manager = manager
        self._ext_settings = ext_settings
        self._name = ext_settings.get('name', self.__class__.__name__).strip()
        self._logger = logging.getLogger('Ext/%s' % self._name)

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
