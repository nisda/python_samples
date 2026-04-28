from typing import List, Dict, Tuple, Any, Self
from string import Formatter
from .dot_dict import DotDict4 as DotDict
from .dot_dict import restore_dotdict
from .path_util import get_nested_data




def format_map1(expr:str, mapping:dict, original_type:bool=False):

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



# 公開するバージョンを設定
format_map = format_map1


def format_recursive(template:Any, mapping:dict, original_type:bool=False):
    """フォーマット適用（再帰処理）"""

    if isinstance(template, dict):
        return {
            k: format_recursive(template=v, mapping=mapping, original_type=original_type)
            for k,v in template.items()
        }
    elif isinstance(template, list):
        return [
            format_recursive(template=v, mapping=mapping, original_type=original_type)
            for v in template
        ]
    elif isinstance(template, tuple):
        return tuple([
            format_recursive(template=v, mapping=mapping, original_type=original_type)
            for v in template
        ])
    elif isinstance(template, str):
        return format_map(template, mapping=mapping, original_type=original_type)
    else:
        return template
