# ============================================================
# 实战：完整的实验数据处理流程（综合）
# ============================================================
# 把 numpy / pandas / scipy / matplotlib 串成一条完整流水线：
#   读数据 → 清洗 → 标准曲线 → 算浓度 → 显著性分析 → 出图 → 导出
# 这是你"阶段一+阶段二"的毕业作品模板。

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# ============================================================
# 一、造一份模拟数据（实际用 pandas 读你的 CSV/Excel）
# ============================================================
# 标准曲线数据
std_data = pd.DataFrame({
    "浓度(mg/mL)": [0.0, 0.1, 0.2, 0.4, 0.8, 1.6],
    "吸光度":      [0.001, 0.082, 0.158, 0.331, 0.654, 1.302],
})

# 样品数据（三组 × 4个重复的吸光度）
sample_data = pd.DataFrame({
    "组别": ["对照"] * 4 + ["低剂量"] * 4 + ["高剂量"] * 4,
    "吸光度": [0.52, 0.55, 0.51, 0.54, 0.35, 0.32, 0.36, 0.34,
               0.21, 0.19, 0.22, 0.20],
})

# ============================================================
# 二、拟合标准曲线
# ============================================================
slope, intercept, r_value, _, _ = stats.linregress(
    std_data["浓度(mg/mL)"], std_data["吸光度"]
)
print(f"标准曲线：y = {slope:.4f}x + {intercept:.4f}，R² = {r_value**2:.4f}")

# ============================================================
# 三、用标准曲线反推样品浓度
# ============================================================
sample_data["浓度"] = (sample_data["吸光度"] - intercept) / slope

# ============================================================
# 四、分组统计
# ============================================================
summary = (
    sample_data.groupby("组别")["浓度"]
    .agg(["mean", "std", "count"])
    .round(3)
)
print("\n===== 各组浓度均值±标准差 =====")
print(summary)

# ============================================================
# 五、显著性分析（ANOVA + 事后检验）
# ============================================================
groups = [g["浓度"].values for _, g in sample_data.groupby("组别")]
f_stat, p = stats.f_oneway(*groups)
print(f"\nANOVA: F = {f_stat:.3f}, p = {p:.4f}")

# 两两 t 检验（简化版，仅演示）
names = list(sample_data["组别"].unique())
print("\n===== 两两比较（t检验）=====")
for i in range(len(groups)):
    for j in range(i + 1, len(groups)):
        t, pv = stats.ttest_ind(groups[i], groups[j])
        sig = "***" if pv < 0.001 else "**" if pv < 0.01 else "*" if pv < 0.05 else "ns"
        print(f"{names[i]} vs {names[j]}: p={pv:.4f} {sig}")

# ============================================================
# 六、出图
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

# 左图：标准曲线
line_x = np.array([0, 1.6])
axes[0].scatter(std_data["浓度(mg/mL)"], std_data["吸光度"])
axes[0].plot(line_x, slope * line_x + intercept, "r--")
axes[0].set_xlabel("浓度 (mg/mL)")
axes[0].set_ylabel("吸光度")
axes[0].set_title(f"标准曲线 R²={r_value**2:.4f}")

# 右图：三组柱状图
means = summary["mean"]
stds = summary["std"]
axes[1].bar(means.index, means, yerr=stds, capsize=5)
axes[1].set_ylabel("浓度 (mg/mL)")
axes[1].set_title("各组浓度比较")

plt.tight_layout()
plt.savefig("实验结果.png", dpi=300)
plt.show()

# ============================================================
# 七、导出结果
# ============================================================
with pd.ExcelWriter("实验结果.xlsx") as writer:
    std_data.to_excel(writer, sheet_name="标准曲线", index=False)
    sample_data.to_excel(writer, sheet_name="样品数据", index=False)
    summary.to_excel(writer, sheet_name="统计汇总")
print("\n结果已导出到 实验结果.xlsx")
print("流程完成：读数据 → 标准曲线 → 算浓度 → 统计 → 出图 → 导出")

# ============================================================
# 使用说明（换成你的真实数据）：
#   1. std_data 换成你的标准品数据
#   2. sample_data 换成你的样品数据
#   3. 组别名、列名按你的实验改
#   4. 运行后得到：标准曲线图、比较图、Excel 结果表
# 这就是你第一个"能交差"的药学数据处理脚本！
