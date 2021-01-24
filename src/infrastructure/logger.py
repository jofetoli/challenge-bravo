#infrastructure/logger.py
import logging
import sys

def get_logger(name):
    logger = logging.getLogger(name)
    _ch = logging.StreamHandler(sys.stdout)
    _ch.setLevel(logging.INFO)
    _formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
    _ch.setFormatter(_formatter)
    logger.addHandler(_ch)
    logger.setLevel(logging.INFO)
    return logger