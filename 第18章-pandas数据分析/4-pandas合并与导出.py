# ============================================================
# pandas 数据合并与导出 — 拼表和保存
# ============================================================
# 实验数据常常分散在多个表里（不同仪器、不同批次），
# 需要合并成一张表，最后导出成 Excel/CSV 交给老师或写进报告。

import pandas as pd

# ============================================================
# 一、拼接：concat（上下拼 / 左右拼）
# ============================================================
# 模拟：三次重复实验，各存一个表
batch1 = pd.DataFrame({"样品": ["A", "B"], "吸光度": [0.5, 0.7]})
batch2 = pd.DataFrame({"样品": ["C", "D"], "吸光度": [0.6, 0.9]})

# 上下拼接（行方向，默认）
all_data = pd.concat([batch1, batch2], ignore_index=True)
print(all_data)
#   样品  吸光度
# 0  A   0.5
# 1  B   0.7
# 2  C   0.6
# 3  D   0.9
# ignore_index=True：重新编号，不保留原索引

# 左右拼接（列方向，按行对齐）
info = pd.DataFrame({"样品": ["A", "B", "C", "D"], "组别": ["对照", "给药", "对照", "给药"]})
combined = pd.concat([all_data, info["组别"]], axis=1)
print(combined)


# ============================================================
# 二、合并：merge（按公共列匹配，类似 Excel VLOOKUP）
# ============================================================
# 两张表有共同的一列（比如"样品编号"），按它对齐
left = pd.DataFrame({
    "样品": ["A", "B", "C"],
    "浓度": [10, 20, 30],
})
right = pd.DataFrame({
    "样品": ["A", "B", "C"],
    "组别": ["对照", "给药", "对照"],
})

merged = pd.merge(left, right, on="样品")   # 按"样品"列合并
print(merged)
#   样品  浓度  组别
# 0  A   10   对照
# 1  B   20   给药
# 2  C   30   对照

# merge 就是"把两张表按同一个编号拼在一起"——实验里超常用


# ============================================================
# 三、导出：to_csv / to_excel
# ============================================================
df = pd.DataFrame({
    "组别": ["对照", "给药"],
    "存活率": [94.75, 62.5],
})

# 导出 CSV
df.to_csv("结果.csv", index=False, encoding="utf-8-sig")
# index=False：不写行号（0,1,2...），更干净
# encoding="utf-8-sig"：Excel 打开中文不乱码的关键！

# 导出 Excel（需 openpyxl）
# df.to_excel("结果.xlsx", index=False)

# 追加导出（Excel 多 sheet）
# with pd.ExcelWriter("报告.xlsx") as writer:
#     df.to_excel(writer, sheet_name="汇总", index=False)
#     df2.to_excel(writer, sheet_name="明细", index=False)


# ============================================================
# 四、保存后再读回（验证）
# ============================================================
df.to_csv("结果.csv", index=False, encoding="utf-8-sig")
back = pd.read_csv("结果.csv")
print(back)     # 读回来内容一致
# 注意：读回来后数字还是数字（pandas 自动识别）


# ============================================================
# 五、实战：完整流程模板
# ============================================================
# 三步走：读入 → 处理 → 导出
def process_experiment(input_csv, output_xlsx):
    """读取实验 CSV → 分组统计 → 导出 Excel"""
    df = pd.read_csv(input_csv, encoding="utf-8")
    df = df.dropna()                       # 清洗
    summary = df.groupby("组别").agg(["mean", "std"]).round(2)
    # 导出
    with pd.ExcelWriter(output_xlsx) as writer:
        df.to_excel(writer, sheet_name="原始数据", index=False)
        summary.to_excel(writer, sheet_name="统计汇总")
    return summary

# process_experiment("实验数据.csv", "实验报告.xlsx")
# 以后拿到实验数据，调用这个函数就能出结果表！
