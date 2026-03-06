import pytest

from dynamodb import dynamodb_util
from dynamodb.dynamodb_util import IndexTypes
from pprint import pprint



@pytest.mark.parametrize(
    [
        "i_search_keys", "i_range_key", "e_is_match", "e_hash_keys", "e_range_keys",
    ],
    [
        pytest.param(["pk1"], None, True, ["pk1"], []),
        pytest.param(["X", "pk1", "Y"], None, True, ["pk1"], []),
        pytest.param(["pk1"], "sk1", False, None, None),
        pytest.param(["pk2"], None, False, None, None),
        pytest.param([], None, False, None, None),
    ]
)
def test_match_hash_only_x1(i_search_keys, i_range_key, e_is_match, e_hash_keys, e_range_keys):
    idx:dynamodb_util.Table = dynamodb_util.Index(
        table=None,
        name="IDX-01",
        type=None,
        hash_keys=["pk1"],
        range_keys=[],
    )

    ret = idx.containing_keys(search_keys=i_search_keys, range_compare_key=i_range_key)
    if e_is_match:
        assert isinstance(ret, dict)
        assert ret["HASH"]  == e_hash_keys
        assert ret["RANGE"] == e_range_keys
    else:
        assert ret is None



@pytest.mark.parametrize(
    [
        "i_search_keys", "i_range_key", "e_is_match", "e_hash_keys", "e_range_keys",
    ],
    [
        pytest.param(["pk1", "pk2", "pk3"], None, True, ["pk1", "pk2", "pk3"], []),
        pytest.param(["X", "pk2", "pk1", "pk3", "Y"], None, True, ["pk1", "pk2", "pk3"], []),
        pytest.param(["pk1", "pk2"], None, False, None, None),
        pytest.param(["pk1", "pk2", "pk3"], "sk1", False, None, None),
        pytest.param([], None, False, None, None),
    ]
)
def test_match_hash_only_x3(i_search_keys, i_range_key, e_is_match, e_hash_keys, e_range_keys):
    idx:dynamodb_util.Table = dynamodb_util.Index(
        table=None,
        name="IDX-01",
        type=None,
        hash_keys=["pk1", "pk2", "pk3"],
        range_keys=[],
    )

    ret = idx.containing_keys(search_keys=i_search_keys, range_compare_key=i_range_key)
    if e_is_match:
        assert isinstance(ret, dict)
        assert ret["HASH"]  == e_hash_keys
        assert ret["RANGE"] == e_range_keys
    else:
        assert ret is None


@pytest.mark.parametrize(
    [
        "i_search_keys", "i_range_key", "e_is_match", "e_hash_keys", "e_range_keys",
    ],
    [
        # Rangeキーすべて含む（OK）
        pytest.param(["A", "pk1", "pk2", "sk1", "sk2", "sk3", "X"], None, True, ["pk1", "pk2"], ["sk1", "sk2", "sk3"]),

        # Rangeキー一部含む（OK）
        pytest.param(["A", "pk1", "pk2", "sk1", "sk2", "X"], None, True, ["pk1", "pk2"], ["sk1", "sk2"]),
        pytest.param(["A", "pk1", "pk2", "sk1", "X"], None, True, ["pk1", "pk2"], ["sk1"]),

        # Rangeキーを含まない（OK）
        pytest.param(["A", "pk1", "pk2", "X"], None, True, ["pk1", "pk2"], []),

        # Rangeキーを含むが順番飛ばし -> 順番が正しいところまでOK
        pytest.param(["A", "pk1", "pk2", "X", "sk1", "sk3"], None, True, ["pk1", "pk2"], ["sk1"]),
        pytest.param(["A", "pk1", "pk2", "X", "sk2", "sk3"], None, True, ["pk1", "pk2"], []),


        # Range比較キー指定（OK）
        pytest.param(["A", "pk1", "pk2", "X"], "sk1", True, ["pk1", "pk2"], ["sk1"]),
        pytest.param(["A", "pk1", "pk2", "X", "sk1"], "sk1", True, ["pk1", "pk2"], ["sk1"]),
        pytest.param(["A", "pk1", "pk2", "X", "sk1"], "sk2", True, ["pk1", "pk2"], ["sk1", "sk2"]),
        pytest.param(["A", "pk1", "pk2", "X", "sk1", "sk2"], "sk3", True, ["pk1", "pk2"], ["sk1", "sk2", "sk3"]),

        # Range比較キーが順番飛ばし（NG）
        pytest.param(["A", "pk1", "pk2", "X"], "sk2", False, None, None),
        pytest.param(["A", "pk1", "pk2", "X", "sk2"], "sk2", False, None, None),
        pytest.param(["A", "pk1", "pk2", "X", "sk1"], "sk3", False, None, None),

        # Range比較キーが RANGE-KEY に含まれていない（NG）
        pytest.param(["A", "pk1", "pk2", "sk1", "sk2", "sk3", "X"], "sk4", False, None, None),
    ]
)
def test_match_hash_and_range(i_search_keys, i_range_key, e_is_match, e_hash_keys, e_range_keys):
    idx:dynamodb_util.Table = dynamodb_util.Index(
        table=None,
        name="IDX-01",
        type=None,
        hash_keys=["pk1", "pk2"],
        range_keys=["sk1", "sk2", "sk3"],
    )

    ret = idx.containing_keys(search_keys=i_search_keys, range_compare_key=i_range_key)
    if e_is_match:
        assert isinstance(ret, dict)
        assert ret["HASH"]  == e_hash_keys
        assert ret["RANGE"] == e_range_keys
    else:
        assert ret is None

