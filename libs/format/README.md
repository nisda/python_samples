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

# 開発メモ

## どこまで対応するか
* 値だけ取得できればOK
* f-string のように簡単な計算や関数呼び出しも可能としたい。
  これができるならこれがいい。いろいろ使いどころがある。
  ただし eval に近い動きをするため、自由入力可能な仕組みに使うと injection のリスクがある。


## 実現方法案
### 割り当てデータをドットアクセス可能にする。
* DotDict / SimpleNamespace に変換する。
* 途中の要素を取得できるかどうかや、データが多い場合の処理負荷が課題。
### プレースホルダー内の文字列を変換して、eval(f-string)やformat関数で実行する。
* これが妥当か。
* eval(f-string)は保留。
### プレースホルダーの解析をして、自前で割り当てる。
    計算や関数は使えない。
    format_spec も使えない。

### format関数と f-string の違い

#### format関数
* 関数 : 使えない
* 計算 : 出来ない
* 添え字 : 文字列でもクォート不要
* 添え字内に変数：不可  # a[b] みたいなの
    ⇒変数なのか添え字なのか区別ができないので。
* spec指定 : 使える

### f-string
* 関数 : 使える
* 計算 : 出来る
* 添え字 : 文字列の場合はクォート必須
* 添え字内に変数：可能
* spec指定 : 使える。


### 備考：プレースホルダーの解析についての検討事項
* プレースホルダ―自体を解析するのは可能。
  `from string import Formatter`
  `Formatter().parse(template)`
* 関数や入れ子を使われると正確な変換が難しそう。
* format や f-string では
  * field_name 内でのネストはNG。
    * `f"{test_data1[{}]}"`
      -> `TypeError: string indices must be integers, not 'set'`
    * set と区別がつかない、ということ。
    * 2重カッコ=エスケープ との区別もつかない。
  * spec は 1階層までならネスト可。

## 結論
format関数ベースの機能にする。
関数は可能であれば対応したい。
プレースホルダ―内で、`xxx(.+)` を検出できれば対応できるのでは。

将来的に f-string のような高機能を実現するとしても、
injectionのリスクを考慮して実現する関数は絞りたい。


