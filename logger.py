import logging


def setup_file_logger(name, log_file, level_name="BREATH", level=logging.INFO):
    formatter = logging.Formatter("%(asctime)s [{0}] %(message)s".format(level_name))
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
