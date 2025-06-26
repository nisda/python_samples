# coding: utf-8


'''
２つ作ろう。ほぼ下位互換の Requests と、更に使いやすくしたラッパークラス。
このモジュール内で Requests <-> requests を置き換えられるようにする。


HTTP Requests (`requests` のほぼ下位互換)
  ver : 1.0.0
  date: 2025/6/15
  description:
    requests のほぼ下位互換。
    https://requests.readthedocs.io/en/latest/user/quickstart/#make-a-request
    PaaS 利用時など、ライブラリ追加が面倒なときに。
'''

from typing import List, Tuple, Any, Dict, Union
import urllib.request
import urllib.parse
import json as jsonlib
import mimetypes
import random
import string
import io
import os


class CaseInsensitiveDict(dict):
    @classmethod
    def _k(cls, key):
        return key.lower() if isinstance(key, str) else key

    def __init__(self, *args, **kwargs):
        super(CaseInsensitiveDict, self).__init__(*args, **kwargs)
        self._convert_keys()

    def __getitem__(self, key):
        return super(CaseInsensitiveDict, self).__getitem__(self.__class__._k(key))

    def __setitem__(self, key, value):
        super(CaseInsensitiveDict, self).__setitem__(
            self.__class__._k(key), value)

    def __delitem__(self, key):
        return super(CaseInsensitiveDict, self).__delitem__(self.__class__._k(key))

    def __contains__(self, key):
        return super(CaseInsensitiveDict, self).__contains__(self.__class__._k(key))

    def has_key(self, key):
        return super(CaseInsensitiveDict, self).has_key(self.__class__._k(key))

    def pop(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).pop(self.__class__._k(key), *args, **kwargs)

    def get(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).get(self.__class__._k(key), *args, **kwargs)

    def setdefault(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).setdefault(self.__class__._k(key), *args, **kwargs)

    def update(self, E={}, **F):
        super(CaseInsensitiveDict, self).update(self.__class__(E))
        super(CaseInsensitiveDict, self).update(self.__class__(**F))

    def _convert_keys(self):
        for k in list(self.keys()):
            v = super(CaseInsensitiveDict, self).pop(k)
            self.__setitem__(k, v)


class Response:
    '''レスポンス'''

    __url: str
    _status: int
    _headers: List[str]
    _content: Any

    def __init__(self, url: str,  res, ex: urllib.error.HTTPError):
        self.__url = url

        if res is not None:
            self._headers = res.getheaders()
            self._status = res.status
            # self._reason = res.reason
            # self._msg = res.msg
            self._content = res.read()
        if ex is not None:
            self._headers = [list(x) for x in ex.headers.items()]
            self._status = ex.code,
            # self._reason = ex.reason,
            # self._msg = ex.msg,
            self._content = ex.read(),
            self._ex = ex

    @property
    def url(self):
        return self.__url

    @property
    def status_code(self):
        return self._status

    @property
    def headers(self) -> CaseInsensitiveDict:
        return CaseInsensitiveDict({x[0]: x[1] for x in self._headers})

    @property
    def encoding(self) -> str:
        return "*未実装*"

    @property
    def raw(self):
        return "*未実装*"

    @property
    def content(self) -> bytes:
        return self._content

    @property
    def text(self) -> str:
        return self._content.decode()

    def json(self) -> Any:
        return jsonlib.loads(self._content.decode())

    def raise_for_status(self) -> None:
        if self._ex is None:
            return None
        else:
            raise self._ex


