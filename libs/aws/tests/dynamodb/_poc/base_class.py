from typing import override


class Parent:

    def greet(self, name: str = "aaa") -> str:
        """親クラスの挨拶メソッド"""
        return f"Hello, {name}"

    def hello(self, name: str) -> str:
        """親クラスのHelloメソッド"""
        return f"Hello, {name}"



class Child(Parent):

    @override  # これによりIDEが親のシグネチャを認識
    def greet(self, name: str) -> str:
        return f"Hello, {name}"

    @override  # パラメータは子のものになる。IDE次第？ ⇒ 同じである保証がないのでしょうがないか。
    def hello(self, *args, **kwargs) -> str:
        return super().hello(*args, **kwargs)


if __name__ == '__main__':
    obj = Child()

    ret = obj.greet(name="bob") # 親クラスのパラメータヒントが表示される
    print(ret)

    ret = obj.hello(name="aaa")
    print(ret)
