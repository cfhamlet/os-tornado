import os
import pytest


def test_iter_class():
    from os_tornado.utils.module_utils import iter_classes
    from tests.test_module_utils.test_mod.class_b import BaseClass
    classes = [c for c in iter_classes('tests.test_module_utils', BaseClass)]
    expected = [
        'ClassB',
    ]
    assert set([c.__name__ for c in classes]) == set(expected)


def test_walk_modules():
    from os_tornado.utils.module_utils import walk_modules
    mods = walk_modules('tests.test_module_utils')
    expected = [
        'tests.test_module_utils',
        'tests.test_module_utils.test_mod',
        'tests.test_module_utils.test_mod.class_b',
        'tests.test_module_utils.test_mod.class_a',
        'tests.test_module_utils.test_mod0',
        'tests.test_module_utils.test_mod0.test_mod1',
        'tests.test_module_utils.test_module_utils',
    ]
    assert set([m.__name__ for m in mods]) == set(expected)


def test_load_class():
    from os_tornado.utils.module_utils import load_class
    from os_tornado.commands import Command
    from os_tornado.commands.version import VersionCommand
    obj = load_class('os_tornado.commands.version.VersionCommand', Command)
    assert obj is VersionCommand
    obj = load_class('os_tornado.commands.Command', Command)
    assert obj is None
    obj = load_class(
        'os_tornado.commands.version.VersionCommand', VersionCommand)
    with pytest.raises(ImportError):
        load_class('not_exist.NotExist', Command)
    with pytest.raises(AttributeError):
        obj = load_class('os_tornado.commands.version.NotExist', Command)
