


### 
* get_best_index
  * 渡された 検索キー名（list） から、適切と思われる index の情報を取得。
    primary, LSI, GSI の優先度で取得 
* scan
  * 全件取得
* query
  * boto3 の query と同一
* query2
  * より簡易に利用できる query。
  * 検索条件となる Dict[key, value]を渡す。
    範囲指定などはできない。
  * Indexは自動判別する。
* get_item
  * Primaryキーが合致するデータを取得。Primaryキー項目の指定が必須。
  * 不一致時は None
* put_item
  * データの追加/更新（1件）
  * 上書き更新の可否の制御が可能。
  * TTL のセットが可能。未指定時は初期化時の設定を採用。
* put_items
  * データの追加/更新（複数件）
  * 上書き更新の可否の制御はできない。同一キーがあれば更新される。
  * TTL のセットが可能。未指定時は初期化時の設定を採用。
* delete_item
  * データの削除（1件）
  * Primaryキーが合致するデータを削除。Primaryキー項目の指定が必須。
* delete_items
  * データの削除（複数件）
* update_item
  * ややこしいので再検討したい。
* delete_upsert
  * 差分更新。
  * ただしINPUTが0件だと削除条件が作れないのが問題。
* truncate
  * 全削除
　