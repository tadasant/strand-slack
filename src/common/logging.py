import logging

from src.config import config


def get_logger(caller_name, output_file):
    log_level = config['LOG_LEVEL'] if 'LOG_LEVEL' in config else logging.DEBUG
    logger = logging.getLogger(caller_name)
    logger.setLevel(log_level)

    ch = logging.StreamHandler()
    ch.setLevel(log_level)

    fh = logging.FileHandler(output_file)
    fh.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger
