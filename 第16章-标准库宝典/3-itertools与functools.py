# ============================================================
# 标准库宝典 ③ — itertools 与 functools
# ============================================================
# itertools：迭代工具（组合/排列/分组/无限序列）
# functools：函数工具（缓存/偏函数/装饰器辅助）

# ============================================================
# 一、itertools 常用工具
# ============================================================
import itertools

# ① 组合 combinations（不重复，顺序无关）
#    场景：从 N 个化合物里选 2 个组合（不考虑顺序）
for combo in itertools.combinations(["A", "B", "C"], 2):
    print(combo)   # → ('A','B') ('A','C') ('B','C')

# ② 排列 permutations（顺序有关）
for perm in itertools.permutations(["A", "B"], 2):
    print(perm)    # → ('A','B') ('B','A')

# ③ 笛卡尔积 product（所有搭配）
for p in itertools.product([1, 2], ["a", "b"]):
    print(p)       # → (1,'a') (1,'b') (2,'a') (2,'b')

# ④ chain：拼接多个可迭代对象
combined = list(itertools.chain([1, 2], [3, 4], [5]))
print(combined)    # → [1, 2, 3, 4, 5]

# ⑤ groupby：分组（注意：要数据已排序）
from itertools import groupby
data = [("A", 1), ("A", 2), ("B", 3), ("B", 4)]
for key, group in groupby(data, key=lambda x: x[0]):
    print(key, [g[1] for g in group])
# → A [1, 2]  B [3, 4]

# ⑥ 无限迭代器（配 break 用）
for i in itertools.count(10):
    if i > 13:
        break
    print(i, end=" ")   # → 10 11 12 13
print()

# ============================================================
# 二、itertools 实战：组合筛选（药学场景）
# ============================================================
# 场景：5 种药两两联用，评估所有组合
drugs = ["药A", "药B", "药C", "药D", "药E"]
combos = list(itertools.combinations(drugs, 2))
print(f"共 {len(combos)} 种两药组合")
for c in combos:
    print(f"  联用方案：{c[0]} + {c[1]}")

# 场景：多个浓度的全组合（做正交实验设计）
conc_levels = [0.1, 1.0, 10.0]      # 3个浓度
factors = ["温度", "pH", "时间"]     # 3个因素
designs = list(itertools.product(conc_levels, repeat=3))
print(f"正交实验共 {len(designs)} 组")

# ============================================================
# 三、functools 常用工具
# ============================================================
import functools

# ① lru_cache：自动缓存（第11章装饰器学过，回顾）
@functools.lru_cache(maxsize=128)
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(10))    # → 3628800（重复调用不重复计算）

# ② partial：偏函数（固定部分参数）
#    场景：统一设定绘图参数/读写参数
def write_report(title, author, content):
    return f"《{title}》 作者:{author}\n{content}"

# 生成一个"默认作者是我"的报告函数
write_mine = functools.partial(write_report, author="楠木")
print(write_mine("实验报告", "数据：0.523"))
# → 《实验报告》 作者:楠木\n数据：0.523

# ③ reduce：累积（第10章学过）
total = functools.reduce(lambda a, b: a + b, [1, 2, 3, 4])
print(total)    # → 10

# ④ wraps：保留装饰函数信息（写装饰器用）
# 见第11章-装饰器

# ============================================================
# 四、partial 实战：批量参数化
# ============================================================
# 场景：同一套代码，处理不同批次的实验数据
def process_batch(data, method="mean", verbose=False):
    if method == "mean":
        result = sum(data) / len(data)
    elif method == "max":
        result = max(data)
    else:
        result = min(data)
    if verbose:
        print(f"[{method}] 结果: {result}")
    return result

# 固定参数，生成专用函数
process_mean = functools.partial(process_batch, method="mean")
process_max = functools.partial(process_batch, method="max", verbose=True)

batch1 = [0.5, 0.8, 0.6]
print(process_mean(batch1))    # → 0.6333...
process_max(batch1)            # → [max] 结果: 0.8

# ============================================================
# 五、总结
# ============================================================
# itertools：combinations(组合) permutations(排列) product(全搭配)
#            groupby(分组) chain(拼接) count(计数)
# functools：lru_cache(缓存) partial(固定参数) reduce(累积)
# 这些是"标准库里的宝藏"，能让代码更短更清晰
