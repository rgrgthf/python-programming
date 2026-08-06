# ============================================================
# numpy 深入 ⑤ — 统计、线性代数与性能
# ============================================================
# numpy 内置了强大的统计和线性代数功能，
# 很多"看起来要写循环"的数学问题，numpy 一行解决。

import numpy as np

# ============================================================
# 一、统计函数大全
# ============================================================
data = np.array([12.3, 13.1, 11.8, 12.9, 13.5, 12.7, 13.2, 12.4])

print(np.mean(data))       # 均值
print(np.median(data))     # 中位数（比均值抗异常值）
print(np.std(data))        # 标准差（总体）
print(np.var(data))        # 方差
print(np.min(data))        # 最小值
print(np.max(data))        # 最大值
print(np.ptp(data))        # 极差（max-min）
print(np.percentile(data, 25))  # 25%分位数（下四分位）
print(np.percentile(data, 75))  # 75%分位数
print(np.percentile(data, [25, 50, 75]))  # 一次性多个分位数

# 求和/积
print(np.sum(data))
print(np.prod(data))       # 乘积

# 忽略 NaN 的版本（数据有缺失时用）
data_nan = np.array([1.0, 2.0, np.nan, 4.0])
print(np.nanmean(data_nan))   # → 2.33（忽略 NaN 求均值）
print(np.nansum(data_nan))
# 实际处理实验数据时 NaN 很常见，numpy 提供了全套 nan 函数

# 协方差与相关系数
x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 6, 8, 10])
print(np.corrcoef(x, y))       # 相关系数矩阵（完美正相关=1）
print(np.cov(x, y))            # 协方差矩阵

# ============================================================
# 二、唯一值与计数
# ============================================================
data = np.array([1, 2, 2, 3, 3, 3, 4])
print(np.unique(data))             # → [1 2 3 4]（去重）
print(np.unique(data, return_counts=True))
# → (array([1,2,3,4]), array([1,2,3,1]))（值和各自出现次数）
# 统计频次，等价于 pandas 的 value_counts

# ============================================================
# 三、线性代数（np.linalg）
# ============================================================
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print(A @ B)                 # 矩阵乘法
print(np.dot(A, B))          # 等价
print(A.T)                   # 转置
print(np.linalg.det(A))      # 行列式 → -2.0
print(np.linalg.inv(A))      # 逆矩阵
print(np.linalg.eig(A))      # 特征值、特征向量

# 解线性方程组 Ax = b：
A = np.array([[3, 1], [1, 2]])
b = np.array([9, 8])
x = np.linalg.solve(A, b)
print(x)                     # → [2. 3.]（x=2, y=3）
# 方程组：3x+y=9, x+2y=8 → 解 x=2,y=3 ✅

# 最小二乘（科研拟合的基础）
# np.linalg.lstsq(A, b) 解最小二乘问题

# ============================================================
# 四、性能对比：numpy vs Python 循环
# ============================================================
import time

n = 1_000_000
arr = np.arange(n)

# Python 循环求和
t0 = time.time()
total = 0
for i in arr:
    total += i
t_loop = time.time() - t0

# numpy 求和
t0 = time.time()
total2 = arr.sum()
t_numpy = time.time() - t0

print(f"Python循环: {t_loop*1000:.1f} ms")
print(f"numpy:      {t_numpy*1000:.3f} ms")
print(f"numpy 快 {t_loop/t_numpy:.0f} 倍")
# 通常 numpy 快 50~200 倍！

# ============================================================
# 五、向量化思想（numpy 的灵魂）
# ============================================================
# ❌ 错误习惯：用 Python 循环逐元素处理
# data = []
# for x in raw_data:
#     data.append((x - mean) / std)    # 慢

# ✅ 正确习惯：一次操作整个数组
# normalized = (raw_data - mean) / std   # 快几百倍

# 规则：能不用循环就不用循环，让 numpy 向量化
# 向量化代码：更短、更快、更不容易出 bug

# ============================================================
# 六、内存与性能提示
# ============================================================
# 1. 避免循环内 append（创建新数组）
# 2. 用对 dtype（float64 默认，够用）
# 3. 大数据优先用 numpy 而不是 Python list
# 4. 处理大型矩阵时用 inplace 操作（+= 比 + 省内存）
# 5. 能用布尔索引别用 where 循环

# ============================================================
# 七、实战：数据标准化（z-score）
# ============================================================
# 论文/机器学习常用：把数据变成均值0、标准差1
data = np.array([12.3, 13.1, 11.8, 12.9, 13.5, 12.7, 13.2, 12.4])

mean = data.mean()
std = data.std()
zscore = (data - mean) / std      # 向量化，一行搞定

print("原始均值：", data.mean())
print("标准化后均值：", zscore.mean())   # → ~0（浮点误差）
print("标准化后标准差：", zscore.std())  # → 1
