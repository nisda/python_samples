import logging
import re

class UniversalMaskFilter(logging.Filter):
    def filter(self, record):
        # 1. getMessage() で、オブジェクトや引数(args)を統合した文字列を取得
        original_message = record.getMessage()
        
        # 2. マスク処理（正規表現など）
        patterns = {
            r'password=\S+': 'password=********',   # 正規表現間違ってるので後ろが切れる
            r'[\w\.-]+@[\w\.-]+': '****@****'
        }
        
        masked_message = original_message
        for pattern, replacement in patterns.items():
            masked_message = re.sub(pattern, replacement, masked_message)
        
        # 3. record.msg をマスク済み文字列に書き換え、args を空にする
        # これにより、後続のフォーマッタはマスク済みの文字列をそのまま使用する
        record.msg = masked_message
        record.args = ()
        
        return True

# セットアップ
logger = logging.getLogger("AppLogger")
handler = logging.StreamHandler()
handler.addFilter(UniversalMaskFilter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# テストケース1: 辞書オブジェクトを渡す
data = {"user": "admin", "details": "password=secret123"}
logger.info(data) # {'user': 'admin', 'details': 'password=********'} 的な内容が出力される

# テストケース2: 例外オブジェクトを渡す
try:
    raise ValueError("Error with email: test@example.com")
except Exception as e:
    logger.error(e) # Error with email: ****@**** が出力される
