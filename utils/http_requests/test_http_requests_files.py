import pytest

import requests as requests_org
from myutils.http_requests import Requests as requests_my
import json as jsonlib
import os

SCRIPT_DIR = os.path.dirname(__file__)
TEST_DATA_DIR = os.path.join(SCRIPT_DIR, '_test_data')


def test_post_files():
    '''
    参考
    https://apidog.com/jp/blog/multipart-form-data/
    https://datatracker.ietf.org/doc/html/rfc7578
    '''

    payload = {}
    headers = {}
    fd1 = open(os.path.join(TEST_DATA_DIR, 'test01.txt'), 'rb')
    fd2 = open(os.path.join(TEST_DATA_DIR, 'test02.bin'), 'rb')
    files = {
        'file1': fd1,
        'file2': ('report2.xls', fd2, 'application/vnd.ms-excel', {'Expires': '0'}),
        'file3': ('report3.csv', 'some,data,to,send\nanother,row,to,send\n'),
        'file4': ('report4.csv', b'some,data,to,send\nanother,row,to,send\n'),
    }

    # 標準？ requestsの実行結果
    r1 = requests_org.post(
        'https://httpbin.org/post',
        data=payload,
        headers=headers,
        files=files,
    )
    print(r1.text)

    r1_dict = r1.json()
    assert r1_dict["data"] == ""
    assert r1_dict["form"] == {}
    assert r1_dict["json"] == None
    assert r1_dict["headers"]["Content-Type"].startswith(
        "multipart/form-data; boundary=")
    assert r1_dict["files"]["file1"] == "a\naa\naaa\n"
    assert r1_dict["files"]["file2"] == "b\nbb\nbbb\n\n"
    assert r1_dict["files"]["file3"] == "some,data,to,send\nanother,row,to,send\n"
    assert r1_dict["files"]["file4"] == "some,data,to,send\nanother,row,to,send\n"

    # 自作requestsの実行結果
    r2 = requests_my.post(
        'https://httpbin.org/post',
        data=payload,
        headers=headers,
        files=files,
    )
    print(r2.text)

    r2_dict = r2.json()
    assert r2_dict["data"] == ""
    assert r2_dict["form"] == {}
    assert r2_dict["json"] == None
    assert r2_dict["headers"]["Content-Type"].startswith(
        "multipart/form-data; boundary=")
    assert r2_dict["files"]["file1"] == "a\naa\naaa\n"
    assert r2_dict["files"]["file2"] == "b\nbb\nbbb\n\n"
    assert r2_dict["files"]["file3"] == "some,data,to,send\nanother,row,to,send\n"
    assert r2_dict["files"]["file4"] == "some,data,to,send\nanother,row,to,send\n"

    return


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
        pytest.param(
            None,
            {"key1": "value1", "key2": ["value2-1", "value2-2"]},
            "multipart/form-data; boundary=",
            "",
            {"key1": "value1", "key2": ["value2-1", "value2-2"]},
            None,
        ),
        # pytest.param(
        #     None,
        #     [("key1", "value1"), ("key2", "value2-1"),
        #      ("key2", "value2-2")],
        #     None,
        #     None,
        #     None,
        #     None,
        # ),
    ]
)
def test_post_data_with_file(content_type, payload, expect_content_type, expect_data, expect_form, expect_json):

    headers = {"Content-Type": content_type} if content_type is not None else None
    files = {
        'file3': ('report3.csv', 'some,data,to,send\nanother,row,to,send\n'),
        'file4': ('report4.tsv', b'some,data,to,send\nanother,row,to,send\n'),
    }

    # 標準？ requestsの実行結果
    r1 = requests_org.post(
        'https://httpbin.org/post',
        data=payload,
        headers=headers,
        files=files,
    )
    r1_dict = r1.json()
    assert r1_dict["data"] == expect_data
    assert r1_dict["form"] == expect_form
    assert r1_dict["json"] == expect_json
    assert r1_dict["headers"]["Content-Type"].startswith(expect_content_type)
    assert r1_dict["files"]["file3"] == "some,data,to,send\nanother,row,to,send\n"
    assert r1_dict["files"]["file4"] == "some,data,to,send\nanother,row,to,send\n"

    # 自作requestsの実行結果
    r2 = requests_my.post(
        'https://httpbin.org/post',
        data=payload,
        headers=headers,
        files=files,
    )
    print(r2.text)

    r2_dict = r2.json()
    assert r2_dict["data"] == expect_data
    assert r2_dict["form"] == expect_form
    assert r2_dict["json"] == expect_json
    assert r2_dict["headers"]["Content-Type"].startswith(expect_content_type)
    assert r2_dict["files"]["file3"] == "some,data,to,send\nanother,row,to,send\n"
    assert r2_dict["files"]["file4"] == "some,data,to,send\nanother,row,to,send\n"

    return
