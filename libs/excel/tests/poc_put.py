import openpyxl

wb = openpyxl.Workbook()
ws = wb.active

# 2行目・2列目（B2セル）を開始位置にする
start_row = 2
start_col = 2
data = [
    ["名前", "年齢", "部署"],
    ["田中", 28, "営業"],
    ["佐藤", 35, "開発"],
    ["鈴木", 30, "人事"]
]


# 4. 一括書き込み
for r_idx, row in enumerate(data):
    for c_idx, value in enumerate(row):
        # 座標を指定して書き込み
        ws.cell(row=start_row + r_idx, column=start_col + c_idx, value=value)

wb.save("test_data/sample_output.xlsx")
