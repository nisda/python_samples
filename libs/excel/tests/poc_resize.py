from typing import List, Any
from pprint import pprint

def resize_records(records:List[List[Any]], width:int=0, height:int=0, default:Any=None):

    if height <= 0 :
        height = len(records)
    if width <= 0:
        width = len(records[0]) if len(records) > 0 else 0

    result = []
    for row in range(0, height):
        base:List[Any] = [default] * width
        if row < len(records):
            rec = records[row][0:len(base)]
            base[0:len(rec)] = rec
            result.append(base)
        else:
            result.append(base)

    return result



data = [
    ["a1", "a2", "a3", "a4", "a5"],
    ["b1", "b2", "b3", "b4"],
    ["c1", "c2", "c3", "c4"],
]


pprint("----")
line1 = [None] * 4
line2 = ["a", "b", "c", "d", "e", "f"][0:len(line1)]
line1[0:len(line2)] = line2
pprint(line1)


pprint("----")
ret = resize_records(records=data, width=0, height=0)
pprint(ret)


pprint("----")
ret = resize_records(records=data, width=3, height=0)
pprint(ret)
ret = resize_records(records=data, width=0, height=2)
pprint(ret)
ret = resize_records(records=data, width=3, height=2)
pprint(ret)

pprint("----")
ret = resize_records(records=data, width=10, height=0)
pprint(ret)
ret = resize_records(records=data, width=0, height=8)
pprint(ret)
ret = resize_records(records=data, width=10, height=8)
pprint(ret)

