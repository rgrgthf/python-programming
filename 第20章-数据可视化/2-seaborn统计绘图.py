# ============================================================
# 数据可视化 ② — seaborn 统计绘图
# ============================================================
# ⚠️ 请在 sci 环境运行（VS Code 右下角切解释器）
# seaborn 是建立在 matplotlib 上的"统计绘图库"：
# 一行代码出专业统计图。特别适合展示实验数据分布和关系。

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 中文字体
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# ============================================================
# 一、准备演示数据（三组实验数据）
# ============================================================
np.random.seed(42)
n = 30
df = pd.DataFrame({
    "组别": ["对照组"] * n + ["低剂量"] * n + ["高剂量"] * n,
    "药效": (np.random.normal(10, 2, n).tolist()
            + np.random.normal(14, 2.5, n).tolist()
            + np.random.normal(19, 3, n).tolist()),
})
print(df.head())

# ============================================================
# 二、sns.boxplot 箱线图（统计检验报告标配）
# ============================================================
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="组别", y="药效")
plt.title("不同剂量组药效分布")
# plt.show()

# 小提琴图（箱线图+分布形状）
plt.figure(figsize=(8, 5))
sns.violinplot(data=df, x="组别", y="药效")
plt.title("小提琴图：更细的分布信息")
# plt.show()

# ============================================================
# 三、sns.barplot 柱状图（带误差棒，自动算均值±SE）
# ============================================================
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="组别", y="药效", errorbar="sd")  # 误差=标准差
plt.title("各组药效均值（误差=SD）")
# plt.show()

# ============================================================
# 四、散点图 + 回归线（sns.regplot）
# ============================================================
# 标准曲线直接看拟合效果
x = np.array([0, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0])
y = x * 0.5 + np.random.normal(0, 0.02, len(x))

plt.figure(figsize=(8, 5))
sns.regplot(x=x, y=y, ci=95)   # ci=置信区间，自带回归线和区间
plt.xlabel("浓度 (mg/mL)")
plt.ylabel("吸光度")
plt.title("标准曲线（seaborn自动拟合）")
# plt.show()

# ============================================================
# 五、热力图（相关性矩阵 / 分子相似性）
# ============================================================
# 生成相关性矩阵
np.random.seed(7)
data = pd.DataFrame(np.random.randn(100, 4),
                    columns=["分子量", "LogP", "TPSA", "活性"])
corr = data.corr()      # 相关系数矩阵

plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", center=0,
            fmt=".2f", square=True)
plt.title("描述符相关性热力图")
# plt.show()
# 颜色深=相关性强（红正蓝负），标注数字

# ============================================================
# 六、联合分布图（两个变量的分布+关系）
# ============================================================
# sns.jointplot 边缘是直方图，中间是散点
# sns.jointplot(data=df, x="药效", y="药效", kind="scatter")
# kind 可选：scatter / hex / kde / reg

# 配对图（多变量两两关系，探索数据神器）
# sns.pairplot(data, hue="组别")

# ============================================================
# 七、seaborn vs matplotlib 怎么选？
# ============================================================
# seaborn 优势：
#   1. 统计图（箱线/小提琴/热力图/回归图）一行出
#   2. 自动带误差棒、置信区间
#   3. 配色专业、和 pandas 无缝配合
# matplotlib 优势：
#   1. 控制力更强（任何细节都能调）
#   2. 更底层，可定制一切
#   3. seaborn 底层就是 matplotlib
#
# 建议：探索数据用 seaborn，精细定制用 matplotlib
#       两者常混用（seaborn 画 + plt 调细节）

# ============================================================
# 八、总结
# ============================================================
# boxplot/violinplot：分布
# barplot：均值±误差
# regplot：散点+回归线+置信区间
# heatmap：相关性矩阵/相似性
# pairplot：多变量两两探索
