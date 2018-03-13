import os

import os_tornado
import pytest
import tornado

from tests.test_commands.cmd import run


def test_command_startproject(tmpdir):
    paths = """
    temp/manager.py
    temp/app/settings.py
    temp/app/__init__.py
    temp/app/extensions/__init__.py
    temp/app/extensions/example_extension.py
    temp/app/request_handlers/__init__.py
    temp/app/request_handlers/example_handler.py
    """
    run('startproject temp %s' % tmpdir.strpath)
    for p in paths.split():
        assert tmpdir.join(p.strip()).exists()


def test_command_list():
    env = os.environ.copy()
    env["OS_TORNADO_SETTINGS_MODULE"] = 'tests.test_commands.settings'
    result, _ = run('list', env=env)
    assert '[ext/req/all]' in result
    result, _ = run('list ext', env=env)
    assert 'TempExtension' in result
    result, _ = run('list req', env=env)
    assert 'TempHandler' in result
    result, _ = run('list all', env=env)
    assert 'TempExtension' in result
    assert 'TempHandler' in result


def test_command_version():
    result, _ = run('version')
    assert os_tornado.__version__ in result


def test_unkown_cmd():
    cmd = 'unknown'
    result, _ = run(cmd)
    assert 'Unknown command: %s' % cmd in result


def test_cmdline():
    result, _ = run()
    for cmd in ['list', 'runserver', 'startproject', 'version']:
        assert cmd in result


@pytest.mark.skip(reason="tornado do not support get_unused_port anymore")
def test_runserver():
    port = tornado.testing.get_unused_port()
    env = os.environ.copy()
    env["OS_TORNADO_SETTINGS_MODULE"] = 'tests.test_commands.settings'
    env["TEST_CMD_CALLBACK_STOP"] = 'TRUE'
    stdout, stderr = run('runserver -p %d' % port, env=env)
    flags = [
        '[LOAD] SUCC Temp tests.test_commands.temp_extension.TempExtension',
        '[LOAD] SUCC / tests.test_commands.temp_handler.TempHandler',
        'listen port %d' % port,
    ]
    for flag in flags:
        assert flag in stderr
    assert 'STOP SUCC' in stdout

    port = tornado.testing.get_unused_port()
    stdout, stderr = run('runserver -s PORT=%d' % port, env=env)
    assert 'listen port %d' % port in stderr

    port1 = tornado.testing.get_unused_port()
    stdout, stderr = run('runserver -s PORT=%d -p %d' %
                         (port, port1), env=env)
    assert 'listen port %d' % port1 in stderr
