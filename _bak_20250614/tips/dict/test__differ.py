
import mylibs.dict_util as dict_util
import pytest
import re


if __name__ == '__main__':
    data_left = {
        "A" : {
            "AA" : 123,
            "AB" : 234,
        },
        "B" : [
            "B1",
            {
                "B2A" : "yhnj",
                "B2B" : "yhnj",
                "B2C" : "yhnj",
            }
        ], 
    }
    data_right = {
        "B" : [
            "B1",
            {
                "B2C" : "gse",
                "B2A" : "hfd",
                "B2B" : "yhnj",
            }
        ],
        "A" : {
            "AB" : 234,
            "aa" : 123,
            "bb" : 432,
        },
    }

    ret = dict_util.differ(data_left=data_left, data_right=data_right)
    print(ret)