class __RequestsCore:

    @classmethod
    def _request(
        cls,
        method: str,
        url: str,
        params: Dict[str, Any] = None,
        data: Union[Dict, List[Tuple], str, bytes] = None,
        json: Dict = None,
        headers: Dict[str, str] = None,
        files: dict = None,
    ) -> Response:
        '''HTTPリクエスト実行'''
        pass

        # URL 整形
        req_url: str = cls.__generate_request_url(url=url, params=params)

        # method 整形
        req_method: str = method.upper()

        # header整形
        req_headers: Dict[str, str] = cls.__generate_headers(headers=headers)

        # body 整形
        content_type, req_data = cls.__generate_request_data(
            data=data,
            json=json,
            headers=headers,
            files=files,
        )

        # content-type を上書き。
        content_type_key = [
            k for k in req_headers.keys() if k.lower() == 'content-type']
        if len(content_type_key) > 0:
            req_headers[content_type_key[0]] = content_type or ""
        else:
            req_headers["Content-Type"] = content_type or ""

        # リクエスト生成
        if req_data is None:
            req = urllib.request.Request(
                method=req_method,
                url=req_url,
                headers=req_headers,
            )
        else:
            req = urllib.request.Request(
                method=req_method,
                url=req_url,
                headers=req_headers,
                data=req_data,
            )

        # リクエスト実行
        try:
            with urllib.request.urlopen(req) as res:
                return Response(url=req_url, res=res, ex=None)
        except urllib.error.HTTPError as ex:
            return Response(url=req_url, res=None, ex=ex)

    @classmethod
    def __generate_request_url(cls, url: str, params: Dict[str, Any] = None) -> str:
        '''リクエストURL生成'''

        if params is None or len(params) == 0:
            # パラメータが空の場合はURLそのまま返却
            return url

        else:
            # パラメータ(QueryString)をURLエンコードして URL に追加
            req_params = cls.__convert_dict_to_urlencode(data=params)
            return url + "?" + req_params

    @classmethod
    def __convert_dict_to_urlencode(cls, data: dict) -> str:
        query: List[Tuple] = cls.__convert_dict_to_tuples(data=data)
        return urllib.parse.urlencode(query=query)

    @staticmethod
    def __convert_dict_to_tuples(data: dict) -> List[Tuple]:
        ret: List[Tuple] = []
        for k, v in data.items():
            if isinstance(v, list):
                ret.extend([(k, x) for x in v])
            else:
                ret.append((k, v))
        return ret

    @classmethod
    def __generate_headers(cls, headers: Dict[str, str]) -> Dict[str, str]:

        # Null の場合は初期化（dict化）
        headers = headers or {}

        # デフォルトヘッダをセット（INPUT優先）
        default_headers = {
            'Accept-Encoding': 'gzip, deflate',
            'Accept': '*/*',
        }
        for k, v in default_headers.items():
            headers.setdefault(k, v)

        # 返却
        return headers

    @staticmethod
    def __get_content_type_from_headers(headers: dict[str, str]) -> Dict[str, str]:
        '''headers から指定キーの値を抽出（Case Insensitive）'''

        # ヘッダ未指定時は空データ返却
        if headers is None:
            return {}

        # content-type 抜き出し
        content_type = CaseInsensitiveDict(headers).get("content-type", None)

        # content-type 未指定時は空データ返却
        if content_type is None:
            return {}

        # 戻り値用の変数を生成
        ret: CaseInsensitiveDict = {"src": content_type}

        # 要素を分解
        splitted: List[str] = [x.strip() for x in content_type.split(";")]

        # １つ目の要素は MIME-type
        ret['mime_type'] = None if splitted[0] == '' else splitted[0]

        # 2つ目以降は指定キー
        for i in range(1, len(splitted)):
            pair: list = splitted[i].split("=")
            if len(pair) >= 2:
                key = pair[0]
                value = "=".join(pair[1:])
                ret[key] = value

        return ret

    @classmethod
    def __generate_request_data(
        cls,
        data: Union[Dict, List[Tuple], str, bytes],
        json: Dict,
        headers: Dict[str, str],
        files: Dict[str, Any],
    ) -> Tuple[str, str]:
        """        
        * param `data`, `json` のタイプ別に以下の変換処理を行なう。
          `data`, `files` が優先。それらが指定されている場合、 `json` は無視される。
        * data 指定時：
            * headers.content-type の変更はしない。
            * Tuple のリストは、dict に変換して処理する。同じキーが複数存在した場合は値を list 化する。
            * input.data を form-urlencode する。
        * json 指定時：
            * headers.content-type の変更はしない。
              元が未指定のときは、 `application/json` をセットする。
            * input.json を json文字列に変換する。
        """

        # content-type を取得・分解
        content_type_dict: CaseInsensitiveDict = \
            cls.__get_content_type_from_headers(headers=headers)
        content_type: str = content_type_dict.get("src", None)
        charset: str = content_type_dict.get("charset", "utf-8")

        # inputパラメータの有無により処理分岐
        if files is not None and len(files) > 0:
            # files ありの場合
            (content_type, send_data) = cls.__convert_multipart_formdata(
                data=data, files=files)
            return (content_type, send_data)

        elif data is not None:
            # data あり
            mime_type: str = None
            if isinstance(data, dict):
                mime_type = "application/x-www-form-urlencoded"
                send_data = cls.__convert_dict_to_urlencode(
                    data).encode(encoding=charset)
            elif isinstance(data, (list, tuple)):
                mime_type = "application/x-www-form-urlencoded"
                send_data = urllib.parse.urlencode(
                    query=data).encode(encoding=charset)
            elif isinstance(data, bytes):
                send_data = data
            else:
                send_data = data.encode(encoding=charset)

            return (content_type or mime_type, send_data)

        elif json is not None:
            # json の場合
            send_data = jsonlib.dumps(json).encode(encoding=charset)

            return (content_type or "application/json", send_data)

        # すべてNoneの場合
        return (content_type, None)

    @classmethod
    def __convert_multipart_formdata(cls, data: dict, files: dict) -> Tuple[str, bytes]:
        '''
        フォームデータとファイルを合わせて multipart/form-data の形式に変換する。
        -----------
        [INPUT-Patterns]
            files = {
                'form-name1': open('report.xls', 'rb'),
                'form-name2': ('report.xls', open('report.xls', 'rb'), 'application/vnd.ms-excel', {'Expires': '0'}),      # 4つ目(header)以降は無視。
                'form-name3': ('report.csv', 'some,data,to,send\nanother,row,to,send\n'),
            }
        '''

        def __get_mime_type(file_name: str) -> str:
            return mimetypes.guess_type(file_name)[0] or 'application/octet-stream'

        def __get_random_str(length: int) -> str:
            return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(length)])

        def __parse_input(file_info: Union[io.IOBase, Tuple, List]) -> Tuple[str, str, bytes]:
            file_name: str = None
            file_data: bytes = None
            mime_type: str = None

            if isinstance(file_info, io.IOBase):
                file_name = file_info.name
                file_info.seek(0)
                file_data = file_info.read()
                mime_type = None
                file_info.close()

            if isinstance(file_info, (list, tuple)):
                file_name = file_info[0]
                if isinstance(file_info[1], io.IOBase):
                    file_info[1].seek(0)
                    file_data = file_info[1].read()
                    file_info[1].close()
                elif isinstance(file_info[1], str):
                    file_data = file_info[1].encode()
                else:
                    file_data = file_info[1]
                if len(file_info) >= 3:
                    mime_type = file_info[2]

            return {
                "file_name": os.path.basename(file_name),
                "mime_type": mime_type,
                "file_data": file_data
            }

        # 処理設定
        BOUNDARY_STR = __get_random_str(30)
        CHAR_ENCODING = "utf-8"
        CRLF = bytes("\r\n", CHAR_ENCODING)
        buf = []

        # data 処理
        data = data or []
        if isinstance(data, dict):
            data = cls.__convert_dict_to_tuples(data)

        for (key, value) in data:
            buf.append(bytes("--" + BOUNDARY_STR, CHAR_ENCODING))
            buf.append(bytes('Content-Disposition: form-data; name="%s"' %
                             key, CHAR_ENCODING))
            buf.append(b'')
            buf.append(bytes(value, CHAR_ENCODING))

        # files 処理
        files = {k: __parse_input(file_info=v) for k, v in files.items()}
        for (key, value) in files.items():
            file_name: str = value['file_name']
            file_data: bytes = value['file_data']
            mime_type: str = value['mime_type']
            buf.append(bytes('--' + BOUNDARY_STR, CHAR_ENCODING))
            buf.append(bytes('Content-Disposition: form-data; name="%s"; filename="%s"' %
                             (key, file_name), CHAR_ENCODING))
            if mime_type is not None:
                buf.append(bytes('Content-Type: %s' %
                           mime_type, CHAR_ENCODING))
            buf.append(b'')
            buf.append(file_data)
        buf.append(bytes('--' + BOUNDARY_STR + '--', CHAR_ENCODING))
        buf.append(b'')

        body = CRLF.join(buf)
        content_type = 'multipart/form-data; boundary=' + BOUNDARY_STR

        return content_type, body


