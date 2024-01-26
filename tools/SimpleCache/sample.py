# coding: utf-8
import time
from SimpleCache import SimpleCache


def func_addition(a, b):
    result  =   a + b
    return result

if __name__ == '__main__':

    cache = SimpleCache()

    #--------------------------------
    #   値をセット（３秒間キャッシュ保持）
    #--------------------------------
    print("-- value:")
    for i in range(0, 5):
        val = cache.cache(key="val", value=i, expiration_seconds=3)
        print(val)
        time.sleep(1)


    #--------------------------------
    #   関数を渡す（３秒間キャッシュ保持）
    #--------------------------------
    print("-- func:")
    for i in range(0, 5):
        val = cache.cache(key="func", value=(lambda:func_addition(1000, i)), expiration_seconds=3)
        print(val)
        time.sleep(1)

    #--------------------------------
    #   途中でキャッシュ削除
    #--------------------------------
    print("-- remove:")
    for i in range(0, 10):
        val = cache.cache(key="rem", value=i, expiration_seconds=60)
        print(val)
        time.sleep(1)
        if i % 4 == 0:
            cache.remove("rem")

