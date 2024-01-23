# coding: utf-8

from typing import List, Tuple, Any
import urllib.request
import urllib.parse
import json

class RestAPI:

    def __init__(self, base_url:str, content_type:str, base_headers:dict=None, base_query_strings:dict=None):
        '''コンストラクタ'''
        self._base_url = base_url.rstrip("/")
        self._content_type = content_type
        self._base_headers = base_headers or {}
        self._base_query_strings = base_query_strings or {}
        return

    def request(self, method:str, path:str, headers:dict=None, query_strings:dict=None, data:Any=None):
        '''リクエスト'''

        # data処理（よく使うcontent-typeだけ対応）
        send_data:bytes = None
        if isinstance(data, bytes):
            send_data = data
        elif self._content_type == "application/x-www-form-urlencoded":
            send_data = urllib.parse.urlencode(data).encode('utf-8')
        elif self._content_type == "application/json":
            send_data = json.dumps(data).encode()
        elif isinstance(data, str):
            send_data = data.encode("utf-8")
        else:
            send_data = data

        # QueryString処理
        merged_qs:dict = {
            "content-type": self._content_type,
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
        headers_merged = {**self._base_headers, **(headers or {})}

        # リクエスト生成
        if data is None:
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
        with urllib.request.urlopen(req) as res:
            return {
                "headers": res.getheaders(),
                "status": res.status,
                "reason": res.reason,
                "msg": res.msg,
                "body": res.read().decode(),
            }
