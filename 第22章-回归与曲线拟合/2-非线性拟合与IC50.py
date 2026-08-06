# ============================================================
# 非线性拟合与 IC50 — 药理实验核心
# ============================================================
# IC50 = 半数抑制浓度：抑制率达到 50% 时所需的药物浓度。
# 剂量-反应曲线通常是 S 形（logistic），不是直线，要用非线性拟合。

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# ============================================================
# 一、剂量-反应数据
# ============================================================
# 药物浓度（用 log 坐标更合理，因为浓度跨度大）
conc = np.array([0.1, 0.3, 1, 3, 10, 30, 100, 300])    # μM
inhibition = np.array([2, 8, 18, 35, 60, 78, 90, 96])  # 抑制率 %

# ============================================================
# 二、定义拟合模型（4参数logistic：Hill方程）
# ============================================================
# 公式：y = bottom + (top - bottom) / (1 + (x/IC50)^(-HillSlope))
#   bottom  = 最小抑制率
#   top     = 最大抑制率
#   IC50    = 半抑制浓度（我们要的）
#   HillSlope = 曲线陡峭程度
def hill(x, bottom, top, ic50, hill_slope):
    return bottom + (top - bottom) / (1 + (x / ic50) ** (-hill_slope))

# ============================================================
# 三、非线性拟合
# ============================================================
# 初始猜测值（帮助拟合收敛）
p0 = [0, 100, 10, 1]
popt, pcov = curve_fit(hill, conc, inhibition, p0=p0)

bottom, top, ic50, hill_slope = popt
print(f"bottom = {bottom:.2f}")
print(f"top    = {top:.2f}")
print(f"IC50   = {ic50:.2f} μM")
print(f"Hill斜率 = {hill_slope:.2f}")

# ============================================================
# 四、画剂量-反应曲线（半对数坐标）
# ============================================================
# 生成平滑曲线
x_smooth = np.logspace(-1, 2.5, 200)    # 0.1 ~ 300 对数均匀
y_smooth = hill(x_smooth, *popt)

plt.scatter(conc, inhibition, color="blue", label="实验数据")
plt.plot(x_smooth, y_smooth, "r-", label="拟合曲线")
plt.xscale("log")                        # 浓度用对数坐标
plt.axhline(50, color="gray", linestyle="--", alpha=0.5)   # 50% 参考线
plt.axvline(ic50, color="green", linestyle="--", alpha=0.5) # IC50 位置
plt.text(ic50, 55, f"IC50 = {ic50:.1f} μM", color="green")
plt.xlabel("药物浓度 (μM)")
plt.ylabel("抑制率 (%)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.3)
plt.savefig("剂量反应曲线.png", dpi=300)
plt.show()

# ============================================================
# 五、预测特定抑制率对应的浓度（EC50/IC50 一般化）
# ============================================================
# 求抑制率达到 50% 时的浓度（验证 IC50）
# 解方程：50 = bottom + (top-bottom)/(1+(x/ic50)^(-h))
def conc_at(y_target, bottom, top, ic50, h):
    return ic50 * ((y_target - bottom) / (top - y_target)) ** (1 / h)

print(f"按公式验证 IC50 = {conc_at(50, *popt):.2f} μM")

# ============================================================
# 六、常见药理学指标
# ============================================================
# IC50  半数抑制浓度（越大越不敏感）
# EC50  半数有效浓度
# LD50  半数致死剂量（毒理）
# 这些都用同一套 Hill 拟合流程，改一下参数名和解读即可

# ============================================================
# 七、注意事项
# ============================================================
# 1. 浓度跨度大 → 用对数坐标展示更直观
# 2. 数据点至少 6~8 个，覆盖从低抑制到高抑制
# 3. 初始猜测值 p0 要给合理范围，否则拟合可能失败
# 4. 结果要和 GraphPad Prism 对比验证（拟合方法应一致）
# 5. 拟合质量控制：看残差是否随机、R² 是否合理
