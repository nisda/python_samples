import logging
import sys
import os
import datetime
import decimal



def sub_routine():
    logger = logging.getLogger(__name__)
    print("id[sub]: " + str(id(logger)))
    logger.critical ("aaa")
    logger.error("bbb")
    logger.warning("ccc")
    logger.info("ddd")
    logger.debug("eee")

    logger.critical({
        "str": "sssss",
        "dt": datetime.datetime.now(),
        "bytes": b'bbbbbb',
        'decimal': decimal.Decimal(123.45),
    })
    return


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    print("[main] id: " + str(id(logger)))

    print("")
    print("[1] 設定なし--------------------")
    sub_routine()

    print("")
    print("[2] 設定あり--------------------")
    LOG_FILE_NAME = os.path.splitext(os.path.basename(__file__))[0] + ".log"
    LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), "log", LOG_FILE_NAME)
    stream_handler = logging.FileHandler(LOG_FILE_PATH)
    stream_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname).4s] %(message)s', '%Y-%m-%d %H:%M:%S'))
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    sub_routine()

    sys.exit(0)




