# http_requests


## 対応メモ

```
□ body と json をユーザー側で気にせず使えるようにしたい。
    □ RequestsCore 仕様
        ・ content-type は __generate_request_data で、body/json/file から判断する。
            ・file が存在する場合は content-type 固定。headers で指定していても無視。
              全体（データ部分）は multipart/form-data、ファイルはそれぞれ。
              json は無視され、データは必ず data を form-urlencode したものになる。
            ・data の場合は以下の通り分岐。
                dict → form-urlencode
                list|tupe -> form-urlencode
                bytes -> そのまま。content-type 指定なし
                その他 -> encode で byte にして送信。content-type 指定なし
            ・charset は content-type に指定されていればそれを採用。なければ utf-8
            ・json の場合は、json.dumps().encode(content-typeのcharset)
    □ これを wrap する対応案
        ・content-type を指定させる。
        ・charset も指定させる。
        ・fileありの場合は気にしない。勝手に編集するので。
    □ POST と GET で content-type を別にするケースもあるし、対応するの難しいような？
        →下手に弄らないようにしようか。        

```