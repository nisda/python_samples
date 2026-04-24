# 拡張 format関数


## 概要
format 関数の機能拡張版。

### 主な機能
* dict をドット連結方式で記述可能。
* 文字列型以外の元のデータ型で返却することが可能。  
  プレースホルダーに変数のみを記述している場合のみ可。

### 使用例
```python
from format_ex import format_map

input = {
    "a" {
        "aa" : [
            {"aa0a": "AA0A", "aa0b", 123}
        ]
    }
}

# 基本的な使い方：dict階層のドット連結記法
ret = format_map(expr="aa0a -> `{a.aa[0].aa0a}`", mapping=input)
assert ret == "aa0a -> `AA0A`"

ret = format_map(expr="aa0b -> `{a.aa[0].aa0b}`", mapping=input)
assert ret == "aa0b -> `123`"

# 元データ型で返却
ret = format_map(expr="{a.aa[0].aa0b}", mapping=input, original_type=True)
assert ret == 123

```
