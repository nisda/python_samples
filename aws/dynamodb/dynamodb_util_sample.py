import json
import mylibs.dynamodb_util as DynamodbUtil

#-------------------------------------------------------
# for `Table.update_item()` and others
#-------------------------------------------------------
update_expression = DynamodbUtil.update_expression(
    set_item={"aaa": "AAA", "bbb": "BBB"},
    remove_item=["ccc", "ddd"],
    add_item={"xxx": "XXX"}
)
print(json.dumps(update_expression, indent=2))


#-------------------------------------------------------
# for DynamodbClient
#-------------------------------------------------------
item = {
    "todoId": "t0001",
    "title": "this is title",
    "status": "unstarted",
    "createdAt": 1674124101857,
    "binary": b"pen",
    "any string set": {"Tag Name1", "Tag Name2", "TagName3"},
    "any number set": {111, 222, 333},
    "any binary set": [b"aaa", b"bbb", b"ccc"],
    "any map": {"map-name1": "map-value1", "map-name2": 111},
    "any list": ["list-value1", "222"],
    "any null": None,
    "any bol": False,
}


print()
print("# Serialize")
serialized_item = DynamodbUtil.type_serialize(item)
print(serialized_item)

print()
print("# Deserialize")
deserialized_item = DynamodbUtil.type_deserialize(serialized_item)
print(deserialized_item)

