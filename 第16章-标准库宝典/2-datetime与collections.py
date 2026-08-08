# ============================================================
# 标准库宝典 ② — datetime 与 collections
# ============================================================
# datetime：处理日期时间（实验记录、时间序列）
# collections：高级容器（计数器、默认字典、有序字典...）

# ============================================================
# 一、datetime 基础
# ============================================================
from datetime import datetime, date, time, timedelta

# 当前时间
now = datetime.now()
print(now)                    # → 2026-08-06 14:30:00.123456
print(now.year, now.month, now.day)     # → 2026 8 6
print(now.hour, now.minute)             # → 14 30

# 手动创建
t1 = datetime(2026, 8, 6, 9, 30)
print(t1)                     # → 2026-08-06 09:30:00

# 只看日期 / 只看时间
d = date(2026, 8, 6)
tm = time(14, 30, 0)

# ============================================================
# 二、格式化与解析（最重要！）
# ============================================================
# strftime：日期 → 字符串（f = format）
now = datetime.now()
print(now.strftime("%Y-%m-%d"))            # → 2026-08-06
print(now.strftime("%H:%M:%S"))            # → 14:30:00
print(now.strftime("%Y年%m月%d日 %A"))      # → 2026年08月06日 Thursday

# strptime：字符串 → 日期（p = parse，解析）
s = "2026-08-06 14:30"
parsed = datetime.strptime(s, "%Y-%m-%d %H:%M")
print(parsed)                 # → 2026-08-06 14:30:00

# 常用格式码：
# %Y 年(4位) %m 月(2位) %d 日 %H 时(24h) %M 分 %S 秒
# %A 星期全称 %a 星期简称 %B 月份全称

# ============================================================
# 三、时间运算（timedelta）
# ============================================================
# 加/减天数
today = date.today()
print(today)                           # 今天
print(today + timedelta(days=7))       # 一周后
print(today - timedelta(days=30))      # 一个月前（按30天算）

# 两个日期差
start = datetime(2026, 1, 1)
end = datetime(2026, 8, 6)
diff = end - start
print(diff)                  # → 217 days, 0:00:00
print(diff.days)             # → 217（天数）

# 实战：计算实验周期
exp_start = datetime(2026, 8, 1, 9, 0)
exp_end = datetime(2026, 8, 6, 15, 30)
hours = (exp_end - exp_start).total_seconds() / 3600
print(f"实验持续 {hours:.1f} 小时")   # → 实验持续 126.5 小时

# ============================================================
# 四、collections.Counter（计数器——统计神器！）
# ============================================================
from collections import Counter

# 统计列表元素出现次数
drugs = ["阿司匹林", "布洛芬", "阿司匹林", "氯雷他定", "阿司匹林", "布洛芬"]
count = Counter(drugs)
print(count)            # → Counter({'阿司匹林': 3, '布洛芬': 2, '氯雷他定': 1})
print(count["阿司匹林"]) # → 3

# 出现最多的前2个
print(count.most_common(2))   # → [('阿司匹林', 3), ('布洛芬', 2)]

# 统计字符串字符（第3章作业的进阶版！）
text = "hello python"
print(Counter(text))    # → Counter({'h': 2, ...})

# ============================================================
# 五、collections.defaultdict（带默认值的字典）
# ============================================================
from collections import defaultdict

# 普通字典：访问不存在的键会 KeyError
# 默认字典：自动给默认值（不会报错）

# 场景：按组收集数据
groups = defaultdict(list)          # 默认值是空列表
data = [("对照组", 0.5), ("给药组", 1.2), ("对照组", 0.6)]
for group, value in data:
    groups[group].append(value)     # 不用先判断键存不存在！
print(dict(groups))
# → {'对照组': [0.5, 0.6], '给药组': [1.2]}

# 对比普通字典的麻烦写法：
groups2 = {}
for group, value in data:
    if group not in groups2:
        groups2[group] = []
    groups2[group].append(value)

# 计数默认字典
word_count = defaultdict(int)       # 默认值是0
for w in ["a", "b", "a", "c"]:
    word_count[w] += 1              # 不用先初始化
print(dict(word_count))             # → {'a': 2, 'b': 1, 'c': 1}

# ============================================================
# 六、其他 collections 工具
# ============================================================
from collections import OrderedDict, deque, namedtuple

# deque：双端队列（两端都能快速增删）
dq = deque([1, 2, 3])
dq.appendleft(0)        # 左边加
dq.append(4)            # 右边加
print(list(dq))         # → [0, 1, 2, 3, 4]
dq.popleft()            # 左边取
print(list(dq))         # → [1, 2, 3, 4]

# namedtuple：有名字的元组（比字典省内存，代码更清晰）
from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])
pt = Point(3, 4)
print(pt.x, pt.y)       # → 3 4（不用 pt[0]）

# 实战：样品记录用 namedtuple
Sample = namedtuple("Sample", ["id", "conc", "absorbance"])
s1 = Sample("A1", 0.5, 0.26)
s2 = Sample("A2", 1.0, 0.52)
print(f"{s1.id}: 浓度{s1.conc} 吸光度{s1.absorbance}")

# ============================================================
# 七、总结
# ============================================================
# datetime：strftime格式化 / strptime解析 / timedelta运算
# Counter：计数统计 most_common
# defaultdict：带默认值的字典（分组收集数据神器）
# namedtuple：轻量结构体（比字典快，代码清晰）

# ============================================================
# 八、易错点汇总
# ============================================================
# 1. strftime 和 strptime 别搞混：
#    strftime = 日期→字符串（f）；strptime = 字符串→日期（p）
# 2. strptime 的格式必须和字符串【完全一致】，否则报错
# 3. datetime 和 date 是不同类：date 没有 hour/minute
# 4. timedelta 相减要先转成 datetime 或 date（同类型才能减）
# 5. Counter.most_common(n) 返回元组列表，不是字典
# 6. defaultdict 的默认值工厂要传【函数】不是值：
#    defaultdict(list) 是函数；defaultdict([]) 是错的！

# ============================================================
# 九、自测（40%基础 + 40%中等 + 20%挑战）
# ============================================================
# 【基础】
# 1. strftime 和 strptime 分别把什么转成什么？
# 2. Counter 和普通字典有什么区别？
# 3. defaultdict(list) 里 list 为什么要写函数名不带括号？
#
# 【中等】
# 4. 用 strptime 解析 "2026-08-06 14:30" 并输出星期几。
# 5. 用 Counter 统计一段文字里每个字符出现次数。
# 6. 用 defaultdict 把数据按组收集（对照组/给药组）。
#
# 【挑战】
# 7. 计算两次实验时间差，输出持续多少小时。
# 8. 用 namedtuple 定义 Sample 记录，创建两个样品并读取属性。
