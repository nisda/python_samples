from logging import getLogger
from uuid import uuid4


logger = getLogger(__name__)

def foo():
    return uuid4()

def log():
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.critical("critical")
    return True
