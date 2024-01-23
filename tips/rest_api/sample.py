import sys
import json
from RestAPI import RestAPI

if __name__ == '__main__':

    print("***********************************")

    api = RestAPI(
        base_url="https://httpbin.org/",
        content_type="application/x-www-form-urlencoded",
        base_headers={"b-api-key": "XXXX"},
        base_query_strings={"b-api-key": "YYYY"}
    )
    response = api.request(
        method="post",
        path="/post",
        headers={"h-aaa": "AAA", "h-bbb": "BBB"},
        query_strings={"q-aaa": "AAA", "q-bbb": ["BBB", "bbb"]},
        data={"d-aaa": "AAA", "d-bbb": ["BBB", "bbb"]},
    )
    print("ret ----------------")
    print(json.dumps(response, indent=2))
    print("body(json) ----------------")
    print(json.dumps(json.loads(response.get("body")), indent=2))


    print("***********************************")

    api = RestAPI(
        base_url="https://httpbin.org/",
        content_type="application/json",
        base_headers={"b-api-key": "XXXX"},
        base_query_strings={"b-api-key": "YYYY"}
    )
    response = api.request(
        method="patch",
        path="/patch",
        headers={"h-aaa": "AAA", "h-bbb": "BBB"},
        query_strings={"q-aaa": "AAA", "q-bbb": ["BBB", "bbb"]},
        data={"d-aaa": "AAA", "d-bbb": ["BBB", "bbb"]},
    )
    print("ret ----------------")
    print(json.dumps(response, indent=2))
    print("body(json) ----------------")
    print(json.dumps(json.loads(response.get("body")), indent=2))

    sys.exit(0)
