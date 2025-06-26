import pytest

import requests as requests_org
from myutils.http_requests import Requests as requests_my
import datetime
import json as jsonlib

'''
ここに書いてある内容をテストケースにする。
他に必要があれば追加する。
https://requests.readthedocs.io/en/latest/user/quickstart/
'''


def __conv_response_for_comp(response: dict) -> dict:
    '''テスト用共通処理：比較用にデータ調整'''
    # ヘッダ調整
    ignore_headers: list = [
        x.lower() for x in ("User-Agent", "X-Amzn-Trace-Id")
    ]
    for k in response["headers"].keys():
        if k.lower() in ignore_headers:
            response["headers"][k] = '*** Not comparable ***'

    # 返却
    return response


def test_basic_response():
    '''基本的なレスポンス'''

    # 元ライブラリの実行
    r1 = requests_org.get('https://httpbin.org/get')

    # 自作ライブラリの実行
    r2 = requests_my.get('https://httpbin.org/get')
    assert r2.url == "https://httpbin.org/get"
    assert r2.status_code == 200
    assert len(r2.headers['Content-type']) > 0
    assert len(r2.headers.get('content-type')) > 0

    # 結果比較

    assert r1.url == r2.url
    assert r1.status_code == r2.status_code

    r1_dict = __conv_response_for_comp(r1.json())
    r2_dict = __conv_response_for_comp(r2.json())

    assert r1_dict == r2_dict

    return


@pytest.mark.parametrize(
    ["payload", "expect_url"],
    [
        pytest.param(
            {'key1': 'value1', 'key2': 'value2'},
            "https://httpbin.org/get?key1=value1&key2=value2",
        ),
        pytest.param(
            {'key1': 'value1', 'key2': ['value2', 'value3']},
            "https://httpbin.org/get?key1=value1&key2=value2&key2=value3",
        ),

    ]
)
def test_get_qs(payload, expect_url):
    '''クエリーストリング'''

    payload = payload
    r1 = requests_my.get('https://httpbin.org/get', params=payload)
    r2 = requests_org.get('https://httpbin.org/get', params=payload)
    print(r1.text)
    print(r2.text)

    assert r1.url == expect_url
    assert r1.url == r2.url

    r1_dict = __conv_response_for_comp(r1.json())
    r2_dict = __conv_response_for_comp(r2.json())
    assert r1_dict == r2_dict

    return


def test_custom_headers():
    headers = {'user-agent': 'my-app/0.0.1'}

    r1 = requests_my.get('https://httpbin.org/get', headers=headers)
    r2 = requests_org.get('https://httpbin.org/get', headers=headers)
    print(r1.text)
    print(r2.text)

    assert r1.json().get("headers").get('User-Agent') == 'my-app/0.0.1'

    r1_dict = __conv_response_for_comp(r1.json())
    r2_dict = __conv_response_for_comp(r2.json())
    assert r1_dict == r2_dict

    return