class Requests(__RequestsCore):

    @classmethod
    def get(
        cls,
        url: str,
        params: Dict[str, Any] = None,
        data: Union[Dict, List[Tuple], str, bytes] = None,
        json: Dict = None,
        headers: Dict[str, str] = None,
    ) -> Response:
        return cls._request(
            method="GET",
            url=url,
            params=params,
            data=data,
            json=json,
            headers=headers,
        )

    @classmethod
    def head(
        cls,
        url: str,
        params: Dict[str, Any] = None,
        headers: Dict[str, str] = None,
    ) -> Response:
        return cls._request(
            method="HEAD",
            url=url,
            params=params,
            headers=headers,
        )

    @classmethod
    def post(
        cls,
        url: str,
        params: Dict[str, Any] = None,
        data: Union[Dict, List[Tuple], str, bytes] = None,
        json: Dict = None,
        headers: Dict[str, str] = None,
        files: dict = None,
    ) -> Response:
        return cls._request(
            method="POST",
            url=url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            files=files,
        )

    @classmethod
    def put(
        cls,
        url: str,
        params: Dict[str, Any] = None,
        data: Union[Dict, List[Tuple], str, bytes] = None,
        json: Dict = None,
        headers: Dict[str, str] = None,
        files: dict = None,
    ) -> Response:
        return cls._request(
            method="PUT",
            url=url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            files=files,
        )

    @classmethod
    def patch(
        cls,
        url: str,
        params: Dict[str, Any] = None,
        data: Union[Dict, List[Tuple], str, bytes] = None,
        json: Dict = None,
        headers: Dict[str, str] = None,
        files: dict = None,
    ) -> Response:
        return cls._request(
            method="PATCH",
            url=url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            files=files,
        )

    @classmethod
    def delete(
        cls,
        url: str,
        params: Dict[str, Any] = None,
        data: Union[Dict, List[Tuple], str, bytes] = None,
        json: Dict = None,
        headers: Dict[str, str] = None,
    ) -> Response:
        return cls._request(
            method="DELETE",
            url=url,
            params=params,
            data=data,
            json=json,
            headers=headers,
        )

    @classmethod
    def options(
        cls,
        url: str,
        params: Dict[str, Any] = None,
        headers: Dict[str, str] = None,
    ) -> Response:
        return cls._request(
            method="OPTIONS",
            url=url,
            params=params,
            headers=headers,
        )


