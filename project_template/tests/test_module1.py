from package_name.module1 import foo, log
import os
import logging



from logging import getLogger

logger = getLogger(__name__)


def test_foo():
    from uuid import UUID
    ret = foo()
    assert isinstance(ret, UUID)


def test_log():
    ret = log()
    logger.warning(ret)
    assert ret == True

