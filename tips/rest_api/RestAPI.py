# coding: utf-8

from typing import List, Tuple, Any
import urllib.request
import urllib.parse
import json
import mimetypes
import random
import string


class RestAPI:

    def __init__(self, base_url:str, base_headers:dict=None, base_query_strings:dict=None):
        '''コンストラクタ'''
        self._base_url = base_url.rstrip("/")
        self._base_headers = base_headers or {}
        self._base_query_strings = base_query_strings or {}
        return

    def request(self,
        method:str,
        path:str,
        content_type:str,
        headers:dict=None,
        query_strings:dict=None,
        data:dict=None,
        files:dict=None,
        raise_http_error:bool=False,
    ):
        '''リクエスト'''

        # data処理（よく使うcontent-typeだけ対応。必要に応じて追加）
        send_data:bytes = None
        if len(files or {}) > 0:
            content_type, send_data = self.__encode_mu1ltipart_formdata(data=data, files=files)
        elif content_type == "application/x-www-form-urlencoded":
            send_data = urllib.parse.urlencode(data).encode('utf-8')
        elif content_type == "application/json":
            send_data = json.dumps(data).encode('utf-8')
        else:
            send_data = data

        # QueryString処理
        merged_qs:dict = {
            **self._base_query_strings,
            **(query_strings or {}),
        }
        qs_tuples:List[Tuple] = []
        for k,v in merged_qs.items():
            if isinstance(v, list):
                qs_tuples.extend([(k,x) for x in v])
            else:
                qs_tuples.append((k,v))
        qs:str = urllib.parse.urlencode(qs_tuples)

        # URL処理
        url:str = f"{self._base_url}/{path.lstrip('/')}"
        url_full:str = f"{url}?{qs}"

        # Header処理
        headers_merged = {
            **self._base_headers,
            **(headers or {}),
            "content-type": content_type,
        }

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
            if raise_http_error:
                raise e
            else:
                return {
                    "headers": [ list(x) for x in e.headers.items() ],
                    "status": e.code,
                    "reason": e.reason,
                    "msg": e.msg,
                    "body": e.read().decode(),
                }

    def __get_content_type(self, filename:str):
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

    def __get_random_str(self, length:int):
        return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(length)])

    def __encode_mu1ltipart_formdata(self, data:dict, files:dict):
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

        BOUNDARY_STR = self.__get_random_str(30)
        CHAR_ENCODING = "utf-8"
        CRLF = bytes("\r\n", CHAR_ENCODING)
        L = []
        for (key, value) in data.items():
            L.append(bytes("--" + BOUNDARY_STR, CHAR_ENCODING))
            L.append(bytes('Content-Disposition: form-data; name="%s"' % key, CHAR_ENCODING))
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
            L.append(bytes('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename), CHAR_ENCODING))
            L.append(bytes('Content-Type: %s' % self.__get_content_type(filename), CHAR_ENCODING))
            L.append(b'')
            L.append(content)
        L.append(bytes('--' + BOUNDARY_STR + '--', CHAR_ENCODING))
        L.append(b'')

        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=' + BOUNDARY_STR
        return content_type, body
