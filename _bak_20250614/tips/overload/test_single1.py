import tips.overload.mylibs.func_single1 as func_ol


# サンプルデータを処理する（引数を変えて関数をコールします）
func_ol.func_name("文字列を表示")      # 文字列として処理します
func_ol.func_name(15)                 # 整数型として処理します
func_ol.func_name([1, 2, 3])          # List型として処理します
func_ol.func_name(3.14)               # 浮動小数点の数値は未登録です

func_ol.func_name()
