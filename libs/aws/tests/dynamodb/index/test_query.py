import pytest
import boto3

from boto3.dynamodb.conditions import AttributeBase, Key, Attr, Or, And, Not
from dynamodb import dynamodb_util
from dynamodb.dynamodb_util import IndexTypes
from pprint import pprint


TABLE_NAME = "test-20260128"

# def test_query():
#     idx:dynamodb_util.Table = dynamodb_util.Index(
#         table=None,
#         name="IDX-01",
#         type=IndexTypes.GSI,
#         hash_keys=["p1", "p2"],
#         range_keys=["s1", "s2", "s3"],
#     )

#     items = [
#         {"p1": 2, "p2": "A", "s1": "11"},
#         {"p1": 2, "p2": "A", "s1": "11", "x1": "XX"},
#         {"p1": 1, "p2": "A", "s1": "11", "s2": "12", "x1": "XX"},
#         {"p1": 1, "p2": "B", "x1": "X", "x2": "XX"},
#         {"p1": 1, "p2": "B", "x1": "X", "x2": "XX", "x3": "XXX"},
#         {"p1": 1, "p2": "B", "x1": "X", "x2": "XX", "x3": "ZZZ", "x4": "ZZZZ"},
#         {"p1": 1, "p2": "A"},
#         {"p1": 1, "p2": "A"},
#         {"p1": 1, "p2": "A"},
#     ]

#     ret = idx.query(items=items)
#     print(type(ret))
#     for r in ret:
#         print(type(r))
        


def test_query():
    dynamodb_rsc = boto3.resource('dynamodb', region_name="ap-northeast-1")
    table = dynamodb_rsc.Table(TABLE_NAME)

    idx:dynamodb_util.Table = dynamodb_util.Index(
        table=table,
        name=None,
        type=IndexTypes.Primary,
        hash_keys=["pk"],
        range_keys=["sk"],
    )

    items = [
        {"pk": "ut_put", "sk": 'overwrite'},
        # {"pk": "ut_put", "sk": 'ttl_none_ow'},
        {"pk": "ut_put", "sk": '****'},
        {"pk": "PartiQL", "aa": "A"},
        {"pk": "PartiQL"},
        # {"pk": "ut_put"},
        # {"pk": "zzz"},
    ]

    ret = idx.query(items=items)
    temp = list(ret)
    print(len(temp))
    for r in temp:
        print(r)
        

    # print("******************")
    # key_condition = Key("pk").eq("ut_put")
    # filter_conditsion = Attr("sk").eq("different key-2")
    # res = table.query(
    #     **{
    #         "KeyConditionExpression" : key_condition,
    #         "FilterExpression" : filter_conditsion,
    #     }
    # )
    # pprint(res["Items"])
    

