import logging
import sys
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
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname).4s] %(message)s', '%Y-%m-%d %H:%M:%S'))
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    sub_routine()

    sys.exit(0)




