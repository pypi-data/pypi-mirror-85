import logging


def create_logger(name, level=logging.INFO):
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(level)

    return logger
