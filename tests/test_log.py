import re
import sys

import pytest
from os_tornado.log import configure_logging
from os_tornado.settings import Settings, default_settings


@pytest.fixture(scope="function")
def logging():
    import logging
    for h in logging.root.handlers:
        logging.root.removeHandler(h)
    return logging


@pytest.fixture(scope="function")
def settings():
    settings = Settings()
    settings.update_from_module(default_settings)
    return settings


def test_log_format(settings, capsys, logging):
    settings['LOG_FORMAT'] = '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s'
    configure_logging(settings)
    logger = logging.getLogger('test')
    log_string = 'test logging'
    logger.info(log_string)
    _, err = capsys.readouterr()
    regex = re.compile(r'''
    \[\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\]
    \s\[INFO\]
    \s\[test\]
    \stest\slogging
    ''', re.X)
    assert regex.match(err)


def test_log_level(settings, capsys, logging):
    settings['LOG_LEVEL'] = 'INFO'
    configure_logging(settings)
    logger = logging.getLogger('test')
    log_string = 'test logging'
    logger.info(log_string)
    _, err = capsys.readouterr()
    assert log_string in err
    logger.debug(log_string)
    _, err = capsys.readouterr()
    assert log_string not in err


def test_base_log(settings, capsys, logging):
    configure_logging(settings)
    logger = logging.getLogger('test')
    log_string = 'test logging'
    logger.info(log_string)
    _, err = capsys.readouterr()
    assert log_string in err


def test_disable_log(settings, capsys, logging):
    settings['LOG_ENABLED'] = False
    configure_logging(settings)
    logger = logging.getLogger('test')
    log_string = 'test logging'
    logger.info(log_string)
    _, err = capsys.readouterr()
    assert log_string not in err
