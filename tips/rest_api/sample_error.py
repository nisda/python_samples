import sys
import json
from RestAPI import RestAPI
import urllib.error

if __name__ == '__main__':

    print("*****************************************************")
    print(" 500 error")
    print("*****************************************************")

    api = RestAPI(
        base_url="https://httpbin.org/",
        base_headers={"b-api-key": "XXXX"},
        base_query_strings={"b-api-key": "YYYY"}
    )
    response = api.request(
        method="get",
        path="/status/500",
        content_type="application/json",
        headers={"h-aaa": "AAA", "h-bbb": "BBB"},
        query_strings={"q-aaa": "AAA", "q-bbb": ["BBB", "bbb"]},
        data={"d-aaa": "AAA", "d-bbb": ["BBB", "bbb"]},
    )
    print("ret ----------------")
    print(json.dumps(response, indent=2))
    print("body(str) ----------------")
    print(response.get("body"))


    print("*****************************************************")
    print(" 500 error (urllib.error.HTTPError)")
    print("*****************************************************")

    api = RestAPI(
        base_url="https://httpbin.org/",
        base_headers={"b-api-key": "XXXX"},
        base_query_strings={"b-api-key": "YYYY"}
    )
    try:
        response = api.request(
            method="get",
            path="/status/500",
            content_type="application/json",
            headers={"h-aaa": "AAA", "h-bbb": "BBB"},
            query_strings={"q-aaa": "AAA", "q-bbb": ["BBB", "bbb"]},
            data={"d-aaa": "AAA", "d-bbb": ["BBB", "bbb"]},
            raise_http_error=True,
        )
    except urllib.error.HTTPError as e:

        ex = urllib.error.HTTPError(
            url = e.url,
            code = e.code,
            # msg = (e.msg, e.read().decode()), # httpbin.org は error 時に body を返さないので。
            msg = (e.msg, json.dumps({"error": "invalid `aaaa`", "code": 123})),
            hdrs = e.hdrs,
            fp = e.fp,
        )
        raise ex

    # print("ret ----------------")
    # print(json.dumps(response, indent=2))
    # print("body(str) ----------------")
    # print(response.get("body"))


    # 終了
    sys.exit(0)
