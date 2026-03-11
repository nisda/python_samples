import boto3
from boto3 import Session
import json
from datetime import datetime 


TABLE_NAME:str = "test-20260128"

session:Session = boto3.Session(region_name="ap-northeast-2")

dynamodb_cli = session.client("dynamodb", region_name="ap-northeast-1")
dynamodb_rsc = session.resource("dynamodb", region_name="ap-northeast-1")

"""
INSERT で上書きはできない。
"""


TABLE_NAME = "test-20260128"

Statement1:str = "DELETE FROM \"test-20260128\" WHERE \"pk\" = 'PartiQL' AND \"sk\" = 'Test1'"
# Statement2:str = "INSERT INTO \"test-20260128\" value {'pk': 'PartiQL', 'sk': 'Test1', '_updated_at': '" + datetime.now().isoformat() + "'}"  # 同じアイテムに対する処理は同じトランザクションではNG
Statement3:str = "INSERT INTO \"test-20260128\" value {'pk': 'PartiQL', 'sk': 'Test2', '_updated_at': '" + datetime.now().isoformat() + "'}"  # これはキーが違うのでOK


res = dynamodb_cli.execute_transaction(
    TransactStatements=[
        {
            "Statement": Statement1
        },
        {
            "Statement": Statement3
        }
    ]
)


print(json.dumps(res, indent=2))
