"""
メソッドに動的にデコレータを追加する。
"""
import functools
import inspect

# デコレータ定義
def log_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"--- Calling: {func.__name__} ---")
        return func(*args, **kwargs)
    return wrapper


class BaseClass:
    def method(self):
        print("Original method")

class MyClass(BaseClass):

    def __init__(self):
        # 全メソッドに対して動的にデコレータを適用
        for attr_info in inspect.getmembers(self, inspect.ismethod):
            attr_name = attr_info[0]

            print(f"add decorator to `{attr_name}`")
            setattr(self, attr_name, log_decorator(getattr(self, attr_name)))


if __name__ == '__main__':
    # インスタンス生成
    obj = MyClass()

    # # 動的にデコレータを適用 -> init で実施するようサンプルを変更
    # obj.method = log_decorator(obj.method)

    # デコレータ付きのメソッドが動作する。
    obj.method()
