# 参考: https://and-engineer.com/articles/ZJ90xhAAACIAGBJE

#     第一引数以外の型には対応していない。
#     複数の引数の型を基に分岐する場合は適していない。


from functools import singledispatch
 
@singledispatch               # singledispatchを使用します
def func_name(arg):           # 念のため、例外処理として追加します
    print("このタイプは表示できません。")
 
@func_name.register           # オーバーロード属性を追加します
def func_name_str(arg: str):  # 文字列型を定義します
    print("文字列型：",arg)
 
@func_name.register           # オーバーロード属性を追加します
def func_name_int(arg: int):  # 整数型を定義します
    print("整数型：", arg)
 
@func_name.register           # オーバーロード属性を追加します
def func_name_list(arg: list):# List型を定義します
    print("List型：", arg)

 
# # サンプルデータを処理する（引数を変えて関数をコールします）
# func_name("文字列を表示")      # 文字列として処理します
# func_name(15)                 # 整数型として処理します
# func_name([1, 2, 3])          # List型として処理します
# func_name(3.14)               # 浮動小数点の数値は未登録です
