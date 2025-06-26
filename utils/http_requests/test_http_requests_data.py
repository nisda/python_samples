import pytest

import requests as requests_org
from myutils.http_requests import Requests as requests_my
import json as jsonlib


@pytest.mark.parametrize(
    [
        "content_type",
        "payload",
        "expect_content_type",
        "expect_data",
        "expect_form",
        "expect_json"
    ],
    [
        # ---------------------------------------
        # データパターン：Dict（List値を含む）
        # ---------------------------------------
        pytest.param(
            None,
            {'key1': ['value1-1', 'value1-2'], 'key2': 'value2'},
            'application/x-www-form-urlencoded',
            '',
            {'key1': ['value1-1', 'value1-2'], 'key2': 'value2'},
            None,
        ),
        pytest.param(
            'application/x-www-form-urlencoded',
            {'key1': ['value1-1', 'value1-2'], 'key2': 'value2'},
            'application/x-www-form-urlencoded',
            '',
            {'key1': ['value1-1', 'value1-2'], 'key2': 'value2'},
            None,
        ),
        pytest.param(
            'application/json',
            {'key1': ['value1-1', 'value1-2'], 'key2': 'value2'},
            'application/json',
            "key1=value1-1&key1=value1-2&key2=value2",
            {},
            None,
        ),
        pytest.param(
            'text/plain',
            {'key1': ['value1-1', 'value1-2'], 'key2': 'value2'},
            'text/plain',
            "key1=value1-1&key1=value1-2&key2=value2",
            {},
            None,
        ),
        pytest.param(
            'application/octet-stream',
            {'key1': ['value1-1', 'value1-2'], 'key2': 'value2'},
            'application/octet-stream',
            "key1=value1-1&key1=value1-2&key2=value2",
            {},
            None,
        ),
        # ---------------------------------------
        # データパターン：Tuples
        # ---------------------------------------
        pytest.param(
            None,
            [('key1', 'value1-1'), ('key1', 'value1-2'), ('key2', 'value2')],
            'application/x-www-form-urlencoded',
            '',
            {'key1': ['value1-1', 'value1-2'], 'key2': 'value2'},
            None,
        ),
        pytest.param(
            'application/x-www-form-urlencoded',
            [('key1', 'value1-1'), ('key1', 'value1-2'), ('key2', 'value2')],
            'application/x-www-form-urlencoded',
            '',
            {'key1': ['value1-1', 'value1-2'], 'key2': 'value2'},
            None,
        ),
        pytest.param(
            'application/json',
            [('key1', 'value1-1'), ('key1', 'value1-2'), ('key2', 'value2')],
            'application/json',
            "key1=value1-1&key1=value1-2&key2=value2",
            {},
            None,
        ),
        pytest.param(
            'text/plain',
            [('key1', 'value1-1'), ('key1', 'value1-2'), ('key2', 'value2')],
            'text/plain',
            "key1=value1-1&key1=value1-2&key2=value2",
            {},
            None,
        ),
        pytest.param(
            'application/octet-stream',
            [('key1', 'value1-1'), ('key1', 'value1-2'), ('key2', 'value2')],
            'application/octet-stream',
            "key1=value1-1&key1=value1-2&key2=value2",
            {},
            None,
        ),
        # ---------------------------------------
        # データパターン：文字列
        # ---------------------------------------
        pytest.param(
            None,
            "サンプルテキスト",
            None,
            "サンプルテキスト",
            {},
            None,
        ),
        pytest.param(
            'application/x-www-form-urlencoded',
            "サンプルテキスト",
            'application/x-www-form-urlencoded',
            '',
            {'サンプルテキスト': ''},
            None,
        ),
        pytest.param(
            'application/json',
            "サンプルテキスト",
            'application/json',
            "サンプルテキスト",
            {},
            None,
        ),
        pytest.param(
            'text/plain',
            "サンプルテキスト",
            'text/plain',
            "サンプルテキスト",
            {},
            None,
        ),
        pytest.param(
            'application/octet-stream',
            "サンプルテキスト",
            'application/octet-stream',
            "サンプルテキスト",
            {},
            None,
        ),
        # ---------------------------------------
        # データパターン：バイナリ
        # ---------------------------------------
        pytest.param(
            None,
            b'sample text',
            None,
            'sample text',
            {},
            None,
        ),
        pytest.param(
            'application/x-www-form-urlencoded',
            b'sample text',
            'application/x-www-form-urlencoded',
            '',
            {'sample text': ''},
            None,
        ),
        pytest.param(
            'application/json',
            b'sample text',
            'application/json',
            'sample text',
            {},
            None,
        ),
        pytest.param(
            'text/plain',
            b'sample text',
            'text/plain',
            'sample text',
            {},
            None,
        ),
        pytest.param(
            'application/octet-stream',
            b'sample text',
            'application/octet-stream',
            'sample text',
            {},
            None,
        ),
        # ---------------------------------------
        # データパターン：None
        # ---------------------------------------
        pytest.param(
            None,
            None,
            None,
            '',
            {},
            None,
        ),
        pytest.param(
            'application/x-www-form-urlencoded',
            None,
            'application/x-www-form-urlencoded',
            '',
            {},
            None,
        ),
        pytest.param(
            'application/json',
            None,
            'application/json',
            '',
            {},
            None,
        ),
        pytest.param(
            'text/plain',
            None,
            'text/plain',
            '',
            {},
            None,
        ),
        pytest.param(
            'application/octet-stream',
            None,
            'application/octet-stream',
            '',
            {},
            None,
        ),
        # ---------------------------------------
        # データパターン：chaeset
        # ---------------------------------------
        pytest.param(
            'application/x-www-form-urlencoded; chaeset=sfift-jis',
            "サンプルテキスト",
            'application/x-www-form-urlencoded; chaeset=sfift-jis',
            '',
            {'サンプルテキスト': ''},
            None,
        ),
        pytest.param(
            'application/json; chaeset=sfift-jis',
            "サンプルテキスト",
            'application/json; chaeset=sfift-jis',
            "サンプルテキスト",
            {},
            None,
        ),
        pytest.param(
            'text/plain; chaeset=sfift-jis',
            "サンプルテキスト",
            'text/plain; chaeset=sfift-jis',
            "サンプルテキスト",
            {},
            None,
        ),
        pytest.param(
            'application/octet-stream; chaeset=sfift-jis',
            "サンプルテキスト",
            'application/octet-stream; chaeset=sfift-jis',
            "サンプルテキスト",
            {},
            None,
        ),

    ]
)
def test_post_data(content_type, payload, expect_content_type, expect_data, expect_form, expect_json):
    '''dictデータ'''

    # ヘッダをセット
    headers = {"content-type": content_type} if content_type is not None else None

    r1 = requests_org.post(
        'https://httpbin.org/post',
        data=payload,
        headers=headers
    )
    print(r1.text)
    r1_dict = r1.json()
    assert expect_content_type == r1_dict["headers"].get("Content-Type", None)
    assert expect_data == r1_dict["data"]
    assert expect_form == r1_dict["form"]
    assert expect_json == r1_dict["json"]

    r2 = requests_my.post(
        'https://httpbin.org/post',
        data=payload,
        headers=headers
    )
    print(r2.text)
    r2_dict = r2.json()
    assert expect_content_type == r2_dict["headers"].get("Content-Type", None)
    assert expect_data == r2_dict["data"]
    assert expect_form == r2_dict["form"]
    assert expect_json == r2_dict["json"]

    return
