import inspect
import os
import sys
from importlib import import_module
from pkgutil import iter_modules


def walk_modules(module_path):
    """Loads a module and all its submodules from the given module path and
    returns them. If *any* module throws an exception while importing, that
    exception is thrown back.

    For example: walk_modules('os_tornado.utils')
    """

    mods = []
    mod = import_module(module_path)
    mods.append(mod)
    if hasattr(mod, '__path__'):
        for _, subpath, ispkg in iter_modules(mod.__path__):
            fullpath = '.'.join((module_path, subpath))
            if ispkg:
                mods += walk_modules(fullpath)
            else:
                submod = import_module(fullpath)
                mods.append(submod)
    return mods


def load_class(class_path, base_class, include_base_class=False):
    module_path, class_name = class_path.rsplit('.', 1)
    _mod = import_module(module_path)
    _cls = getattr(_mod, class_name)
    if inspect.isclass(_cls) and \
            issubclass(_cls, base_class) and \
            (include_base_class or _cls != base_class):
        return _cls
    return None


def iter_classes(module_path, base_class, include_base_class=False):
    for module in walk_modules(module_path):
        for obj in vars(module).values():
            if inspect.isclass(obj) and \
                    issubclass(obj, base_class) and \
                    obj.__module__ == module.__name__ and \
                    (include_base_class or obj != base_class):
                yield obj
