import csv
import json

lines = None
with open('./sample_data/csv_input.csv') as f:
    reader = csv.reader(f)
    lines = list(reader)
    print("------------------")
    print(lines)
    # for row in reader:
    #     print(row)

# １行目をヘッダ（カラム名）として扱う
headers = lines[0]
data_list = lines[1:]

print("------------------")
print(headers)
print(data_list)

# カラム名：値　のリストに変換する。
print("------------------")
data = [ dict(zip(headers, x)) for x in data_list ]
print(data)



