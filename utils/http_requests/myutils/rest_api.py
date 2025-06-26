# coding: utf-8

"""
REST API
  ver : 1.0.0
  date: 2025/6/15
"""

from typing import List, Tuple, Any, Dict
import urllib.request
import urllib.parse
import json
import mimetypes
import random
import string


class RestAPI:

    def __init__(self, base_url: str, base_headers: dict = None, base_qs: dict = None, raise_http_error: bool = False):
        '''コンストラクタ'''
        self._base_url: str = base_url.rstrip("/")
        self._base_headers: dict = base_headers or {}
        self._base_qs: dict = base_qs or {}
        self._raise_http_error: bool = raise_http_error
        return

    def __generate_body(self, content_type: str, data: Any, files: Dict, encoding: str) -> Tuple[str, bytes]:
        data = data or {}
        send_data: bytes = None
        if len(files or {}) > 0:
            content_type, send_data = self.__encode_multipart_formdata(
                data=data, files=files)
        elif content_type == "application/x-www-form-urlencoded":
            send_data = urllib.parse.urlencode(data).encode(encoding=encoding)
        elif content_type == "application/json":
            send_data = json.dumps(data).encode(encoding=encoding)
        else:
            send_data = data
        return (content_type, send_data)

    def __generate_qs(self, qs: Dict) -> str:
        merged_qs: dict = {
            **self._base_qs,
            **(qs or {}),
        }
        qs_tuples: List[Tuple] = []
        for k, v in merged_qs.items():
            if isinstance(v, list):
                qs_tuples.extend([(k, x) for x in v])
            else:
                qs_tuples.append((k, v))
        qs: str = urllib.parse.urlencode(qs_tuples)
        return qs

    def __generate_url(self, path: str, qs: str = "") -> str:
        url: str = f"{self._base_url}/{path.lstrip('/')}"

        if qs is None or len(qs) == 0:
            return url
        else:
            return f"{url}?{qs}"

    def __generate_header(self, content_type: str, headers: dict) -> Dict[str, str]:

        return {
            **self._base_headers,
            **(headers or {}),
            "content-type": content_type,
        }

    def __encode_multipart_formdata(self, data: dict, files: dict):
        '''
        フォームデータとファイルを合わせて multipart/form-data の形式に変換する。
        -----------
        [INPUT]
        files = {
            "<form-name>" : {
                "filename": <str>,
                "content" : <bytes>,
            }
        }
        '''

        def __get_content_type(self, filename: str):
            return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

        def __get_random_str(self, length: int):
            return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(length)])

        BOUNDARY_STR = __get_random_str(30)
        CHAR_ENCODING = "utf-8"
        CRLF = bytes("\r\n", CHAR_ENCODING)
        L = []
        data = data or {}
        for (key, value) in data.items():
            L.append(bytes("--" + BOUNDARY_STR, CHAR_ENCODING))
            L.append(bytes('Content-Disposition: form-data; name="%s"' %
                     key, CHAR_ENCODING))
            L.append(b'')
            if isinstance(value, (list, dict)):
                # 暫定：このパターンのデータの扱いが不明。許容するべきでない？
                L.append(bytes(json.dumps(value), CHAR_ENCODING))
            else:
                L.append(bytes(value, CHAR_ENCODING))
        for (key, value) in files.items():
            filename = value['filename']
            content = value['content']
            L.append(bytes('--' + BOUNDARY_STR, CHAR_ENCODING))
            L.append(bytes('Content-Disposition: form-data; name="%s"; filename="%s"' %
                     (key, filename), CHAR_ENCODING))
            L.append(bytes('Content-Type: %s' %
                     __get_content_type(filename), CHAR_ENCODING))
            L.append(b'')
            L.append(content)
        L.append(bytes('--' + BOUNDARY_STR + '--', CHAR_ENCODING))
        L.append(b'')

        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=' + BOUNDARY_STR
        return content_type, body

    def request(self,
                method: str,
                path: str,
                content_type: str,
                headers: dict = None,
                qs: dict = None,
                data: dict = None,
                files: dict = None,
                encoding: str = 'utf-8',
                ):
        '''リクエスト'''

        # data処理（よく使うcontent-typeだけ対応。必要に応じて追加）
        (content_type, send_data) = self.__generate_body(
            content_type=content_type,
            data=data,
            files=files,
            encoding=encoding
        )

        # QueryString処理
        qs: str = self.__generate_qs(qs=qs)

        # URL処理
        url_full: str = self.__generate_url(path=path, qs=qs)

        # Header処理
        headers_merged = self.__generate_header(
            content_type=content_type,
            headers=headers
        )

        # リクエスト生成
        if send_data is None:
            req = urllib.request.Request(
                method=method.upper(),
                url=url_full,
                headers=headers_merged,
            )
        else:
            req = urllib.request.Request(
                method=method.upper(),
                url=url_full,
                headers=headers_merged,
                data=send_data,
            )

        # リクエスト実行
        try:
            with urllib.request.urlopen(req) as res:
                return {
                    "headers": res.getheaders(),
                    "status": res.status,
                    "reason": res.reason,
                    "msg": res.msg,
                    "body": res.read().decode(),
                }
        except urllib.error.HTTPError as e:
            if self._raise_http_error:
                raise e
            else:
                return {
                    "headers": [list(x) for x in e.headers.items()],
                    "status": e.code,
                    "reason": e.reason,
                    "msg": e.msg,
                    "body": e.read().decode(),
                }

    def __parse_response_body(header: List[])
