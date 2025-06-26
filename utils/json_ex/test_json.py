import myutils.json_ex as json  # import test-target
import pytest
import datetime
import decimal
import uuid
import os
import pathlib

# 共通設定
WORK_DIR = os.path.join(os.path.dirname(__file__), '_test_data')


@pytest.mark.parametrize(
    ["input", "expect_type", "expect_value"],
    [

        # datetime
        pytest.param(
            datetime.datetime(2025, 2, 15, 12, 34, 56),
            str, "2025-02-15T12:34:56"),

        # date
        pytest.param(
            datetime.date(2025, 2, 15),
            str, "2025-02-15"),

        # time
        pytest.param(
            datetime.time(12, 34, 56),
            str, "12:34:56"),

        # decimal
        pytest.param(decimal.Decimal(123), int, 123),
        pytest.param(decimal.Decimal(123.00), int, 123),
        pytest.param(decimal.Decimal(123.45), float, 123.45),

        # uuid
        pytest.param(
            uuid.UUID("93035c19-d9bb-4c69-8785-5463ec60a3df"),
            str, "93035c19-d9bb-4c69-8785-5463ec60a3df"),

        # byte
        pytest.param(b'test', str, 'test')
    ]
)
def test_serialize(input, expect_type, expect_value):
    json_str = json.dumps(input)
    ret = json.loads(json_str)
    assert isinstance(ret, expect_type)
    assert expect_value == ret


def test_batch_dump_serialize():
    '''dump: シリアライズ'''

    output_dir: str = os.path.join(WORK_DIR, 'test_batch_dump_serialize')
    data = {
        'dict': {'a': 'AAA'},
        'string': "sample message",
        'datetime': datetime.datetime(2025, 2, 15, 12, 34, 56),
        'uuid': uuid.UUID("93035c19-d9bb-4c69-8785-5463ec60a3df"),
        "null": None,
    }
    json.batch_dump(dir_path=output_dir, data=data)

    # ファイルが存在することを持ってOKとする。
    assert os.path.exists(os.path.join(output_dir, "dict.json"))
    assert os.path.exists(os.path.join(output_dir, "string.json"))
    assert os.path.exists(os.path.join(output_dir, "datetime.json"))
    assert os.path.exists(os.path.join(output_dir, "uuid.json"))
    assert os.path.exists(os.path.join(output_dir, "null.json"))


def test_batch_dump_replace():
    '''dump: ディレクトリ内の洗い替え'''
    output_dir: str = os.path.join(WORK_DIR, 'test_batch_dump_replace')

    # 既存ファイルを作成
    os.makedirs(output_dir, exist_ok=True)
    existing_file_paths = [
        os.path.join(output_dir, "a.json"),
        os.path.join(output_dir, "b.txt"),
    ]
    for path in existing_file_paths:
        p = pathlib.Path(path)
        p.touch()
        assert os.path.exists(path)

    # dump出力（テスト対象）
    data = {
        'dict': {'a': 'AAA'},
        'string': "sample message",
    }
    json.batch_dump(dir_path=output_dir, data=data)

    # dumpファイル存在チェック
    assert os.path.exists(os.path.join(output_dir, "dict.json"))
    assert os.path.exists(os.path.join(output_dir, "string.json"))

    # 既存ファイル非存在チェック
    for path in existing_file_paths:
        assert not os.path.exists(path)


def test_batch_load():
    '''ファイル読み込み'''

    output_dir: str = os.path.join(WORK_DIR, 'test_batch_load')

    # 先に出力。batch_dump は正常動作する前提
    data = {
        'dict': {'a': 'AAA'},
        'string': "sample message",
        'datetime': datetime.datetime(2025, 2, 15, 12, 34, 56),
        'uuid': uuid.UUID("93035c19-d9bb-4c69-8785-5463ec60a3df"),
        "null": None,
    }
    json.batch_dump(dir_path=output_dir, data=data)

    # 読み込み（テスト対象）
    ret = json.batch_load(dir_path=output_dir)
    assert ret['dict'] == {'a': 'AAA'}
    assert ret['string'] == "sample message"
    assert ret['datetime'] == "2025-02-15T12:34:56"
    assert ret['uuid'] == "93035c19-d9bb-4c69-8785-5463ec60a3df"
    assert ret["null"] is None


def test_sort():
    input = {"c": "789", "a": "1234", "b": "852"}
    expect = {"a": "1234", "b": "852", "c": "789"}

    input_str = json.dumps(input, sort_keys=False)
    sorted_str = json.dumps(input, sort_keys=True)
    expect_str = json.dumps(expect)

    assert input_str != sorted_str
    assert input_str != expect_str
    assert sorted_str == expect_str
