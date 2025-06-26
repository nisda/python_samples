print(int("123"))
print(int(123))


# dictのキー



import decimal

dict_a = {
    "1" : "str1",
    1   : "num1",
    2   : "num2",
    "2" : "str2",
    "3" : "str3",
    3.0 : "float3",
    "4" : "str4",
    decimal.Decimal(4) : "Decimal4",
    -1 : "int -1",
    "-1" : "str -1",
    -2.1 : "float -2.1",
    "-2.1" : "str -2.1",
}

for k in [1, 2, 3, 4, -1, -2.1]:
    print("----------")
    print(dict_a[str(k)])
    print(dict_a[float(k)])
    print(dict_a[decimal.Decimal(k)])
    print(dict_a[int(k)])


print("----------")
for k,v in dict_a.items():
    print(f"{k} : {k.__class__.__name__}")


for k in ["1", "1.1", "-1.1"]:
    print(k.isdecimal())

