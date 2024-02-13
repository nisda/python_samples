import logging
import sys
import datetime
import decimal

# ▼これだけでも最低限の動作はする
# logging.basicConfig()


# ▼いろいろ設定ありで初期化。
# ルートロガーへの設定
logging.basicConfig(
    filename=None,
    level=logging.ERROR,
    # format="[%(levelname)s] %(name)s:%(message)s",
    style='{', format='{asctime} [{levelname:.4}] {name}: {message}',   # styleで書式変更できる
    )



def sub_routine():
    logger = logging.getLogger(__name__)
    print("[sub] id: " + str(id(logger)))
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
    print("[1]--------------------")
    sub_routine()

    print("")
    print("[2]--------------------")
    logger.setLevel(logging.DEBUG)
    sub_routine()

    sys.exit(0)




