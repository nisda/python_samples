from typing import List, Dict, Any

def update_expression(
        set_item:Dict[str, Any]=None,
        add_item:Dict[str, Any]=None,
        remove_item:List[str]=None
    ):

    # INPUTパラメータの調整
    set_item    = set_item or {}
    remove_item = remove_item or []
    add_item    = add_item or {}

    # 更新情報の生成
    update_expressions:List[str] = []

    set_expressions:List    = [ f"#{k} = :{k}" for k in set_item.keys()]
    set_attr_names:dict     = { f"#{k}":k for k in set_item.keys() }
    set_attr_values:dict    = { f":{k}":v for k,v in set_item.items() }
    if len(set_expressions) > 0:
        update_expressions.append("SET " + ', '.join(set_expressions))

    remove_expressions:List = [ f"#{k}" for k in remove_item]
    remove_attr_names:dict   = { f"#{k}":k for k in remove_item }
    if len(remove_expressions) > 0:
        update_expressions.append("REMOVE " + ', '.join(remove_expressions))

    add_expressions:List    = [ f"#{k} = :{k}" for k in add_item.keys()]
    add_attr_names:dict     = { f"#{k}":k for k in add_item.keys() }
    add_attr_values:dict    = { f":{k}":v for k,v in add_item.items() }
    if len(add_expressions) > 0:
        update_expressions.append("ADD " + ', '.join(add_expressions))

    # テスト
    return {
        "UpdateExpression": " ".join(update_expressions),
        "ExpressionAttributeNames": {
            **set_attr_names,
            **remove_attr_names,
            **add_attr_names,
        },
        "ExpressionAttributeValues": {
            **set_attr_values,
            **add_attr_values,
        },
    }
