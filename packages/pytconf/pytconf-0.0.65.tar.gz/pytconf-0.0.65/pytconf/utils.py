import logging

from pytconf.data import LOGGER_NAME


def get_logger():
    return logging.getLogger(LOGGER_NAME)
