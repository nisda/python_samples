import sys
import json
from RestAPI import RestAPI

if __name__ == '__main__':

    print("*****************************************************")
    print(" application/x-www-form-urlencoded")
    print("*****************************************************")

    api = RestAPI(
        base_url="https://httpbin.org/",
        base_headers={"b-api-key": "XXXX"},
        base_query_strings={"b-api-key": "YYYY"}
    )
    response = api.request(
        method="post",
        path="/post",
        content_type="application/x-www-form-urlencoded",
        headers={"h-aaa": "AAA", "h-bbb": "BBB"},
        query_strings={"q-aaa": "AAA", "q-bbb": ["BBB", "bbb"]},
        data={"d-aaa": "AAA", "d-bbb": ["BBB", "bbb"]},
    )
    print("ret ----------------")
    print(json.dumps(response, indent=2))
    print("body(json) ----------------")
    print(json.dumps(json.loads(response.get("body")), indent=2))


    print("*****************************************************")
    print(" application/json")
    print("*****************************************************")

    api = RestAPI(
        base_url="https://httpbin.org/",
        base_headers={"b-api-key": "XXXX"},
        base_query_strings={"b-api-key": "YYYY"}
    )
    response = api.request(
        method="patch",
        path="/patch",
        content_type="application/json",
        headers={"h-aaa": "AAA", "h-bbb": "BBB"},
        query_strings={"q-aaa": "AAA", "q-bbb": ["BBB", "bbb"]},
        data={"d-aaa": "AAA", "d-bbb": ["BBB", "bbb"]},
    )
    print("ret ----------------")
    print(json.dumps(response, indent=2))
    print("body(json) ----------------")
    print(json.dumps(json.loads(response.get("body")), indent=2))


    print()
    print("*****************************************************")
    print(" with files")
    print("*****************************************************")
    api = RestAPI(
        base_url="https://httpbin.org/",
    )
    response = api.request(
        method="post",
        path="/post",
        content_type="application/json",
        headers={
            "api-key" : "bjBrofuw23Cjvgm9W2e43",
        },
        data={"d-aaa": "AAA", "d-bbb": ["BBB", "bbb"]},
        files = {
            "file1" : {
                "filename": "aaa.txt",
                "content" : b"aaa\nAAA\n",
            },
            "file2" : {
                "filename": "bbb.json",
                "content" : json.dumps({
                    "id": "pux010354",
                    "name": "test",
                    "price": 123.45,
                    "child-ids": [
                        "pby206679",
                        "pbz311036",
                    ]
                },indent=2).encode('utf-8'),
            },
        },
    )
    print("ret ----------------")
    print(json.dumps(response, indent=2))
    print("body(json) ----------------")
    print(json.dumps(json.loads(response.get("body")), indent=2))


    sys.exit(0)