# class ApiRequests:

#     def __init__(self, base_url: str, base_headers: dict = None, base_qs: dict = None, raise_http_error: bool = False):
#         '''コンストラクタ'''
#         self._base_url: str = base_url.rstrip("/")
#         self._base_headers: dict = base_headers or {}
#         self._base_qs: dict = base_qs or {}
#         self._raise_http_error: bool = raise_http_error
#         return

#     def __generate_body(self, content_type: str, data: Any, files: Dict, encoding: str) -> Tuple[str, bytes]:
#         data = data or {}
#         send_data: bytes = None
#         if len(files or {}) > 0:
#             content_type, send_data = self.__encode_multipart_formdata(
#                 data=data, files=files)
#         elif content_type == "application/x-www-form-urlencoded":
#             send_data = urllib.parse.urlencode(data).encode(encoding=encoding)
#         elif content_type == "application/json":
#             send_data = jsonlib.dumps(data).encode(encoding=encoding)
#         else:
#             send_data = data
#         return (content_type, send_data)

#     def __generate_qs(self, qs: Dict) -> str:
#         merged_qs: dict = {
#             **self._base_qs,
#             **(qs or {}),
#         }
#         qs_tuples: List[Tuple] = []
#         for k, v in merged_qs.items():
#             if isinstance(v, list):
#                 qs_tuples.extend([(k, x) for x in v])
#             else:
#                 qs_tuples.append((k, v))
#         qs: str = urllib.parse.urlencode(qs_tuples)
#         return qs

