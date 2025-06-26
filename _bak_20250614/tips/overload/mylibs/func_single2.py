# 参考: https://www.python.digibeatrix.com/archives/1373

from functools import singledispatch

@singledispatch
def process(arg):
    print("デフォルトの処理:", arg)

@process.register(int)
def _(arg):
    print("整数を処理:", arg)

@process.register(str)
def _(arg):
    print("文字列を処理:", arg)

# # 使用例
# process(10)  # 出力: 整数を処理: 10
# process("こんにちは")  # 出力: 文字列を処理: こんにちは
# process([1, 2, 3])  # 出力: デフォルトの処理: [1, 2, 3]


