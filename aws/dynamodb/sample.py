import json
import mylib.DynamodbUtil as DynamodbUtil

res = DynamodbUtil.update_expression(
    # set_item={"aaa": "AAA", "bbb": "BBB"},
    # remove_item=["ccc", "ddd"],
    # add_item={"xxx": "XXX"}
)
print(json.dumps(res, indent=2))
