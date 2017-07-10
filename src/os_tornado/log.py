import logging
from logging.config import dictConfig


DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'incremental': True,
}


def configure_logging(settings):
    dictConfig(DEFAULT_LOGGING)
    if settings["LOG_ENABLED"]:
        handler = logging.StreamHandler()
    else:
        handler = logging.NullHandler()

    formatter = logging.Formatter(
        fmt=settings['LOG_FORMAT'],
        datefmt=settings['LOG_DATEFORMAT'])
    logging.root.setLevel(logging.NOTSET)
    handler.setFormatter(formatter)
    handler.setLevel(settings['LOG_LEVEL'])
    logging.root.addHandler(handler)