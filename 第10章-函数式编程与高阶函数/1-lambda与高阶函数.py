# ============================================================
# 函数式编程 ① — lambda 与高阶函数
# ============================================================
# 函数式编程 = 把"函数"当"值"一样使用：
# 可以传来传去、可以当场创建、可以嵌套返回。
# 配合数据处理（pandas/sklearn）非常实用。

# ============================================================
# 一、lambda 匿名函数
# ============================================================
# 定义：lambda 参数: 表达式（只能写一行，自动返回结果）
# 等价于：
#   def 函数名(参数): return 表达式

# 传统写法
def double(x):
    return x * 2

# lambda 写法
double_l = lambda x: x * 2

print(double(5))        # → 10
print(double_l(5))      # → 10

# 多参数
add = lambda a, b: a + b
print(add(3, 4))        # → 7

# 什么时候用 lambda？
# 一次性使用、逻辑简单 → 用 lambda
# 逻辑复杂、要复用     → 用 def

# ============================================================
# 二、高阶函数：函数作为参数
# ============================================================
# 高阶函数 = 接收函数作为参数，或返回函数的函数
# Python 内置三个最常用的：sorted / max / min 都支持 key 参数

# ① sorted 的 key 参数（超常用！）
data = ["12", "3", "125", "45"]
print(sorted(data))                    # 字符串排序 → ['12', '125', '3', '45']
print(sorted(data, key=int))           # 按数值排序 → ['3', '12', '45', '125']
print(sorted(data, key=lambda s: len(s)))  # 按长度排序

# ② 按字典的值排序（处理数据神器）
samples = {"样品A": 0.523, "样品B": 1.014, "样品C": 0.098}
# 按吸光度从高到低排
ranked = sorted(samples.items(), key=lambda item: item[1], reverse=True)
print(ranked)   # → [('样品B', 1.014), ('样品A', 0.523), ('样品C', 0.098)]

# ③ max/min 的 key 参数
numbers = [3, 17, 5, 9]
print(max(numbers))                    # → 17
print(max(numbers, key=lambda x: -x))  # 找"最小"的取法：按-x最大

# ④ 列表排序 sort 也支持 key
lst = [(1, 9), (3, 2), (2, 5)]
lst.sort(key=lambda t: t[1])           # 按第二个元素排序
print(lst)   # → [(3, 2), (2, 5), (1, 9)]

# ============================================================
# 三、常用高阶函数（了解 + 会用）
# ============================================================
# map：把函数作用到每个元素
nums = [1, 2, 3, 4]
squared = list(map(lambda x: x ** 2, nums))
print(squared)   # → [1, 4, 9, 16]
# 等价列表推导式（更 Pythonic）：
# squared = [x ** 2 for x in nums]

# filter：按条件过滤
even = list(filter(lambda x: x % 2 == 0, nums))
print(even)      # → [2, 4]
# 等价推导式：[x for x in nums if x % 2 == 0]

# reduce：累积计算（在 functools 里）
from functools import reduce
total = reduce(lambda a, b: a + b, nums)
print(total)     # → 10（1+2+3+4）
# 等价：sum(nums)

# 老师建议：
#   map/filter/reduce 都能用推导式替代，推导式更易读。
#   了解它们（面试/读别人代码用），日常用推导式。

# ============================================================
# 四、函数作为返回值（闭包 Closures）
# ============================================================
# 闭包 = 函数 + 它记住的外部变量环境
def make_multiplier(n):
    def multiplier(x):
        return x * n        # 记住外部变量 n
    return multiplier

times_2 = make_multiplier(2)
times_3 = make_multiplier(3)
print(times_2(10))   # → 20
print(times_3(10))   # → 30

# 闭包实战：生成一系列"校准函数"
def make_calibrator(a, b):
    """生成 y = a*x + b 的校准函数（标准曲线系数固定后复用）"""
    def calibrate(x):
        return a * x + b
    return calibrate

cal_curve = make_calibrator(0.985, -0.012)   # 标准曲线：y=0.985x-0.012
print(cal_curve(0.5))   # → 0.4805（预测浓度）

# ============================================================
# 五、实战：用 lambda 处理实验数据
# ============================================================
# 场景：一组浓度-吸光度数据，想按浓度排序、找最大值
data = [
    {"浓度": 0.1, "吸光度": 0.05},
    {"浓度": 1.0, "吸光度": 0.52},
    {"浓度": 0.5, "吸光度": 0.26},
    {"浓度": 2.0, "吸光度": 1.01},
]

# 按浓度排序
data_sorted = sorted(data, key=lambda d: d["浓度"])
print("按浓度排序：")
for d in data_sorted:
    print(f"  浓度 {d['浓度']} → 吸光度 {d['吸光度']}")

# 找吸光度最大的样品
best = max(data, key=lambda d: d["吸光度"])
print("吸光度最大：", best)

# 计算浓度>0.5的样品吸光度之和
high = sum(d["吸光度"] for d in data if d["浓度"] > 0.5)
print("高浓度样品吸光度和：", high)

# ============================================================
# 六、总结
# ============================================================
# lambda：一行匿名函数（逻辑简单时用）
# key 参数：sorted/max/min 按自定义规则（超常用）
# 闭包：函数记住外部变量（做"定制函数工厂"）
# map/filter/reduce：能用推导式替代，了解即可
