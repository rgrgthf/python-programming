# ============================================================
# 方差分析 ANOVA 与卡方检验 — 多组比较
# ============================================================
# t 检验只能比两组；三组及以上要用 ANOVA。
# 场景：对照 / 低剂量 / 高剂量 三组，比较存活率是否有差异。

import numpy as np
from scipy import stats

# ============================================================
# 一、单因素方差分析（one-way ANOVA）
# ============================================================
# 三组数据（每组多个重复）
control = np.array([95, 93, 97, 94, 96, 95, 92, 96])
low     = np.array([80, 78, 82, 79, 81, 83, 80, 78])
high    = np.array([50, 45, 47, 52, 48, 49, 46, 51])

f_stat, p_value = stats.f_oneway(control, low, high)
print(f"ANOVA: F = {f_stat:.3f}, p = {p_value:.5f}")
# p < 0.05 → 三组间至少有一组和其他组有显著差异

# ⚠️ ANOVA 只能告诉你"组间有差异"，不能告诉你是哪两组！
# 需要做事后检验（post-hoc）找出具体差异。

# ============================================================
# 二、事后检验（两两比较）
# ============================================================
# 用 scipy 的 pairwise_tukeyhsd（需要 statsmodels 库）
# 先安装：pip install statsmodels
try:
    from statsmodels.stats.multicomp import pairwise_tukeyhsd
    import pandas as pd

    # 把三组数据整理成"一列数值 + 一列组名"
    all_values = np.concatenate([control, low, high])
    all_groups = (["对照"] * len(control) +
                  ["低剂量"] * len(low) +
                  ["高剂量"] * len(high))

    result = pairwise_tukeyhsd(all_values, all_groups)
    print(result)
    # 输出里：reject=True 表示这两组差异显著
except ImportError:
    print("需要安装 statsmodels：pip install statsmodels")

# 论文里的常见表述：
#   "对照组与高剂量组差异显著（p<0.001），
#    低剂量与高剂量组差异显著（p<0.001）"

# ============================================================
# 三、卡方检验（分类数据）
# ============================================================
# 场景：比较"两组实验的成功率"是否有差异（计数数据，不是数值）
# 数据是列联表（行=组别，列=结果）

# 例如：对照组 40 只，给药组 40 只，各记录"存活/死亡"
contingency = np.array([
    [30, 10],   # 对照组：存活30，死亡10
    [35, 5],    # 给药组：存活35，死亡5
])

chi2, p_value, dof, expected = stats.chi2_contingency(contingency)
print(f"卡方 = {chi2:.3f}, p = {p_value:.4f}")
# p < 0.05 → 两组生存率有显著差异

# 卡方适用于：计数/比例数据（如有效 vs 无效、阳性 vs 阴性）
# 数值数据（如浓度、吸光度）不要用卡方！

# ============================================================
# 四、相关性分析（两个连续变量的关系）
# ============================================================
# 场景：浓度和抑制率是否相关
conc = np.array([1, 2, 4, 8, 16, 32])
inhibition = np.array([5, 12, 25, 48, 76, 92])

# Pearson 相关系数（要求两变量都正态）
r, p_value = stats.pearsonr(conc, inhibition)
print(f"Pearson: r = {r:.3f}, p = {p_value:.4f}")
# r 越接近 1 → 正相关越强；p < 0.05 → 相关显著

# Spearman 秩相关（不正态时用，更稳健）
rho, p_value = stats.spearmanr(conc, inhibition)
print(f"Spearman: rho = {rho:.3f}, p = {p_value:.4f}")

# r 的解读：
#   |r| > 0.8 → 强相关
#   |r| 0.5~0.8 → 中等相关
#   |r| 0.3~0.5 → 弱相关
#   |r| < 0.3 → 基本不相关

# ============================================================
# 五、论文显著性标注规范
# ============================================================
# *   p < 0.05     差异显著
# **  p < 0.01     差异较显著
# *** p < 0.001    差异极显著
# ns  p >= 0.05    无显著差异（not significant）
#
# 柱状图上通常在组间画线标星号（matplotlib 可手动画）
