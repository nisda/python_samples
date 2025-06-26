from typing import Any


def compare(value_left:Any, value_right:Any) -> int:
    """
    複数のデータ型に対応した比較処理
    
    Notes
    -----
    数値型は int, float, Decimal に対応。型を問わずに比較する。
    それ以外の型は同じ型に限り値で比較する。
    異なる型の場合は型で優先度をつける。優先度はあらかじめ決められており指定不可。
    比較演算子が使えない型の比較では Exception が発生する。
    """

    # 型の優先度。未定義の型は型名で比較。
    type_others = ["bool", "str", "bytes", "UUID"]
    type_numbers = ["int", "float", "Decimal"]

    # 型名を取得
    type_left = type(value_left).__name__
    type_right = type(value_right).__name__


    # 両方が数値型であればそのまま比較
    if (type_left in type_numbers) and (type_right in type_numbers):
        if value_left < value_right: return -1
        if value_left > value_right: return 1
        else: return 0

    # 型をマージ
    type_merged = [*type_numbers, *type_others]

    # それぞれの型の優先度を取得
    priority_left = type_merged.index(type_left) if type_left in type_merged else 100
    priority_right = type_merged.index(type_right) if type_right in type_merged else 100

    # 両方が未定義型の場合
    if ( priority_left == 100 ) and ( priority_right == 100 ):
        # まずは型名で比較
        if type_left < type_right: return -1
        if type_left > type_right: return 1
        # 同じ型の場合は値を比較
        if value_left < value_right: return -1
        if value_left > value_right: return 1
        return 0

    # 両方の型が同じ場合
    if priority_left == priority_right:
        # 値を比較
        if value_left < value_right: return -1
        if value_left > value_right: return 1
        return 0

    # それ以外＝型が異なる場合は、型の優先度で比較
    if priority_left < priority_right: return -1
    if priority_left > priority_right: return 1
    return 0

