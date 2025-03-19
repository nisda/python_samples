## 備考
* きちんと調べたわけではない。
* 調べるならまずは公式を。
  https://docs.python.org/ja/3.9/tutorial/modules.html#

## 相対import

* `.` や `..` を利用できるのはモジュール内のみ。


## \_\_init__.py

* ライブラリのフォルダに置くファイル。必須ではない。
* 現在、空ファイルでは何も意味を持たない？
  古い Python バージョンでは意味があったらしい。
* そのフォルダを import したときに最初に読み込まれるコード。
* 基本的な書きかた使いかた。たぶんこれでOK。
  ```python:__init__.py
  from . import func_a
  from . import ClassA
  from .mod_sub import func_b
  ```

* 以下のような書き方をすることで、そのライブラリフォルダにあるすべてのモジュールを読み込んで利用可能になる。
  ただしこの書き方は推奨されないらしい。
  同名モジュールが存在したら上書きされそうなので、明示すべきということなのかも。  
  ```python:__init__.py
  from . import *
  ```


## 指定のパスを import する。
* `sys.path.append(path)`
* 例
  ```python
  import sys
  import os
  sys.path.append('絶対パス')
  sys.path.append(os.path.join(os.path.dirname(__file__), "sub_dir")) # これで相対パスのように書けるが。

  # append したパスにあるモジュールを参照できる。
  import func_A
  from subdir import ClassA
  ```
* 推奨はされない。
  * 「import は一番上にまとめるべき」が実現できない。
    `__init__.py` に書くのなら可能かもしれない。
  * 自分が管理していない他のライブラリの動作にも影響が出るかも。



