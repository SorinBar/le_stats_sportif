import time
import logging
from logging.handlers import RotatingFileHandler

logging.Formatter.converter = time.gmtime

def get_logger(logger_name, logger_filename):
    """
    Setup and return the logger
    """

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(logger_filename, maxBytes=10000, backupCount=10)
    formatter = logging.Formatter('%(asctime)s %(levelname)6s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
