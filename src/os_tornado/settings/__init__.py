"""
Settings
"""

from importlib import import_module
import six
import json
from collections import MutableMapping
from . import default_settings

TORNADO_APP_SETTINGS_PREFIX = "TORNADO_APP_SETTINGS_"
TORNADO_SERVER_SETTINGS_PREFIX = "TORNADO_SERVER_SETTINGS_"


class Settings(MutableMapping):

    def __init__(self, attributes=None):
        self.frozen = False
        self.attributes = {}
        self.update(attributes)

    def __getitem__(self, name):
        if name not in self:
            return None
        return self.attributes[name]

    def __contains__(self, name):
        return name in self.attributes

    def __setitem__(self, name, value):
        self._assert_mutability()
        self.attributes[name] = value

    def __delitem__(self, name):
        self._assert_mutability()
        del self.attributes[name]

    def __iter__(self):
        return iter(self.attributes)

    def __len__(self):
        return len(self.attributes)

    def get(self, name, default=None):
        """
        Get a setting value without affecting its original type.

        :param name: the setting name
        :type name: string

        :param default: the value to return if no setting is found
        :type default: any
        """
        return self[name] if name in self else default

    def _assert_mutability(self):
        if self.frozen:
            raise TypeError("Trying to modify an immutable Settings object")

    def get_bool(self, name, default=False):
        """
        Get a setting value as a boolean.

        ``1``, ``'1'``, `True`` and ``'True'`` return ``True``,
        while ``0``, ``'0'``, ``False``, ``'False'`` and ``None`` return ``False``.

        For example, settings populated through environment variables set to
        ``'0'`` will return ``False`` when using this method.

        :param name: the setting name
        :type name: string

        :param default: the value to return if no setting is found
        :type default: any
        """
        got = self.get(name, default)
        try:
            return bool(int(got))
        except ValueError:
            if got in ("True", "true"):
                return True
            if got in ("False", "false"):
                return False
            raise ValueError("Supported values for boolean settings "
                             "are 0/1, True/False, '0'/'1', "
                             "'True'/'False' and 'true'/'false'")

    def get_int(self, name, default=0):
        """
        Get a setting value as an int.

        :param name: the setting name
        :type name: string

        :param default: the value to return if no setting is found
        :type default: any
        """
        return int(self.get(name, default))

    def get_list(self, name, default=None):
        """
        Get a setting value as a list. If the setting original type is a list, a
        copy of it will be returned. If it's a string it will be split by ",".

        For example, settings populated through environment variables set to
        ``'one,two'`` will return a list ['one', 'two'] when using this method.

        :param name: the setting name
        :type name: string

        :param default: the value to return if no setting is found
        :type default: any
        """
        value = self.get(name, default or [])
        if isinstance(value, six.string_types):
            value = value.split(',')
            value = [v.strip() for v in value]
        return list(value)

    def get_dict(self, name, default=None):
        """
        Get a setting value as a dictionary. If the setting original type is a
        dictionary, a copy of it will be returned. If it is a string it will be
        evaluated as a JSON dictionary. In the case that it is a
        :class:`~os_tornado.settings.Settings` instance itself, it will be
        converted to a dictionary, containing all its current settings values
        as they would be returned by :meth:`~os_tornado.settings.Settings.get`,
        and losing all information about mutability.

        :param name: the setting name
        :type name: string

        :param default: the value to return if no setting is found
        :type default: any
        """
        value = self.get(name, default or {})
        if isinstance(value, six.string_types):
            value = json.loads(value)
        return dict(value)

    def get_float(self, name, default=0.0):
        """
        Get a setting value as a float.

        :param name: the setting name
        :type name: string

        :param default: the value to return if no setting is found
        :type default: any
        """
        return float(self.get(name, default))

    def set(self, name, value):
        self[name] = value

    def update_from_module(self, settings_module_path):
        self._assert_mutability()
        module = settings_module_path
        if isinstance(settings_module_path, six.string_types):
            module = import_module(settings_module_path)
        for key in dir(module):
            if key.isupper():
                self[key] = getattr(module, key)

    def update(self, values):
        self._assert_mutability()
        if isinstance(values, six.string_types):
            values = json.loads(values)
        if values is not None:
            for name, value in six.iteritems(values):
                self[name] = value

    def freeze(self):
        """
        Disable further changes to the current settings.

        After calling this method, the present state of the settings will become
        immutable. Trying to change values through the :meth:`~set` method and
        its variants won't be possible and will be alerted.
        """
        self.frozen = True


def iter_default_settings():
    """Return the default settings as an iterator of (name, value) tuples"""
    for name in dir(default_settings):
        if name.isupper():
            yield name, getattr(default_settings, name)


def iter_overridden_settings(settings):
    """Iterate settings that have been overridden default settings"""
    for name, def_value in iter_default_settings():
        if name not in settings:
            continue
        value = settings[name]
        if not isinstance(def_value, dict) and value != def_value:
            yield name, value


def _get_setttings_by_prefix(settings, prefix):
    p_settings = {}
    prefix_length = len(prefix)
    for key in settings:
        if key.startswith(prefix):
            k = key[prefix_length:].lower()
            p_settings[k] = settings[key]
    return p_settings


def get_tornado_app_settings(settings):
    return _get_setttings_by_prefix(settings, TORNADO_APP_SETTINGS_PREFIX)


def get_tornado_server_settings(settings):
    return _get_setttings_by_prefix(settings, TORNADO_SERVER_SETTINGS_PREFIX)
