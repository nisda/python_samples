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
            'application/json',
            jsonlib.dumps(
                {'key1': ['value1-1', 'value1-2'], 'key2': 'value2'}),
            {},
            {'key1': ['value1-1', 'value1-2'], 'key2': 'value2'},
        ),
        pytest.param(
            'application/x-www-form-urlencoded',
            {'key1': ['value1-1', 'value1-2'], 'key2': 'value2'},
            'application/x-www-form-urlencoded',
            '',
            {jsonlib.dumps(
                {'key1': ['value1-1', 'value1-2'], 'key2': 'value2'}): ''},
            None,
        ),
        pytest.param(
            'application/json',
            {'key1': ['value1-1', 'value1-2'], 'key2': 'value2'},
            'application/json',
            jsonlib.dumps(
                {'key1': ['value1-1', 'value1-2'], 'key2': 'value2'}),
            {},
            {'key1': ['value1-1', 'value1-2'], 'key2': 'value2'},
        ),
        pytest.param(
            'text/plain',
            {'key1': ['value1-1', 'value1-2'], 'key2': 'value2'},
            'text/plain',
            jsonlib.dumps(
                {'key1': ['value1-1', 'value1-2'], 'key2': 'value2'}),
            {},
            {'key1': ['value1-1', 'value1-2'], 'key2': 'value2'},
        ),
        pytest.param(
            'application/octet-stream',
            {'key1': ['value1-1', 'value1-2'], 'key2': 'value2'},
            'application/octet-stream',
            jsonlib.dumps(
                {'key1': ['value1-1', 'value1-2'], 'key2': 'value2'}),
            {},
            {'key1': ['value1-1', 'value1-2'], 'key2': 'value2'},
        ),
        # ---------------------------------------
        # データパターン：Tuples
        # ---------------------------------------
        pytest.param(
            None,
            [('key1', 'value1-1'), ('key1', 'value1-2'), ('key2', 'value2')],
            'application/json',
            jsonlib.dumps(
                [["key1", "value1-1"], ["key1", "value1-2"], ["key2", "value2"]]),
            {},
            [["key1", "value1-1"], ["key1", "value1-2"], ["key2", "value2"]],
        ),
        pytest.param(
            'application/x-www-form-urlencoded',
            [('key1', 'value1-1'), ('key1', 'value1-2'), ('key2', 'value2')],
            'application/x-www-form-urlencoded',
            '',
            {'[["key1", "value1-1"], ["key1", "value1-2"], ["key2", "value2"]]': ''},
            None,
        ),
        pytest.param(
            'application/json',
            [('key1', 'value1-1'), ('key1', 'value1-2'), ('key2', 'value2')],
            'application/json',
            jsonlib.dumps(
                [["key1", "value1-1"], ["key1", "value1-2"], ["key2", "value2"]]),
            {},
            [["key1", "value1-1"], ["key1", "value1-2"], ["key2", "value2"]],
        ),
        pytest.param(
            'text/plain',
            [('key1', 'value1-1'), ('key1', 'value1-2'), ('key2', 'value2')],
            'text/plain',
            jsonlib.dumps(
                [["key1", "value1-1"], ["key1", "value1-2"], ["key2", "value2"]]),
            {},
            [["key1", "value1-1"], ["key1", "value1-2"], ["key2", "value2"]],
        ),
        pytest.param(
            'application/octet-stream',
            [('key1', 'value1-1'), ('key1', 'value1-2'), ('key2', 'value2')],
            'application/octet-stream',
            jsonlib.dumps(
                [["key1", "value1-1"], ["key1", "value1-2"], ["key2", "value2"]]),
            {},
            [["key1", "value1-1"], ["key1", "value1-2"], ["key2", "value2"]],
        ),
        # ---------------------------------------
        # データパターン：文字列
        # ---------------------------------------
        pytest.param(
            None,
            "サンプルテキスト",
            'application/json',
            jsonlib.dumps("サンプルテキスト"),
            {},
            "サンプルテキスト",
        ),
        pytest.param(
            'application/x-www-form-urlencoded',
            "サンプルテキスト",
            'application/x-www-form-urlencoded',
            '',
            {jsonlib.dumps('サンプルテキスト'): ''},
            None,
        ),
        pytest.param(
            'application/json',
            "サンプルテキスト",
            'application/json',
            jsonlib.dumps("サンプルテキスト"),
            {},
            "サンプルテキスト",
        ),
        pytest.param(
            'text/plain',
            "サンプルテキスト",
            'text/plain',
            jsonlib.dumps("サンプルテキスト"),
            {},
            "サンプルテキスト",
        ),
        pytest.param(
            'application/octet-stream',
            "サンプルテキスト",
            'application/octet-stream',
            jsonlib.dumps("サンプルテキスト"),
            {},
            "サンプルテキスト",
        ),
        # ---------------------------------------
        # データパターン：バイナリ　-> # 内部処理でエラーになるためリクエスト実行不可
        # ---------------------------------------
        # pytest.param(
        #     None,
        #     b'sample text',
        #     'application/json',
        #     'sample text',
        #     {},
        #     'sample text',
        # ),
        # pytest.param(
        #     'application/x-www-form-urlencoded',
        #     b'sample text',
        #     'application/x-www-form-urlencoded',
        #     '',
        #     {'sample text': ''},
        #     None,
        # ),
        # pytest.param(
        #     'application/json',
        #     b'sample text',
        #     'application/json',
        #     'sample text',
        #     {},
        #     None,
        # ),
        # pytest.param(
        #     'text/plain',
        #     b'sample text',
        #     'text/plain',
        #     'sample text',
        #     {},
        #     None,
        # ),
        # pytest.param(
        #     'application/octet-stream',
        #     b'sample text',
        #     'application/octet-stream',
        #     'sample text',
        #     {},
        #     None,
        # ),
        # ---------------------------------------
        # データパターン：None
        #   -> json=None の場合は data が優先処理される。
        #      data=None と同じ結果となることを確認する。
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
            'application/x-www-form-urlencoded; charset=shift_jis',
            "サンプルテキスト",
            'application/x-www-form-urlencoded; charset=shift_jis',
            '',
            {jsonlib.dumps('サンプルテキスト'): ''},
            None,
        ),
        pytest.param(
            'application/json; charset=shift_jis',
            "サンプルテキスト",
            'application/json; charset=shift_jis',
            jsonlib.dumps("サンプルテキスト"),
            {},
            "サンプルテキスト",
        ),
        pytest.param(
            'text/plain; charset=shift_jis',
            "サンプルテキスト",
            'text/plain; charset=shift_jis',
            jsonlib.dumps("サンプルテキスト"),
            {},
            "サンプルテキスト",
        ),
        pytest.param(
            'application/octet-stream; charset=shift_jis',
            "サンプルテキスト",
            'application/octet-stream; charset=shift_jis',
            jsonlib.dumps("サンプルテキスト"),
            {},
            "サンプルテキスト",
        ),
    ]
)
def test_post_json(content_type, payload, expect_content_type, expect_data, expect_form, expect_json):
    '''dictデータ'''

    # ヘッダをセット
    headers = {"content-type": content_type} if content_type is not None else None

    r1 = requests_org.post(
        'https://httpbin.org/post',
        json=payload,
        headers=headers
    )
    print(r1.text)
    r1_dict = r1.json()
    assert r1_dict["headers"].get("Content-Type", None) == expect_content_type
    assert r1_dict["data"] == expect_data
    assert r1_dict["form"] == expect_form
    assert r1_dict["json"] == expect_json

    r2 = requests_my.post(
        'https://httpbin.org/post',
        json=payload,
        headers=headers
    )
    print(r2.text)
    r2_dict = r2.json()
    assert r2_dict["headers"].get("Content-Type", None) == expect_content_type
    assert r2_dict["data"] == expect_data
    assert r2_dict["form"] == expect_form
    assert r2_dict["json"] == expect_json

    return
