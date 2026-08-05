# ============================================================
# 常用标准库 — 写真实程序天天用的工具
# ============================================================
# 标准库 = Python 自带，无需安装。这里挑最常用的几个。

# ============================================================
# 一、math — 数学函数
# ============================================================
import math
print(math.sqrt(16))       # → 4.0（平方根）
print(math.pi)             # → 3.141592653589793（圆周率）
print(math.ceil(3.1))      # → 4（向上取整）
print(math.floor(3.9))     # → 3（向下取整）
print(math.fabs(-5))       # → 5.0（绝对值）
print(math.pow(2, 10))     # → 1024.0（幂，结果 float）


# ============================================================
# 二、random — 随机数
# ============================================================
import random
print(random.random())          # → 0~1 之间的小数
print(random.randint(1, 100))   # → 1~100 随机整数（闭区间）
print(random.choice(["A", "B", "C"]))  # 随机选一个
print(random.sample([1, 2, 3, 4, 5], 2))  # 随机取 2 个（不重复）
lst = [1, 2, 3, 4, 5]
random.shuffle(lst)             # 原地打乱
print(lst)                      # → 顺序随机
# 注意：random 不是真随机（伪随机），够用就行


# ============================================================
# 三、datetime — 日期时间
# ============================================================
from datetime import datetime, date

now = datetime.now()            # 当前时间
print(now)                      # → 2026-08-05 14:30:00.123456

# 格式化：strftime = string format time
print(now.strftime("%Y-%m-%d"))           # → 2026-08-05
print(now.strftime("%H:%M:%S"))           # → 14:30:00
print(now.strftime("%Y年%m月%d日 %H:%M")) # → 2026年08月05日 14:30

# 字符串转日期
d = datetime.strptime("2026-01-01", "%Y-%m-%d")
print(d)                        # → 2026-01-01 00:00:00
# strptime 格式必须和字符串匹配，否则报错


# ============================================================
# 四、json — 数据交换格式（非常重要！）
# ============================================================
# JSON 是互联网最通用的数据格式，API 返回的数据基本都是 JSON。
# Python 字典 ↔ JSON 字符串互转。
import json

data = {"name": "小明", "age": 18, "scores": [90, 85, 92]}

# 字典 → JSON 字符串
json_str = json.dumps(data, ensure_ascii=False)   # ensure_ascii=False 保留中文
print(json_str)      # → {"name": "小明", "age": 18, "scores": [90, 85, 92]}

# JSON 字符串 → 字典
back = json.loads(json_str)
print(back["name"])  # → 小明

# 字典 ↔ 文件
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)   # dump：直接写文件

with open("data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)                    # load：直接从文件读
print(loaded["age"])   # → 18
# 记住：dumps/loads 是字符串，dump/load 是文件


# ============================================================
# 五、csv — 表格数据
# ============================================================
# CSV = 逗号分隔的值，Excel 能直接打开。
import csv

# 写入
with open("data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["姓名", "分数"])       # 表头
    writer.writerow(["小明", 90])
    writer.writerow(["小红", 85])

# 读取
with open("data.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)      # → ['姓名', '分数'] / ['小明', '90'] 等
# 科研数据大多能存成 CSV，pandas 读 CSV 更是标配


# ============================================================
# 六、小结：什么时候用哪个
# ============================================================
# 数学计算        → math
# 随机            → random
# 时间日期        → datetime
# 网络数据交换    → json（API 数据）
# 表格数据        → csv（Excel 打开）
# 文件/路径       → os、pathlib
# 复制            → copy（浅拷贝/深拷贝）
# 系统信息        → sys
