import json
import mylib.DynamodbUtil as DynamodbUtil

update_expression = DynamodbUtil.update_expression(
    set_item={"aaa": "AAA", "bbb": "BBB"},
    remove_item=["ccc", "ddd"],
    add_item={"xxx": "XXX"}
)
print(json.dumps(update_expression, indent=2))


