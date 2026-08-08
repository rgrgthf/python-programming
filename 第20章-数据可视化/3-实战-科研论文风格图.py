# ============================================================
# 数据可视化 ③ — 实战：科研论文风格图
# ============================================================
# ⚠️ 请在 sci 环境运行
# 把学过的技能综合起来，做一张"能放进论文/汇报"的完整图。

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# ============================================================
# 一、统一设置（论文级样式）
# ============================================================
plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei"],
    "axes.unicode_minus": False,
    "figure.dpi": 100,           # 屏幕显示
    "axes.grid": True,
    "grid.alpha": 0.3,
    "axes.labelsize": 12,
    "axes.titlesize": 14,
    "legend.fontsize": 10,
})

# ============================================================
# 二、实战任务：标准曲线 + 剂量-反应 IC50 综合图
# ============================================================
# 任务：一张图包含两个面板
#   左：标准曲线（线性拟合）
#   右：剂量-反应曲线（IC50 拟合）

from scipy.optimize import curve_fit

# ---------- 数据 ----------
# 标准曲线数据（浓度 vs 吸光度）
conc_std = np.array([0, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0])
abs_std = np.array([0, 0.048, 0.125, 0.251, 0.51, 1.01, 2.49])

# 剂量-反应数据（浓度 vs 抑制率%）
conc_dose = np.array([0.001, 0.01, 0.1, 1, 10, 100, 1000])
inhib = np.array([2, 5, 18, 45, 78, 92, 97])

# ---------- 拟合 ----------
# 标准曲线线性拟合
k, b = np.polyfit(conc_std, abs_std, 1)
line = k * conc_std + b

# IC50 用 Hill 方程拟合：E = Emax * c^n / (IC50^n + c^n)
def hill(c, emax, ic50, n):
    return emax * c ** n / (ic50 ** n + c ** n)

popt, _ = curve_fit(hill, conc_dose, inhib, p0=[100, 1, 1])
emax_fit, ic50_fit, n_fit = popt
x_fit = np.logspace(-3, 3, 200)
y_fit = hill(x_fit, *popt)

# ---------- 画图 ----------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# 左图：标准曲线
ax1.scatter(conc_std, abs_std, color="#4C72B0", s=60, label="实测点", zorder=5)
ax1.plot(conc_std, line, color="#C44E52", label=f"拟合: y={k:.3f}x{b:+.3f}")
ax1.set_xlabel("浓度 (mg/mL)")
ax1.set_ylabel("吸光度")
ax1.set_title("(a) 标准曲线")
ax1.legend(loc="upper left")
ax1.text(0.05, 0.9, f"R² = {np.corrcoef(conc_std, abs_std)[0,1]**2:.4f}",
         transform=ax1.transAxes)

# 右图：剂量-反应曲线
ax2.scatter(conc_dose, inhib, color="#55A868", s=60, label="实测点", zorder=5)
ax2.plot(x_fit, y_fit, color="#C44E52", label="Hill拟合")
ax2.set_xscale("log")                  # x轴对数
ax2.set_xlabel("药物浓度 (μM, 对数)")
ax2.set_ylabel("抑制率 (%)")
ax2.set_title(f"(b) 剂量-反应曲线  IC50={ic50_fit:.2f} μM")
ax2.legend(loc="upper left")
ax2.axvline(ic50_fit, color="gray", linestyle="--", alpha=0.7)  # IC50 竖线
ax2.text(ic50_fit * 1.1, 50, f"IC50={ic50_fit:.2f}", color="gray")

plt.tight_layout()
# plt.show()

# 保存出版级高清图
# plt.savefig("论文图_标准曲线与IC50.png", dpi=300, bbox_inches="tight")
print(f"拟合结果：R²={np.corrcoef(conc_std, abs_std)[0,1]**2:.4f}, "
      f"IC50={ic50_fit:.2f} μM, Hill系数n={n_fit:.2f}")

# ============================================================
# 三、多图拼接与标注技巧
# ============================================================
# 子图编号 (a) (b)：论文习惯，便于文中引用
# 图例位置：upper left / lower right / best
# 在图上加文字：ax.text(x, y, "内容")
# 加参考线：ax.axvline(位置) 竖线 / ax.axhline(位置) 横线

# ============================================================
# 四、输出格式建议
# ============================================================
# 论文投稿：.pdf / .svg（矢量图，无限放大清晰）
#    plt.savefig("fig.pdf")
# 汇报PPT：.png 300dpi 或 .svg
# 网页/文档：.png 150dpi
# 注意：保存格式由扩展名决定

# ============================================================
# 五、一套可复用的"科研出图模板"
# ============================================================
def make_science_plot(ax, x, y, xlabel, ylabel, title=None, fit=None):
    """通用科研散点图（可选拟合线）"""
    ax.scatter(x, y, s=50, color="#4C72B0", zorder=5)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    if fit:                       # fit = (斜率, 截距)
        k, b = fit
        xs = np.linspace(min(x), max(x), 100)
        ax.plot(xs, k * xs + b, color="#C44E52")
    ax.grid(True, alpha=0.3)

# 用法示例（复用模板快速出图）
# fig, ax = plt.subplots(figsize=(6, 4))
# make_science_plot(ax, conc_std, abs_std, "浓度", "吸光度",
#                   "标准曲线", fit=(k, b))
# plt.show()

# ============================================================
# 六、总结
# ============================================================
# 统一 rcParams 设置全局样式
# 多子图 plt.subplots(1, 2) + 子图编号(a)(b)
# 对数轴 set_xscale("log")（剂量-反应必须）
# Hill 拟合 curve_fit（IC50 计算）
# 保存 dpi=300 / pdf矢量
# 总结成可复用模板函数

# ============================================================
# 六、易错点汇总
# ============================================================
# 1. 论文图要求：坐标轴加粗、刻度向内、字体够大、
#    网格线淡——提前设好 plt.rcParams 全局默认
# 2. 所有图风格统一：用 rcParams 一次性配置，别每张图手改
# 3. 标题用英文或规范中文，字号别太小（论文 10~12pt 起步）
# 4. 误差棒（errorbar）要带上，论文/汇报标配
# 5. 图例位置避免挡数据：loc="best" 或手动指定
# 6. 可复用模板：把"设置+画图+保存"封装成函数，换数据即用

# ============================================================
# 七、自测（40%基础 + 40%中等 + 20%挑战）
# ============================================================
# 【基础】
# 1. 论文级图至少要注意哪几个要素？
# 2. 怎么统一所有图的风格？
# 3. 误差棒用什么函数？
#
# 【中等】
# 4. 用 rcParams 设置全局：中文字体、坐标轴粗细、网格。
# 5. 画一组数据的均值+误差棒（errorbar）。
# 6. 封装一个 plot_paper(x, y, xlabel, ylabel, title) 函数。
#
# 【挑战】
# 7. 用模板函数画一张论文风格的标准曲线图并保存。
# 8. 对比"每张图手改"和"模板函数"两种方式的优劣。
