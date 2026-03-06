import boto3
from boto3 import Session
import json


TABLE_NAME:str = "test-20260128"

session:Session = boto3.Session(region_name="ap-northeast-2")
session2:Session = boto3.Session(session, region_name="ap-southeast-1")
session:Session = boto3.Session(region_name=None)

dynamodb_cli = session.client("dynamodb", region_name=None)
dynamodb_rsc = session2.resource("dynamodb", region_name=None)

print(session.region_name)
print(session2.region_name)


