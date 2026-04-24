from typing import List, Dict, Tuple, Any, Self
from string import Formatter
from .dot_dict import DotDict4 as DotDict
from .dot_dict import restore_dotdict


def format_map(expr:str, mapping:dict, original_type:bool=False, allow_missing:bool=False):

    # original_type 返却可否の判定
    is_original_type_convertible = False
    if original_type:
        # format(expr) を分解
        elements = [
            { 'literal_text': l, 'field_name': f, 'format_spec': s, 'conversion': c}
            for l, f, s, c in Formatter().parse(expr)
        ]
        # １要素のみ, field_name のみの場合に元タイプ変換可能
        is_original_type_convertible = bool(
            len(elements) == 1
            and not elements[0]['literal_text']
            and not elements[0]['format_spec']
            and elements[0]['field_name']
        )

    # データを変換ドット連結可能な方式に変換
    data = DotDict(mapping)

    # format 実行
    if is_original_type_convertible:
        # オリジナルタイプ返却の場合は'{}'を削除してeval実行
        ret = eval(expr[1:-1], {}, data)
        return restore_dotdict(ret) # dotdict から元の dict に戻す。

    elif advanced := False:
        # 必ず False になる。通らない。
        # この方法であればプレースホルダー内で function も使えそうだが当面は公開しない。
        # f-string と format() では template の書式が若干違うため仕様検討が必要。

        # format実行（eval: f-string）
        return eval(f'f"{expr}"', {}, data)

    else:
        return expr.format_map(data)



