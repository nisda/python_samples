import logging
import sys


# これだけだと setLevel が効かない。
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.critical ("aaa") # 出力される
logger.error("bbb")     # 出力される
logger.warning("ccc")   # 出力される
logger.info("ddd")      # 出力されない
logger.debug("eee")     # 出力されない

sys.exit(0)
