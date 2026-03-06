import boto3
from boto3 import Session
import json
from boto3.dynamodb.conditions import AttributeBase, Key, Attr, Or, And, Not

import sys
TABLE_NAME:str = "test-20260128"

session:Session = boto3.Session(region_name="ap-northeast-1")

dynamodb_cli = session.client("dynamodb", region_name=None)
dynamodb_rsc = session.resource("dynamodb", region_name=None)

table = dynamodb_rsc.Table(TABLE_NAME)
indexes = sorted(table.global_secondary_indexes, key=lambda x: x["IndexName"]) 
print(json.dumps(indexes, indent=2))

keys = [
    (key["KeyType"], key["AttributeName"])
    for idx in indexes
    for key in idx["KeySchema"]
]
print(json.dumps(keys, indent=2))


sys.exit(0)

ret = table.query(
    IndexName="GSI-02",
    KeyConditionExpression=(
        # HASKキーは "全ての項目を" "イコールで" 指定する必要あり。
        # １つだけ指定は認められない。
        Key('gsi_pk1').eq('test') &
        Key('gsi_pk2').eq('test') &
        # RANGEキーは順番に指定する必要あり。飛ばせない。
        # さらに最後に指定する１つだけが範囲指定可能。それより前は eq のみ。
        Key('gsi_sk1').eq('aa') &
        Key('gsi_sk2').lt('a')
    ),
    # FilterConditionExpression=(
    #     Key('gsi_pk1').eq('test') &
    #     Key('gsi_pk2').eq('test') &
    #     Attr('gsi_sk1').eq('test')
    # ),
)
print(ret["Items"])

