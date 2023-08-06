import os
import logging


def enable_logging(func):
    def wrapper(*args, **kwargs):
        logging.getLogger().setLevel(os.environ.get('LOG_LEVEL', 'INFO'))
        return func(*args, **kwargs)

    return wrapper
