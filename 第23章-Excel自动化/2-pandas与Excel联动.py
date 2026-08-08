# ============================================================
# Excel 自动化 ② — pandas 与 Excel 联动
# ============================================================
# ⚠️ 请在 sci 环境运行
# 处理 Excel 最顺手的组合：
#   pandas 负责"分析和处理"，openpyxl 负责"样式和细节"。
# pandas 的 read_excel / to_excel 底层就是 openpyxl。

import pandas as pd

# ============================================================
# 一、读取 Excel（read_excel）
# ============================================================
# 创建测试文件
from openpyxl import Workbook
wb = Workbook()
ws = wb.active
ws.append(["样品", "浓度", "吸光度", "日期"])
for i in range(1, 6):
    ws.append([f"A{i}", i * 0.5, i * 0.25 + 0.01, "2026-08-06"])
wb.save("样品数据.xlsx")

# 读取（sheet_name 指定表，header 指定表头行）
df = pd.read_excel("样品数据.xlsx")
print(df)

# 指定列
df = pd.read_excel("样品数据.xlsx", usecols=["样品", "浓度"])
print(df.head())

# 多表工作簿：sheet_name=None 读所有表 → 返回字典
# sheets = pd.read_excel("文件.xlsx", sheet_name=None)

# ============================================================
# 二、写出 Excel（to_excel）
# ============================================================
# 分析结果直接导出成 Excel
df["校正吸光度"] = df["吸光度"] - 0.01      # 模拟处理
df["浓度平方"] = df["浓度"] ** 2

# 写回新表
df.to_excel("样品数据_处理后.xlsx", index=False)
print("已导出 样品数据_处理后.xlsx")

# 多个表写到一个文件
with pd.ExcelWriter("综合报告.xlsx") as writer:
    df.to_excel(writer, sheet_name="原始数据", index=False)
    df[["样品", "校正吸光度"]].to_excel(writer, sheet_name="结果", index=False)
print("已生成多表 Excel：综合报告.xlsx")

# ============================================================
# 三、Excel 常见坑与技巧
# ============================================================
# ① 读进来数字变字符串/文本
#   → 用 dtype 指定类型，或用 pd.to_numeric 转换
df = pd.read_excel("样品数据.xlsx", dtype={"浓度": float})

# ② 日期列读进来是字符串
#   → 用 parse_dates
# df = pd.read_excel("文件.xlsx", parse_dates=["日期"])

# ③ 空单元格变成 NaN
#   → 用 fillna / dropna 处理
print(df.isna().sum())       # 查看每列缺失数

# ④ 表头不在第一行
#   → 用 header= 指定
# df = pd.read_excel("文件.xlsx", header=2)

# ⑤ 合并单元格
#   → 读取时自动变成 NaN 重复值，用 ffill 填充
# df["列"].ffill()

# ============================================================
# 四、实战：Excel 数据处理全流程
# ============================================================
# 场景：仪器导出的原始 Excel，要做清洗+统计+导出报告
raw = pd.DataFrame({
    "样品": [f"S{i}" for i in range(1, 8)],
    "浓度": [0.1, 0.5, None, 1.0, 2.0, None, 5.0],
    "吸光度": [0.05, 0.26, 0.1, 0.52, 1.01, 0.9, 2.49],
    "备注": ["", "", "稀释10倍", "", "", "异常", ""],
})

# 1. 清洗
raw["浓度"] = pd.to_numeric(raw["浓度"], errors="coerce")  # 转数字
raw["浓度"] = raw["浓度"].fillna(0.5)        # 缺失补0.5
raw = raw[raw["备注"] != "异常"]              # 去掉异常行

# 2. 计算
raw["校正吸光度"] = raw["吸光度"] - 0.01

# 3. 统计
summary = pd.DataFrame({
    "指标": ["样品数", "平均浓度", "平均吸光度"],
    "数值": [len(raw), raw["浓度"].mean(), raw["吸光度"].mean()],
})

# 4. 导出报告（两个表）
with pd.ExcelWriter("实验报告.xlsx") as writer:
    raw.to_excel(writer, sheet_name="清洗后数据", index=False)
    summary.to_excel(writer, sheet_name="统计摘要", index=False)

print("实验报告.xlsx 已生成！")

# ============================================================
# 五、pandas + openpyxl 配合（精细控制）
# ============================================================
# pandas 负责数据，openpyxl 负责最后的美化
from openpyxl import load_workbook
from openpyxl.styles import Font

# 用 pandas 写完数据
# 再用 openpyxl 打开美化（自动保存需要 keep_vba 之类注意）

# ============================================================
# 六、总结
# ============================================================
# 读：pd.read_excel（sheet_name/usecols/dtype/parse_dates）
# 写：df.to_excel（index=False，多表用 ExcelWriter）
# 清洗：to_numeric + fillna + dropna
# 报告：数据表 + 统计表 + 样式 一条龙

# ============================================================
# 六、易错点汇总
# ============================================================
# 1. pandas 的 to_excel 底层依赖 openpyxl，
#    没装 openpyxl 会报错
# 2. 写多个 sheet 用 pd.ExcelWriter(路径) + to_excel(sheet_name=)
#    最后 writer.save() 或 with 语句自动保存
# 3. to_excel 默认带索引列，表格数据记得 index=False
# 4. pandas 写样式（列宽/颜色）能力弱，
#    要精细样式用 openpyxl 二次处理
# 5. 读 Excel 用 pd.read_excel(sheet_name=)
# 6. Excel 里数字可能被读成字符串/日期，注意 dtype

# ============================================================
# 七、自测（40%基础 + 40%中等 + 20%挑战）
# ============================================================
# 【基础】
# 1. to_excel 依赖什么库？
# 2. 怎么避免导出时带索引列？
# 3. 读 Excel 用什么函数？
#
# 【中等】
# 4. 用 pandas 把一个 DataFrame 导出为 Excel。
# 5. 用 ExcelWriter 写两个 sheet（原始+汇总）。
# 6. 读回 Excel 并检查 dtype。
#
# 【挑战】
# 7. pandas 写表 + openpyxl 美化样式，生成完整实验报告。
# 8. 说明 pandas 和 openpyxl 各自擅长什么，如何配合。
