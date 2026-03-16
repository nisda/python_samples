import boto3
from boto3 import Session
import json
from boto3.dynamodb.conditions import AttributeBase, Key, Attr, Or, And, Not

import sys
TABLE_NAME:str = "apigw-poc-apigw-basic-auth"

session:Session = boto3.Session(region_name="ap-northeast-1")

dynamodb_cli = session.client("dynamodb", region_name=None)
dynamodb_rsc = session.resource("dynamodb", region_name=None)

table = dynamodb_rsc.Table(TABLE_NAME)

print(type(table.global_secondary_indexes or []))
print(type(table.local_secondary_indexes or []))
