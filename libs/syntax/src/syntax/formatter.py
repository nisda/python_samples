from typing import Any, Dict, List, Callable, Tuple, Literal, Type
import ast
import operator
import sys
import builtins
from .evaluater import Evaluater
from string import Formatter as Formatter


class FormatterPlus(Evaluater):



    # def assign_data(self, expr:str, context:Dict[str, Any], original_type:bool=True):
    #     if self.__is_fieldname_only(expr) and original_type:
    #         return self.evaluate(expr=expr[1:-1], context=context)
    #     else:
    #         escaped_expr = expr.replace('"', '\\"')
    #         return self.evaluate(expr=f'f"{escaped_expr}"', context=context)



    def format(
            self,
            template:str|Dict|List|Tuple,
            /,
            mapping:Dict[str, Any],
            recursive:bool = True,
            original_type:bool=True,
            errors:Literal['raise', 'coerce', 'ignore']='raise',
        ) -> Any:
        """テンプレートへのデータマッピング（再帰実行可）"""


        # オリジナルタイプ変換可否関数
        def __is_fieldname_only(expr:str) -> bool:
            try:
                # format(expr) を分解
                elements = [
                    dict(zip(['literal_text', 'field_name', 'format_spec', 'conversion'], p))
                    for p in Formatter().parse(expr)
                ]
                # １要素のみ且つ field_name のみである
                ret = bool(
                    len(elements) == 1
                    and not elements[0]['literal_text']
                    and not elements[0]['format_spec']
                    and not elements[0]['conversion']
                    and elements[0]['field_name']
                )
                return ret
            except Exception as e:
                return False


        # データ割り当て関数
        def __assign_data(expr:str, mapping:Dict):
            try:
                if original_type and self.__is_fieldname_only(expr):
                    return self.evaluate(expr[1:-1], context=mapping)
                else:
                    try:
                        escaped_expr = expr.replace('"', '\\"')
                        return self.evaluate(f'f"{escaped_expr}"', context=mapping)
                    except Exception as e:
                        e_type:Type = type(e)
                        e_msg:str   = f"{str(e).rstrip('.')}. occurred at expression='{expr}'"
                        raise e_type(e_msg) from e
            except Exception as e:
                if errors == 'coerce':
                    return None
                elif errors == 'ignore':
                    return expr
                else:
                    raise

        # パラメータまとめ
        common_params = {
            "mapping" : mapping,
            "recursive" : recursive,
            "original_type" : original_type,
            "errors" : errors,
        }

        # タイプ別に再帰実行
        if isinstance(template, Dict):
            return {
                k: self.format(template, **common_params)
                for k,v in template.items()
            }
        elif isinstance(template, List):
            return [
                self.format(template, **common_params)
                for v in template
            ]
        elif isinstance(template, Tuple):
            return tuple(
                self.format(template, **common_params)
                for v in template
            )
        elif isinstance(template, str):
            return __assign_data(template, mapping=mapping)
        else:
            return template

