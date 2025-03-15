from json import dumps as origin_dumps
from json import *
import functools

import datetime
import decimal
import uuid

# json.dump未対応データ型の変換関数
# usage:
#   json.dumps(variable, default=_json_serialize)
def __json_serialize(obj):
    # datetime
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    if isinstance(obj, datetime.time):
        return obj.isoformat()
    # decimal
    if isinstance(obj, decimal.Decimal):
        if '.' in str(obj):
            return float(obj)
        else:
            return int(obj)
    # bytes
    if isinstance(obj, bytes):
        return obj.decode()
    # uuid
    if isinstance(obj, uuid.UUID):
        return str(obj)
    # 上記以外はサポート対象外.
    raise TypeError ("Type %s not serializable" % type(obj))


# dumps:parameter-override
dumps = functools.partial(origin_dumps, default=__json_serialize)



