import pytest
from datetime import datetime
from decimal import Decimal
from syntax import Evaluater


INPUT_DATA = {
    "id"    : "00001",
    "title" : "new issue",
    "type" : [
        {"id": 11, "name": "task"},
        {"id": 22, "name": "bug"},
    ],
    "create_date" : datetime(2025, 12, 23).date(),
    "update_date" : datetime(2026, 2, 23).date(),
}



"""デフォルト動作"""
def test_default():

    template = {
        "project" : 12345,
        "id"      : "{id}",
        "content" : {
            "title"  : "{title}",
            "type_1" : "{type[0]}",
            "type_2" : "{type[1]}",
            "meta"   : {
                "created_at" : "{create_date}",
                "updated_at" : "{update_date}",
            }
        }
    }

    expect = {
        "project" : 12345,
        "id"      : "00001",
        "content" : {
            "title"  : "new issue",
            "type_1" : {"id": 11, "name": "task"},
            "type_2" : {"id": 22, "name": "bug"},
            "meta"   : {
                "created_at" : datetime(2025, 12, 23).date(),
                "updated_at" : datetime(2026, 2, 23).date(),
            }
        }
    }

    evaluater = Evaluater()
    ret = evaluater.format(template, mapping=INPUT_DATA)
    assert ret == expect
    assert type(ret) == type(expect)



"""文字列"""
def test_assign_dtype_str():

    template = {
        "project" : 12345,
        "id"      : "{id}",
        "content" : {
            "title"  : "{title}",
            "type_1" : "{type[0]}",
            "type_2" : "{type[1]}",
            "meta"   : {
                "created_at" : "{create_date}",
                "updated_at" : "{update_date}",
            }
        }
    }

    expect = {
        "project" : 12345,
        "id"      : "00001",
        "content" : {
            "title"  : "new issue",
            "type_1" : "{'id': 11, 'name': 'task'}",
            "type_2" : "{'id': 22, 'name': 'bug'}",
            "meta"   : {
                "created_at" : "2025-12-23",
                "updated_at" : "2026-02-23",
            }
        }
    }

    evaluater = Evaluater()
    ret = evaluater.format(template, mapping=INPUT_DATA, original_type=False)
    assert ret == expect
    assert type(ret) == type(expect)



"""フォーマット指定あり（強制的に文字列）"""
def test_assign_dtype_str():

    template = {
        "created_at"            : "{create_date}",
        "created_at_str"        : "_{create_date}",
        "created_at_spec"       : "{create_date:%Y%m%d}",
        # "created_at_blank_spec" : "{create_date:}",       # これは':'なしと区別がつかないため文字列化できない
    }

    expect = {
        "created_at"            : datetime(2025, 12, 23).date(),
        "created_at_str"        : "_2025-12-23",
        "created_at_spec"       : "20251223",
        # "created_at_blank_spec" : "2025-12-23",
    }

    evaluater = Evaluater()
    ret = evaluater.format(template, mapping=INPUT_DATA, original_type=True)
    assert ret == expect
    assert type(ret) == type(expect)



"""エスケープ"""
def test_escape():

    template = {
        "created_at" : "{create_date}",
        "updated_at" : "{{update_date}}",
    }

    expect = {
        "created_at" : datetime(2025, 12, 23).date(),
        "updated_at" : "{update_date}",
    }

    evaluater = Evaluater()
    ret = evaluater.format(template, mapping=INPUT_DATA)
    assert ret == expect
    assert type(ret) == type(expect)



"""再帰処理"""
@pytest.mark.parametrize(
    [
        "template", "expected",
    ],
    [
        pytest.param({"id": "{id}"}, {"id": "00001"}),                            # dict
        pytest.param(["{id}", ("{id}", "{id}")], ["00001", ("00001", "00001")]),  # list/tuple
        pytest.param("{id}", "00001"),                                            # str
    ]
)
def test_recursive(template, expected):

    evaluater = Evaluater()
    ret = evaluater.format(template, mapping=INPUT_DATA, recursive=True)
    assert ret == expected
    assert type(ret) == type(expected)



"""再帰なし"""
@pytest.mark.parametrize(
    [
        "template", "expected",
    ],
    [
        pytest.param({"id": "{id}"}, {"id": "{id}"}),                          # dict
        pytest.param(["{id}", ("{id}", "{id}")], ["{id}", ("{id}", "{id}")]),  # list/tuple
        pytest.param("{id}", "00001"),                                         # str
    ]
)
def test_not_recursive(template, expected):

    evaluater = Evaluater()
    ret = evaluater.format(template, mapping=INPUT_DATA, recursive=False)
    assert ret == expected
    assert type(ret) == type(expected)





"""エラー/handling"""
@pytest.mark.parametrize(
    [
        "template", "errors", "expected"
    ],
    [
        pytest.param({"id": "{id}", "unknown": "{ID}"}, 'coerce', {"id": "00001", "unknown": None}),
        pytest.param({"id": "{id}", "unknown": "{ID}"}, 'ignore', {"id": "00001", "unknown": "{ID}"}),
    ]
)
def test_error_handling(template, errors, expected):

    evaluater = Evaluater()
    ret = evaluater.format(template, mapping=INPUT_DATA, errors=errors)
    assert ret == expected
    assert type(ret) == type(expected)


"""エラー/raise"""
@pytest.mark.parametrize(
    [
        "template",  "e_type", "e_msg"
    ],
    [
        # オリジナルタイプ
        pytest.param({"id": "{id}", "unknown": "{ID}"}, KeyError, "\"'ID'. occurred at expression='{ID}'\""),
        pytest.param({"id": "{id}", "unknown": "{type[999]}"}, IndexError, "list index out of range. occurred at expression='{type[999]}'"),

        # str
        pytest.param({"id": "{id}", "unknown": "_{ID}"}, KeyError, "\"'ID'. occurred at expression='_{ID}'\""),
        pytest.param({"id": "{id}", "unknown": "_{type[999]}"}, IndexError, "list index out of range. occurred at expression='_{type[999]}'"),

        # フォーマット不備（str）
        pytest.param({"id": "{id}", "unknown": "{type[aaa}"}, SyntaxError, "closing parenthesis '}' does not match opening parenthesis '[' (<unknown>, line 1). occurred at expression='{type[aaa}'"),
        pytest.param({"id": "{id}", "unknown": "{id:xyz}"}, ValueError, "Invalid format specifier 'xyz' for object of type 'str'. occurred at expression='{id:xyz}'"),
    ]
)
def test_error_handling(template, e_type, e_msg):

    evaluater = Evaluater()
    with pytest.raises(Exception) as e:
        ret = evaluater.format(template, mapping=INPUT_DATA, errors='raise')
    assert str(e.value) == e_msg
    assert e.type == e_type



