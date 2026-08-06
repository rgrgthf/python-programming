# ============================================================
# 函数式编程 ② — map/filter/reduce 与推导式全家桶
# ============================================================
# 这一节把"批量处理数据"的几种写法讲透。
# 处理实验数据时，80% 的操作都是"对每个元素做点什么"。

# ============================================================
# 一、推导式（最推荐，Pythonic）
# ============================================================
# ① 列表推导式
squares = [x ** 2 for x in range(5)]
print(squares)   # → [0, 1, 4, 9, 16]

# 带条件
even_sq = [x ** 2 for x in range(10) if x % 2 == 0]
print(even_sq)   # → [0, 4, 16, 36, 64]

# ② 字典推导式
squares_dict = {x: x ** 2 for x in range(5)}
print(squares_dict)   # → {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# ③ 集合推导式（去重）
unique = {x % 3 for x in range(10)}
print(unique)    # → {0, 1, 2}

# ④ 生成器表达式（大数据用，惰性）
gen = (x ** 2 for x in range(5))   # 圆括号 = 生成器
print(gen)                         # → <generator object>
print(sum(gen))                    # → 30（直接用一次）

# ============================================================
# 二、map / filter / reduce 对照
# ============================================================
nums = [1, 2, 3, 4, 5]

# map（映射）：每个元素应用函数
#   推导式：  [x*2 for x in nums]
#   map写法： list(map(lambda x: x*2, nums))
print([x * 2 for x in nums])                 # → [2,4,6,8,10]

# filter（过滤）：保留满足条件的
#   推导式：  [x for x in nums if x > 2]
#   filter： list(filter(lambda x: x > 2, nums))
print([x for x in nums if x > 2])            # → [3,4,5]

# reduce（累积）：两两合并
#   推导式没有直接替代，但 sum/min/max 覆盖了大部分场景
from functools import reduce
print(reduce(lambda a, b: a * b, nums))      # → 120（连乘）

# 结论：日常用推导式 + sum/min/max，map/filter/reduce 了解即可

# ============================================================
# 三、多重推导式（嵌套）
# ============================================================
# 两个列表交叉组合
colors = ["红", "蓝"]
sizes = ["大", "小"]
combos = [f"{c}{s}" for c in colors for s in sizes]
print(combos)   # → ['红大', '红小', '蓝大', '蓝小']

# 展平二维列表
matrix = [[1, 2], [3, 4], [5, 6]]
flat = [x for row in matrix for x in row]
print(flat)     # → [1, 2, 3, 4, 5, 6]

# ============================================================
# 四、实战：数据处理中的推导式应用
# ============================================================
# 场景1：清洗数据——把所有浓度值从字符串转浮点数并过滤异常
raw = ["0.1", "0.5", "-3", "2.0", "N/A", "1.5"]
# 先转数字，过滤掉无法转换的和负数
clean = [float(x) for x in raw if x.replace(".", "").isdigit() and float(x) > 0]
print(clean)    # → [0.1, 0.5, 2.0, 1.5]

# 场景2：把重复样品名去重（保持顺序）
samples = ["A1", "B2", "A1", "C3", "B2"]
seen = set()
unique = [s for s in samples if not (s in seen or seen.add(s))]
print(unique)   # → ['A1', 'B2', 'C3']

# 场景3：从字典列表提取某一列（pandas 之前的手动版）
data = [{"name": "A", "value": 1}, {"name": "B", "value": 2}]
names = [d["name"] for d in data]
print(names)    # → ['A', 'B']

# ============================================================
# 五、zip 的妙用（并行遍历 + 解包）
# ============================================================
# ① 并行遍历两个列表
names = ["甲", "乙", "丙"]
scores = [85, 92, 78]
for name, score in zip(names, scores):
    print(f"{name}: {score}")

# ② zip 后转字典（快速配对）
pairs = dict(zip(names, scores))
print(pairs)    # → {'甲': 85, '乙': 92, '丙': 78}

# ③ * 解包还原
a, b = zip(*pairs.items())
print(a, b)     # → ('甲', '乙', '丙') ('85', '92', '78')

# ============================================================
# 六、enumerate / any / all 速查
# ============================================================
# enumerate：同时拿索引和值
for i, name in enumerate(names, start=1):
    print(f"第{i}个: {name}")

# any：有任何一个满足
print(any(x > 90 for x in scores))    # → False
# all：全部满足
print(all(x > 60 for x in scores))    # → True

# ============================================================
# 七、总结：怎么选？
# ============================================================
# 简单遍历修改   → 推导式（[x for x in ...]）
# 取和/最大/最小 → sum()/max()/min()
# 需要索引       → enumerate()
# 并行遍历       → zip()
# 判断存在性     → any()/all()
# 复杂逻辑       → 普通 for 循环（可读性优先）
