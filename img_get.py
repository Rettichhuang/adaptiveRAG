import pandas as pd

xls_path=r"D:\project\vcop\adaptiveRAG\data\Captures\image_list.xlsx"

# 读取 Excel 文件
df = pd.read_excel(xls_path, engine='openpyxl')

# 遍历表格的每一行，检查第三列的值是否为1
for index, row in df.iterrows():
    if row["sat"] == 1:  # 检查第三列（索引从0开始，所以第三列是索引2）
        print(row["name"])  # 打印第一列的值（索引0）
