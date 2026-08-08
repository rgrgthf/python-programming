# ============================================================
# 数据可视化 ① — matplotlib 进阶
# ============================================================
# ⚠️ 请在 sci 环境运行（VS Code 右下角切解释器）
# 第9章学过 matplotlib 基础，这一节是"论文级"进阶：
# 多子图、样式、坐标轴控制、保存高清图。

import matplotlib.pyplot as plt
import numpy as np

# 中文字体支持（Windows）
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False   # 负号正常显示

# ============================================================
# 一、子图布局（一张图放多个子图）
# ============================================================
x = np.linspace(0, 10, 100)

# 2行2列子图
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
# axes 是 2x2 的数组

axes[0, 0].plot(x, np.sin(x), "b-")
axes[0, 0].set_title("sin")

axes[0, 1].plot(x, np.cos(x), "r--")
axes[0, 1].set_title("cos")

axes[1, 0].plot(x, np.exp(-x), "g-")
axes[1, 0].set_title("exp(-x)")

axes[1, 1].plot(x, x ** 2, "m:")
axes[1, 1].set_title("x^2")

plt.tight_layout()      # 自动调整间距
# plt.show()

# ============================================================
# 二、样式与美化
# ============================================================
# 线条样式：
#   "-" 实线  "--" 虚线  "-." 点划线  ":" 点线
#   颜色：r红 g绿 b蓝 k黑 m品红 c青 y黄
#   标记：o圆 s方 ^三角 *星形

x = np.linspace(0, 5, 20)
y1 = x ** 2
y2 = x ** 1.5

plt.figure(figsize=(8, 5))
plt.plot(x, y1, "bo-", label="y=x²", linewidth=2, markersize=5)
plt.plot(x, y2, "rs--", label="y=x^1.5", linewidth=2)
plt.xlabel("浓度 (mg/mL)", fontsize=12)
plt.ylabel("吸光度", fontsize=12)
plt.title("浓度-吸光度关系", fontsize=14)
plt.legend()            # 显示图例
plt.grid(True, alpha=0.3)   # 网格线
# plt.show()

# ============================================================
# 三、散点图 + 拟合线（实验数据标配！）
# ============================================================
# 模拟标准曲线数据
conc = np.array([0, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0])
abs_ = np.array([0, 0.05, 0.13, 0.26, 0.52, 1.01, 2.50])

# 线性拟合
k, b = np.polyfit(conc, abs_, 1)
line = k * conc + b

plt.figure(figsize=(8, 5))
plt.scatter(conc, abs_, color="b", s=60, label="实测点", zorder=5)
plt.plot(conc, line, "r-", label=f"拟合线 y={k:.3f}x+{b:.3f}")
plt.xlabel("浓度 (mg/mL)")
plt.ylabel("吸光度")
plt.title("标准曲线")
plt.legend()
plt.grid(True, alpha=0.3)
# plt.show()

# ============================================================
# 四、保存高清图（论文/报告用）
# ============================================================
# plt.savefig("标准曲线.png", dpi=300, bbox_inches="tight")
# dpi=300：出版级清晰度
# bbox_inches="tight"：裁掉多余空白

# ============================================================
# 五、柱状图与误差棒
# ============================================================
# 三组数据的均值 ± 标准差
groups = ["对照组", "低剂量", "高剂量"]
means = [10.2, 14.5, 21.3]
stds = [1.5, 2.1, 2.8]

plt.figure(figsize=(8, 5))
bars = plt.bar(groups, means, yerr=stds, capsize=5, width=0.5,
               color=["#4C72B0", "#DD8452", "#55A868"])
plt.ylabel("药效指标")
plt.title("不同剂量组的药效比较（均值±SD）")
# 在柱顶标数值
for bar, m in zip(bars, means):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f"{m:.1f}", ha="center")
# plt.show()

# ============================================================
# 六、箱线图（看数据分布，异常值）
# ============================================================
np.random.seed(42)
data1 = np.random.normal(10, 2, 50)
data2 = np.random.normal(13, 3, 50)
data3 = np.random.normal(8, 1.5, 50)

plt.figure(figsize=(8, 5))
plt.boxplot([data1, data2, data3], labels=groups, patch_artist=True)
plt.ylabel("测量值")
plt.title("三组数据分布对比")
plt.grid(True, alpha=0.3)
# plt.show()
# 箱线图信息：中位数、四分位、异常点（圆圈）

# ============================================================
# 七、双 y 轴（两种单位同图）
# ============================================================
x = np.linspace(0, 10, 50)
y_conc = np.exp(x / 5)
y_pct = x * 5

fig, ax1 = plt.subplots(figsize=(8, 5))
ax1.plot(x, y_conc, "b-", label="浓度")
ax1.set_xlabel("时间")
ax1.set_ylabel("浓度 (mg/mL)", color="b")
ax1.tick_params(axis="y", labelcolor="b")

ax2 = ax1.twinx()                     # 共享x轴的第二个y轴
ax2.plot(x, y_pct, "r--", label="转化率")
ax2.set_ylabel("转化率 (%)", color="r")
ax2.tick_params(axis="y", labelcolor="r")
# plt.show()

# ============================================================
# 八、总结
# ============================================================
# 子图：plt.subplots(rows, cols)
# 样式：颜色+线型+标记（"bo-"），label+legend
# 标准曲线：scatter实测 + plot拟合线（科研标配）
# 保存：savefig(dpi=300, bbox_inches="tight")
# 柱状图：bar + yerr误差棒；箱线图：boxplot
# 双轴：twinx()

# ============================================================
# 六、易错点汇总
# ============================================================
# 1. figure（画布）和 axes（坐标系）是两个概念：
#    plt.subplots(1,2) 返回 (fig, axes)，多子图用 axes 画
# 2. 中文乱码：plt.rcParams["font.sans-serif"]=["SimHei"]
#    + plt.rcParams["axes.unicode_minus"]=False
# 3. plt.show() 阻塞；批量出图先 savefig 再 show
# 4. 子图索引 axes[0]、axes[1]；axes 是一维/二维数组要对应取
# 5. 双轴 twinx() 两个 y 轴单位不同时用，别忘了标注图例区分
# 6. 保存图设 dpi=300、bbox_inches="tight"（裁掉空白）

# ============================================================
# 七、自测（40%基础 + 40%中等 + 20%挑战）
# ============================================================
# 【基础】
# 1. figure 和 axes 的区别？
# 2. 中文标题乱码怎么解决？
# 3. savefig 为什么要在 show 之前调用？
#
# 【中等】
# 4. 用 subplots(1,2) 画左右两张子图。
# 5. 在同一张图叠加两条曲线并加图例。
# 6. 用 twinx() 画双轴图（如浓度+抑制率）。
#
# 【挑战】
# 7. 写一个能复用的出图函数：输入 x/y，输出论文级图并保存。
# 8. 解释 dpi=300 和 bbox_inches="tight" 的作用。
