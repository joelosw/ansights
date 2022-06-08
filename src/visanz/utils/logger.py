import logging

"""
Let All loggers be handled by the console
"""
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s : %(name)s : %(levelname)s : %(message)s', "%H:%M:%S")
console.setFormatter(formatter)


def get_logger(name, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(console)
    return logger
