# ============================================================
# Excel 自动化 ③ — 实战：批量处理实验记录
# ============================================================
# ⚠️ 请在 sci 环境运行
# 综合实战：一个文件夹里 50 个 Excel 实验记录，
# 批量读取 → 汇总 → 统计 → 生成一张总表 + 统计报告。

import pandas as pd
import os
from pathlib import Path
from openpyxl import Workbook

# ============================================================
# 一、准备演示数据（模拟 5 个批次的 Excel 文件）
# ============================================================
Path("批量实验").mkdir(exist_ok=True)

for batch in range(1, 6):
    wb = Workbook()
    ws = wb.active
    ws.title = "记录"
    ws.append(["批次", "样品", "浓度", "吸光度"])
    for i in range(1, 6):
        ws.append([batch, f"B{batch}-{i}", i * 0.4, i * 0.2 + 0.02])
    wb.save(f"批量实验/批次{batch}_记录.xlsx")

print("已生成 5 个批次文件")

# ============================================================
# 二、批量读取所有 Excel
# ============================================================
all_data = []
for file in Path("批量实验").glob("*.xlsx"):
    df = pd.read_excel(file)
    all_data.append(df)
    print(f"读取 {file.name}: {len(df)} 条")

# 合并所有批次
combined = pd.concat(all_data, ignore_index=True)
print(f"\n共合并 {len(combined)} 条记录")
print(combined.head())

# ============================================================
# 三、批量统计（按批次分组）
# ============================================================
# 每组均值/标准差/样本数
stats = combined.groupby("批次").agg(
    样品数=("样品", "count"),
    平均浓度=("浓度", "mean"),
    平均吸光度=("吸光度", "mean"),
    吸光度标准差=("吸光度", "std"),
).round(3)
print("\n各批次统计：")
print(stats)

# ============================================================
# 四、合并后的全局统计
# ============================================================
overall = {
    "总记录数": len(combined),
    "总平均浓度": round(combined["浓度"].mean(), 3),
    "总平均吸光度": round(combined["吸光度"].mean(), 3),
    "吸光度最大值": round(combined["吸光度"].max(), 3),
    "吸光度最小值": round(combined["吸光度"].min(), 3),
}
print("\n总体统计：", overall)

# ============================================================
# 五、导出汇总报告
# ============================================================
with pd.ExcelWriter("批量实验_汇总报告.xlsx") as writer:
    combined.to_excel(writer, sheet_name="全部数据", index=False)
    stats.to_excel(writer, sheet_name="分批次统计")
    pd.DataFrame([overall]).to_excel(writer, sheet_name="总体统计", index=False)

print("\n✅ 汇总报告已生成：批量实验_汇总报告.xlsx")

# ============================================================
# 六、异常检查（自动发现问题）
# ============================================================
# 检查是否有异常值（超过3倍标准差）
mean = combined["吸光度"].mean()
std = combined["吸光度"].std()
outliers = combined[abs(combined["吸光度"] - mean) > 3 * std]
if len(outliers) > 0:
    print(f"\n⚠️ 发现 {len(outliers)} 个异常值：")
    print(outliers)
else:
    print("\n✅ 未发现异常值")

# ============================================================
# 七、总结：这个实战用到了什么？
# ============================================================
# Path.glob("*.xlsx")        → 批量找文件
# pd.read_excel              → 读每个文件
# pd.concat                  → 合并所有批次
# groupby().agg()            → 分组统计
# ExcelWriter + 多sheet      → 生成汇总报告
# 3倍标准差                 → 异常值检测
#
# 这就是"实验数据自动化处理"的完整套路，
# 毕业论文数据处理、实验课报告都能这么干！