#     def __generate_url(self, path: str, qs: str = "") -> str:
#         url: str = f"{self._base_url}/{path.lstrip('/')}"

#         if qs is None or len(qs) == 0:
#             return url
#         else:
#             return f"{url}?{qs}"

#     def __generate_header(self, content_type: str, headers: dict) -> Dict[str, str]:

#         return {
#             **self._base_headers,
#             **(headers or {}),
#             "content-type": content_type,
#         }

#     def __encode_multipart_formdata(self, data: dict, files: dict):
#         '''
#         フォームデータとファイルを合わせて multipart/form-data の形式に変換する。
#         -----------
#         [INPUT]
#         files = {
#             "<form-name>" : {
#                 "filename": <str>,
#                 "content" : <bytes>,
#             }
#         }
#         '''

#         def __get_content_type(self, filename: str):
#             return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

#         def __get_random_str(self, length: int):
#             return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(length)])

#         BOUNDARY_STR = __get_random_str(30)
#         CHAR_ENCODING = "utf-8"
#         CRLF = bytes("\r\n", CHAR_ENCODING)
#         L = []
#         data = data or {}
#         for (key, value) in data.items():
#             L.append(bytes("--" + BOUNDARY_STR, CHAR_ENCODING))
#             L.append(bytes('Content-Disposition: form-data; name="%s"' %
#                      key, CHAR_ENCODING))
#             L.append(b'')
#             if isinstance(value, (list, dict)):
#                 # 暫定：このパターンのデータの扱いが不明。許容するべきでない？
#                 L.append(bytes(jsonlib.dumps(value), CHAR_ENCODING))
#             else:
#                 L.append(bytes(value, CHAR_ENCODING))
#         for (key, value) in files.items():
#             filename = value['filename']
#             content = value['content']
#             L.append(bytes('--' + BOUNDARY_STR, CHAR_ENCODING))
#             L.append(bytes('Content-Disposition: form-data; name="%s"; filename="%s"' %
#                      (key, filename), CHAR_ENCODING))
#             L.append(bytes('Content-Type: %s' %
#                      __get_content_type(filename), CHAR_ENCODING))
#             L.append(b'')
#             L.append(content)
#         L.append(bytes('--' + BOUNDARY_STR + '--', CHAR_ENCODING))
#         L.append(b'')

#         body = CRLF.join(L)
#         content_type = 'multipart/form-data; boundary=' + BOUNDARY_STR
#         return content_type, body

#     def request(self,
#                 method: str,
#                 path: str,
#                 content_type: str,
#                 headers: dict = None,
#                 qs: dict = None,
#                 data: dict = None,
#                 files: dict = None,
#                 encoding: str = 'utf-8',
#                 ):
#         '''リクエスト'''

#         # data処理（よく使うcontent-typeだけ対応。必要に応じて追加）
#         (content_type, send_data) = self.__generate_body(
#             content_type=content_type,
#             data=data,
#             files=files,
#             encoding=encoding
#         )

#         # QueryString処理
#         qs: str = self.__generate_qs(qs=qs)

#         # URL処理
#         url_full: str = self.__generate_url(path=path, qs=qs)

#         # Header処理
#         headers_merged = self.__generate_header(
#             content_type=content_type,
#             headers=headers
#         )

#         # リクエスト生成
#         if send_data is None:
#             req = urllib.request.Request(
#                 method=method.upper(),
#                 url=url_full,
#                 headers=headers_merged,
#             )
#         else:
#             req = urllib.request.Request(
#                 method=method.upper(),
#                 url=url_full,
#                 headers=headers_merged,
#                 data=send_data,
#             )

#         # リクエスト実行
#         try:
#             with urllib.request.urlopen(req) as res:
#                 return {
#                     "headers": res.getheaders(),
#                     "status": res.status,
#                     "reason": res.reason,
#                     "msg": res.msg,
#                     "body": res.read().decode(),
#                 }
#         except urllib.error.HTTPError as e:
#             if self._raise_http_error:
#                 raise e
#             else:
#                 return {
#                     "headers": [list(x) for x in e.headers.items()],
#                     "status": e.code,
#                     "reason": e.reason,
#                     "msg": e.msg,
#                     "body": e.read().decode(),
#                 }
