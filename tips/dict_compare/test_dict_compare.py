# coding: utf-8
from dict_compare import is_contains
import re

'''
pytest: `test` で始まる関数がテスト対象になる。

usage:
  $ pytest 
  or
  $ pytest test_dict_compare.py 
'''

TEST_DATA={
    "eventVersion": "1.08",
    "userIdentity": {
        "type": "IAMUser",
        "principalId": "xxxxxxxxxxxxxxx",
        "arn": "arn:aws:iam::123456789012:user/xxxxxxxxxxxxxxx",
        "accountId": "123456789012",
        "accessKeyId": "xxxxxxxxxxxxxxx",
        "userName": "xxxxxxxxxxxxxxx"
    },
    "eventTime": "2024-02-15T06:39:03Z",
    "eventSource": "resource-groups.amazonaws.com",
    "eventName": "DeleteGroup",
    "awsRegion": "ap-northeast-1",
    "sourceIPAddress": "aaa.bbb.ccc.ddd",
    "userAgent": "APN/1.0 HashiCorp/1.0 Terraform/1.7.0 (+https://www.terraform.io) terraform-provider-aws/5.32.1 (+https://registry.terraform.io/providers/hashicorp/aws) aws-sdk-go-v2/1.24.1 os/linux lang/go#1.20.12 md/GOOS#linux md/GOARCH#amd64 api/resourcegroups#1.19.7",
    "requestParameters": {
        "GroupName": "lambda-poc"
    },
    "responseElements": {
        "Group": {
            "GroupArn": "arn:aws:resource-groups:ap-northeast-1:123456789012:group/lambda-poc",
            "Name": "lambda-poc",
            "OwnerId": "123456789012"
        }
    },
    "requestID": "428146f4-adbc-4c4d-af79-e847dd95a7e7",
    "eventID": "8c2e1158-390a-4038-be2f-28b5f67c5da6",
    "readOnly": False,
    "eventType": "AwsApiCall",
    "managementEvent": True,
    "recipientAccountId": "123456789012",
    "eventCategory": "Management"
}

def custom_condition_between(data, min, max):
    print(f"{data}")
    return bool(min <= data and data <= max)

BASE_CONDITION={
    # 単純比較
    "eventType": "AwsApiCall",
    "readOnly": False,
    # リストは、値がその中の１つにマッチしていればOK。
    "awsRegion": [
        "ap-northeast-1",
        "us-east-1",
    ],
    # dict構造はドリルダウンして比較。
    "userIdentity": {
        "type": [
            "IAMUser",
            "AssumedRole"
        ],
    },
    # 正規表現比較
    "recipientAccountId": re.compile(r'^[0-9]{12}$'),
    # カスタム条件その１
    "managementEvent": lambda x: x == True,
    # カスタム条件その２
    "eventTime": lambda x: custom_condition_between(x, "2024-01-01T00:00:00Z", "2024-12-31T23:59:59Z"),
}


def test_null_condition():
    condition = {}
    result = is_contains(TEST_DATA, condition)
    assert result == True

def test_base_condition():
    condition = BASE_CONDITION
    result = is_contains(TEST_DATA, condition)
    assert result

def test_missing_key():
    condition = {
        **BASE_CONDITION,
        "new_key": "missing",
    }
    result = is_contains(TEST_DATA, condition)
    assert not(result)

def test_umnatch_type():
    condition = {
        **BASE_CONDITION,
        "userIdentity": [
            "aaa",
            "bbb"
        ],
    }
    result = is_contains(TEST_DATA, condition)
    assert not(result)

def test_value_not_matched():
    condition = {
        **BASE_CONDITION,
        "eventType": "AwsApiCaaaall",
    }
    result = is_contains(TEST_DATA, condition)
    assert not(result)

def test_value_not_matched_regex():
    condition = {
        **BASE_CONDITION,
        "recipientAccountId": "1234567890123",
    }
    result = is_contains(TEST_DATA, condition)
    assert not(result)

def test_value_not_matched_regex():
    condition = {
        **BASE_CONDITION,
        "userIdentity": {
            "type": [
                "IAMUserr",
                "AssumedRole",
                "Unknown",
            ],
        },
    }
    result = is_contains(TEST_DATA, condition)
    assert not(result)


def test_custom_function():
    condition = {
        **BASE_CONDITION,
        "eventTime": lambda x: custom_condition_between(x, "2024-01-01T00:00:00Z", "2024-01-31T23:59:59Z"),
    }
    result = is_contains(TEST_DATA, condition)
    assert not(result)


