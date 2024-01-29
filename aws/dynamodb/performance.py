#---------------------------------------
#   DynamoDBのパフォーマンス計測
#---------------------------------------
import boto3
import datetime
import time
import sys


def measure(func:callable):
    before = datetime.datetime.now()
    func()
    after = datetime.datetime.now()
    diff = after - before
    print(f"{before:%H:%M:%S.%f} -> {after:%H:%M:%S.%f} | {diff}")

def create_tables():
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')

    table_provisioned = dynamodb.create_table(**{
        "TableName": 'performance-provisioned',
        "KeySchema": [
            {"AttributeName": "id", "KeyType": "HASH"},
        ],
        "AttributeDefinitions": [
            {"AttributeName": "id", "AttributeType": "N"},
        ],
        "BillingMode" : "PROVISIONED",
        "ProvisionedThroughput": {"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
    })
    print(f"Creating 'performance-provisioned'...")


    table_ondemand = dynamodb.create_table(**{
        "TableName": 'performance-ondemand',
        "KeySchema": [
            {"AttributeName": "id", "KeyType": "HASH"},
        ],
        "AttributeDefinitions": [
            {"AttributeName": "id", "AttributeType": "N"},
        ],
        "BillingMode" : "PAY_PER_REQUEST",
    })
    print(f"Creating 'performance-ondemand'...")


    table_provisioned.wait_until_exists()
    table_ondemand.wait_until_exists()

    return (table_provisioned, table_ondemand)


def put_item(table, data):
    response = table.put_item(
        Item=data
    )

def get_item(table, key):
    response = table.get_item(
        Key=key,
    )

def delete_item(table, key):
    response = table.get_item(
        Key=key,
    )




if __name__ == '__main__':

    print()
    print("-- create tables")
    (table_provisioned, table_ondemand) = create_tables()

    # ▼ここだけそれぞれ2秒くらいかかる。ウォームアップ|スケーリング中による遅さと推測。
    print("-- put_item / provisioned")
    time.sleep(1)
    measure(lambda: put_item(table_provisioned, data={"id": 1, "value": "AAA"}))
    time.sleep(1)
    measure(lambda: put_item(table_provisioned, data={"id": 2, "value": "BBB"}))
    time.sleep(1)
    measure(lambda: put_item(table_provisioned, data={"id": 3, "value": "CCC"}))

    # ▼ここから先は全部ミリ秒
    print("-- put_item / ondemand")
    time.sleep(1)
    measure(lambda: put_item(table_ondemand, data={"id": 1, "value": "AAA"}))
    time.sleep(1)
    measure(lambda: put_item(table_ondemand, data={"id": 2, "value": "BBB"}))
    time.sleep(1)
    measure(lambda: put_item(table_ondemand, data={"id": 3, "value": "CCC"}))


    print("-- get_item / provisioned")
    time.sleep(1)
    measure(lambda: get_item(table_provisioned, key={"id": 1}))
    time.sleep(1)
    measure(lambda: get_item(table_provisioned, key={"id": 2}))
    time.sleep(1)
    measure(lambda: get_item(table_provisioned, key={"id": 3}))

    print("-- get_item / ondemand")
    time.sleep(1)
    measure(lambda: get_item(table_ondemand, key={"id": 1}))
    time.sleep(1)
    measure(lambda: get_item(table_ondemand, key={"id": 2}))
    time.sleep(1)
    measure(lambda: get_item(table_ondemand, key={"id": 3}))


    print("-- delete_item / provisioned")
    time.sleep(1)
    measure(lambda: delete_item(table_provisioned, key={"id": 1}))
    time.sleep(1)
    measure(lambda: delete_item(table_provisioned, key={"id": 2}))
    time.sleep(1)
    measure(lambda: delete_item(table_provisioned, key={"id": 3}))

    print("-- delete_item / ondemand")
    time.sleep(1)
    measure(lambda: delete_item(table_ondemand, key={"id": 1}))
    time.sleep(1)
    measure(lambda: delete_item(table_ondemand, key={"id": 2}))
    time.sleep(1)
    measure(lambda: delete_item(table_ondemand, key={"id": 3}))

    
    print("-- put_item / provisioned")
    time.sleep(1)
    measure(lambda: put_item(table_provisioned, data={"id": 1, "value": "AAA"}))
    time.sleep(1)
    measure(lambda: put_item(table_provisioned, data={"id": 2, "value": "BBB"}))
    time.sleep(1)
    measure(lambda: put_item(table_provisioned, data={"id": 3, "value": "CCC"}))

    print("-- put_item / ondemand")
    time.sleep(1)
    measure(lambda: put_item(table_ondemand, data={"id": 1, "value": "AAA"}))
    time.sleep(1)
    measure(lambda: put_item(table_ondemand, data={"id": 2, "value": "BBB"}))
    time.sleep(1)
    measure(lambda: put_item(table_ondemand, data={"id": 3, "value": "CCC"}))


    print("-- get_item / provisioned")
    time.sleep(1)
    measure(lambda: get_item(table_provisioned, key={"id": 1}))
    time.sleep(1)
    measure(lambda: get_item(table_provisioned, key={"id": 2}))
    time.sleep(1)
    measure(lambda: get_item(table_provisioned, key={"id": 3}))

    print("-- get_item / ondemand")
    time.sleep(1)
    measure(lambda: get_item(table_ondemand, key={"id": 1}))
    time.sleep(1)
    measure(lambda: get_item(table_ondemand, key={"id": 2}))
    time.sleep(1)
    measure(lambda: get_item(table_ondemand, key={"id": 3}))


    print("-- delete_item / provisioned")
    time.sleep(1)
    measure(lambda: delete_item(table_provisioned, key={"id": 1}))
    time.sleep(1)
    measure(lambda: delete_item(table_provisioned, key={"id": 2}))
    time.sleep(1)
    measure(lambda: delete_item(table_provisioned, key={"id": 3}))

    print("-- delete_item / ondemand")
    time.sleep(1)
    measure(lambda: delete_item(table_ondemand, key={"id": 1}))
    time.sleep(1)
    measure(lambda: delete_item(table_ondemand, key={"id": 2}))
    time.sleep(1)
    measure(lambda: delete_item(table_ondemand, key={"id": 3}))


    print("-- delete tables")
    time.sleep(1)
    table_provisioned.delete()
    table_ondemand.delete()


    sys.exit(0)


