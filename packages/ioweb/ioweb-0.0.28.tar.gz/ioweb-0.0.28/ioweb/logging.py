import logging
from logging.handlers import RotatingFileHandler


def setup_fail_logging(
        filename, mode='a', max_bytes=(50 * 1024 * 1024),
        formatter='%(asctime)s [%(levelname)s] (%(name)s) %(message)s',
    ):
    logger = logging.getLogger()
    hdl = RotatingFileHandler(filename, mode, maxBytes=max_bytes)
    hdl.setFormatter(logging.Formatter(formatter))
    hdl.setLevel(logging.ERROR)
    logger.addHandler(hdl)
