import boto3
from boto3 import Session
import json


TABLE_NAME:str = "test-20260128"

session:Session = boto3.Session(region_name="ap-northeast-2")

dynamodb_cli = session.client("dynamodb", region_name="ap-northeast-1")
dynamodb_rsc = session.resource("dynamodb", region_name="ap-northeast-1")


def get_item(client):
    response = client.get_item(
        **{
            'Key': {
                'pk': {
                    'S': 'ut_put',
                },
                'sk': {
                    'S': 'overwrite',
                }
            },
            'TableName': TABLE_NAME,
        }
    )
    return response["Item"]



def transact_get_items(client):
    response = client.transact_get_items(
        TransactItems=[
            {
                'Get': {
                    'Key': {
                        'pk': {
                            'S': 'ut_put',
                        },
                        'sk': {
                            'S': 'overwrite',
                        }
                    },
                    'TableName': TABLE_NAME,
                }
            },
        ],
    )
    return response["Items"]

def transact_put_items(client):
    response = client.transact_write_items(
        TransactItems=[
            {
                'ConditionCheck': {
                    'Key': {
                        'string': {
                            'S': 'string',
                            'N': 'string',
                            'B': b'bytes',
                            'SS': [
                                'string',
                            ],
                            'NS': [
                                'string',
                            ],
                            'BS': [
                                b'bytes',
                            ],
                            'M': {
                                'string': {'... recursive ...'}
                            },
                            'L': [
                                {'... recursive ...'},
                            ],
                            'NULL': True|False,
                            'BOOL': True|False
                        }
                    },
                    'TableName': 'string',
                    'ConditionExpression': 'string',
                    'ExpressionAttributeNames': {
                        'string': 'string'
                    },
                    'ExpressionAttributeValues': {
                        'string': {
                            'S': 'string',
                            'N': 'string',
                            'B': b'bytes',
                            'SS': [
                                'string',
                            ],
                            'NS': [
                                'string',
                            ],
                            'BS': [
                                b'bytes',
                            ],
                            'M': {
                                'string': {'... recursive ...'}
                            },
                            'L': [
                                {'... recursive ...'},
                            ],
                            'NULL': True|False,
                            'BOOL': True|False
                        }
                    },
                    'ReturnValuesOnConditionCheckFailure': 'ALL_OLD'|'NONE'
                },
                'Put': {
                    'Item': {
                        'string': {
                            'S': 'string',
                            'N': 'string',
                            'B': b'bytes',
                            'SS': [
                                'string',
                            ],
                            'NS': [
                                'string',
                            ],
                            'BS': [
                                b'bytes',
                            ],
                            'M': {
                                'string': {'... recursive ...'}
                            },
                            'L': [
                                {'... recursive ...'},
                            ],
                            'NULL': True|False,
                            'BOOL': True|False
                        }
                    },
                    'TableName': 'string',
                    'ConditionExpression': 'string',
                    'ExpressionAttributeNames': {
                        'string': 'string'
                    },
                    'ExpressionAttributeValues': {
                        'string': {
                            'S': 'string',
                            'N': 'string',
                            'B': b'bytes',
                            'SS': [
                                'string',
                            ],
                            'NS': [
                                'string',
                            ],
                            'BS': [
                                b'bytes',
                            ],
                            'M': {
                                'string': {'... recursive ...'}
                            },
                            'L': [
                                {'... recursive ...'},
                            ],
                            'NULL': True|False,
                            'BOOL': True|False
                        }
                    },
                    'ReturnValuesOnConditionCheckFailure': 'ALL_OLD'|'NONE'
                },
                'Delete': {
                    'Key': {
                        'string': {
                            'S': 'string',
                            'N': 'string',
                            'B': b'bytes',
                            'SS': [
                                'string',
                            ],
                            'NS': [
                                'string',
                            ],
                            'BS': [
                                b'bytes',
                            ],
                            'M': {
                                'string': {'... recursive ...'}
                            },
                            'L': [
                                {'... recursive ...'},
                            ],
                            'NULL': True|False,
                            'BOOL': True|False
                        }
                    },
                    'TableName': 'string',
                    'ConditionExpression': 'string',
                    'ExpressionAttributeNames': {
                        'string': 'string'
                    },
                    'ExpressionAttributeValues': {
                        'string': {
                            'S': 'string',
                            'N': 'string',
                            'B': b'bytes',
                            'SS': [
                                'string',
                            ],
                            'NS': [
                                'string',
                            ],
                            'BS': [
                                b'bytes',
                            ],
                            'M': {
                                'string': {'... recursive ...'}
                            },
                            'L': [
                                {'... recursive ...'},
                            ],
                            'NULL': True|False,
                            'BOOL': True|False
                        }
                    },
                    'ReturnValuesOnConditionCheckFailure': 'ALL_OLD'|'NONE'
                },
                'Update': {
                    'Key': {
                        'string': {
                            'S': 'string',
                            'N': 'string',
                            'B': b'bytes',
                            'SS': [
                                'string',
                            ],
                            'NS': [
                                'string',
                            ],
                            'BS': [
                                b'bytes',
                            ],
                            'M': {
                                'string': {'... recursive ...'}
                            },
                            'L': [
                                {'... recursive ...'},
                            ],
                            'NULL': True|False,
                            'BOOL': True|False
                        }
                    },
                    'UpdateExpression': 'string',
                    'TableName': 'string',
                    'ConditionExpression': 'string',
                    'ExpressionAttributeNames': {
                        'string': 'string'
                    },
                    'ExpressionAttributeValues': {
                        'string': {
                            'S': 'string',
                            'N': 'string',
                            'B': b'bytes',
                            'SS': [
                                'string',
                            ],
                            'NS': [
                                'string',
                            ],
                            'BS': [
                                b'bytes',
                            ],
                            'M': {
                                'string': {'... recursive ...'}
                            },
                            'L': [
                                {'... recursive ...'},
                            ],
                            'NULL': True|False,
                            'BOOL': True|False
                        }
                    },
                    'ReturnValuesOnConditionCheckFailure': 'ALL_OLD'|'NONE'
                }
            },
        ],
    )


res = get_item(client=dynamodb_cli)
print(json.dumps(res, indent=2))
