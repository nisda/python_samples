from mylibs.dynamodb_util import Table as Table
import boto3
from boto3.dynamodb.conditions import Key

table = Table(table_name='test_20250317')

print("--------------------")
items = table.scan()
print(list(items))

print("--------------------")
items = table.query(KeyConditionExpression=Key("id").eq("123"))
print(list(items))

print("--------------------")
items = table.query(
    KeyConditionExpression="#id = :id",
    ExpressionAttributeNames={ '#id' : 'id'},
    ExpressionAttributeValues={ ':id' : '456'},
)
print(list(items))


print("--------------------")
items = table.query(
    IndexName='name-index',
    KeyConditionExpression="#name = :name",
    ExpressionAttributeNames={ '#name' : 'name'},
    ExpressionAttributeValues={ ':name' : 'bob'},
)
print(list(items))

