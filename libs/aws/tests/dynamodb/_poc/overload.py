from typing import overload, Union



@overload
def test(id:int) -> int:
    print("AAAAAAAAAA")
    ...

@overload
def test(id:str) -> str:
    ...

def test(id:Union[int,str]) -> Union[int,str]:
    return id


ret = test(1)
print(type(ret))
print(ret)

ret = test("a")
print(type(ret))
print(ret)

