# ============================================================
# 📘 第8章·第5节：常用标准库 — 写真实程序天天用的工具
# ============================================================
# 标准库 = Python 自带、无需安装、随时 import。
# 这一节是【实用手册】：每个库都讲"什么时候用 + 怎么用 + 药学例子"。
# 不用背，用的时候回来查就行——但要知道"有这个东西可用"。

# ============================================================
# 一、math — 数学函数
# ============================================================
import math
print(math.sqrt(16))       # → 4.0（平方根）
print(math.pi)             # → 3.141592653589793（圆周率）
print(math.ceil(3.1))      # → 4（向上取整：3.1→4）
print(math.floor(3.9))     # → 3（向下取整：3.9→3）
print(math.fabs(-5))       # → 5.0（绝对值，返回 float）
print(math.pow(2, 10))     # → 1024.0（幂，结果 float）

# 更多常用（了解即可，用到再查）：
#   math.log(x) 对数 / math.exp(x) e的x次方 /
#   math.sin/cos/tan 三角函数 / math.factorial(n) 阶乘 /
#   math.gcd(a,b) 最大公约数（算配比很有用）/
#   math.isclose(a,b) 浮点数近似比较（实验数据判等用这个，别用 ==）

# ---------- 药学应用：浮点数比较必须用 isclose ----------
# 0.1 + 0.2 == 0.3  → False！（浮点数精度问题）
print(0.1 + 0.2 == 0.3)              # → False（别用 == 比较浮点数！）
print(math.isclose(0.1 + 0.2, 0.3))  # → True（用 isclose 才对）
# 实验数据判等、算浓度对错，都应该用 isclose 或设定容差。

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

# ---------- random 的关键知识点 ----------
# ① 伪随机：它不是真随机，是算法生成的"看起来随机"的序列。
#    但对你 99% 的场景足够（抽奖、抽样、随机分组）。
# ② random.seed(数字)：固定随机种子 → 结果可复现！
#    写实验/写作业要"每次结果一样"时，加一行 seed 就行：
random.seed(42)
print(random.random())   # → 0.6394267984578837（每次固定这个数）
random.seed(42)
print(random.random())   # → 再次相同 → 可复现！
# ③ 药学应用：随机分组（随机抽样做对照实验）
#    把 30 只小鼠随机分 3 组：random.sample 或 shuffle+切片


# ============================================================
# 三、datetime — 日期时间
# ============================================================
from datetime import datetime, date, timedelta

now = datetime.now()            # 当前时间
print(now)                      # → 2026-08-05 14:30:00.123456

# 格式化输出：strftime = string format time（把时间变成字符串）
print(now.strftime("%Y-%m-%d"))           # → 2026-08-05
print(now.strftime("%H:%M:%S"))           # → 14:30:00
print(now.strftime("%Y年%m月%d日 %H:%M")) # → 2026年08月05日 14:30

# 字符串转日期：strptime = string parse time（把字符串解析成时间）
d = datetime.strptime("2026-01-01", "%Y-%m-%d")
print(d)                        # → 2026-01-01 00:00:00
# ⚠️ strptime 的格式必须和字符串【完全匹配】，否则报错

# ---------- 常用格式符（记这几个就够）----------
# %Y 年份(4位)  %m 月份(2位)  %d 日  %H 小时(24)  %M 分钟  %S 秒
# %y 年份(2位)  %I 小时(12)  %p 上午/下午

# ---------- 时间运算：timedelta ----------
# 两个时间相减得到 timedelta，可以做"几天后/几小时前"：
today = datetime.now()
print(today + timedelta(days=7))        # → 7 天后
print(today - timedelta(hours=3))       # → 3 小时前

# ---------- 药学应用：实验日期管理 ----------
# 计算"药品保质期""配液效期"等：
make = datetime(2026, 8, 1, 9, 0)        # 某天 9 点配的液
valid = make + timedelta(hours=24)       # 24 小时效期
print(valid.strftime("%m月%d日 %H:%M")) # → 08月02日 09:00

# 注意：datetime 带日期时间；如果只要日期用 date，
#   只要时间用 time。不要混着用。


# ============================================================
# 四、json — 数据交换格式（非常重要！）
# ============================================================
# JSON 是互联网最通用的数据格式，API 返回的数据基本都是 JSON。
# Python 的字典/列表 ↔ JSON 文本，几乎一一对应，所以能互转。
import json

data = {"name": "小明", "age": 18, "scores": [90, 85, 92]}

# 字典 → JSON 字符串（dumps = dump string）
json_str = json.dumps(data, ensure_ascii=False)   # ensure_ascii=False 保留中文
print(json_str)      # → {"name": "小明", "age": 18, "scores": [90, 85, 92]}

# JSON 字符串 → 字典（loads = load string）
back = json.loads(json_str)
print(back["name"])  # → 小明

# 字典 ↔ 文件（dump / load 不带 s = 直接对文件操作）
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)   # dump：直接写文件

with open("data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)                    # load：直接从文件读
print(loaded["age"])   # → 18

# ---------- 记忆法 ----------
#   dumps / loads  = 和【字符串】打交道（s = string）
#   dump  / load   = 和【文件】打交道
# 就这么简单。

# ---------- 药学应用：存/读结构化数据 ----------
# 比如把"今天配了几张处方"存成 JSON，下次直接读：
rx = {"2026-08-05": ["氯雷他定", "阿莫西林"], "2026-08-06": ["布洛芬"]}
with open("rx.json", "w", encoding="utf-8") as f:
    json.dump(rx, f, ensure_ascii=False, indent=2)   # indent=2 格式化好看
# 以后做实验记录、存配置、存中间结果，JSON 都是首选。


# ============================================================
# 五、csv — 表格数据（实验数据的最爱）
# ============================================================
# CSV = 逗号分隔的值，Excel/WPS 能直接打开，科研数据标配格式。
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
# 注意：读出来全是字符串（'90' 是 str），要算数先 int()/float() 转
# 科研数据大多能存成 CSV；以后学 pandas，读 CSV 更是标配。

# ============================================================
# 六、os 和 pathlib — 文件与路径（必会）
# ============================================================
import os
print(os.getcwd())            # 当前工作目录
print(os.path.exists("data.csv"))   # 文件是否存在 → True
print(os.path.join("a", "b"))       # 拼接路径 → a\b（跨平台安全）
# 用 os.path.join 而不是手动写 "a/b"：Windows 用 \\，Linux 用 /，
# join 会自动处理，写出的代码到哪都能跑。

# 列出目录、创建文件夹、重命名：
#   os.listdir(目录)   列出文件
#   os.mkdir(目录)     新建文件夹（已存在会报错）
#   os.rename(旧, 新)  重命名
# 推荐现代写法 pathlib（更优雅）：
from pathlib import Path
p = Path("data.csv")
print(p.exists())         # → True
print(p.stem, p.suffix)   # → data .csv（文件名 / 扩展名）
# 记住：os 是经典，pathlib 是现代推荐，两者都会一点不吃亏。

# ============================================================
# 七、copy — 浅拷贝 vs 深拷贝（重要易错点！）
# ============================================================
# 直接 b = a 不是拷贝，是让两个名字指向【同一个列表】：
a = [1, 2, [3, 4]]
b = a                    # b 和 a 是同一个东西！
b.append(99)
print(a)                 # → [1, 2, [3, 4], 99]（a 也变了！）
# 想复制要显式拷贝：
import copy
import copy
# 浅拷贝（copy.copy）：外层复制，但【嵌套的列表还是共享】：
shallow = copy.copy(a)
shallow[2].append(5)     # 改嵌套列表
print(a[2])              # → [3, 4, 5]（a 的嵌套也被改了！）
# 深拷贝（copy.deepcopy）：连嵌套内容也彻底复制，互不影响：
deep = copy.deepcopy(a)
deep[2].append(6)
print(a[2])              # → [3, 4, 5]（不受影响）
# 口诀：普通赋值=共用；copy=浅拷贝(外壳独立)；deepcopy=深拷贝(全独立)。
# 有嵌套结构（列表套列表/字典套列表）要独立，用 deepcopy。

# ============================================================
# 八、小结：什么时候用哪个
# ============================================================
# 数学计算        → math
# 随机            → random
# 时间日期        → datetime
# 网络数据交换    → json（API 数据）
# 表格数据        → csv（Excel 打开）
# 文件/路径       → os、pathlib
# 复制            → copy（浅拷贝/深拷贝）
# 系统信息        → sys

# ============================================================
# 九、易错点汇总
# ============================================================
# 1. 浮点数别用 ==：用 math.isclose 或设容差
# 2. csv 读出来全是字符串，要计算先 int()/float()
# 3. random 是伪随机：需要可复现用 random.seed(数字)
# 4. strptime 格式必须和字符串完全匹配，否则报错
# 5. 复制嵌套结构用 copy.deepcopy，否则改了共享部分连累原数据
# 6. 拼路径用 os.path.join / pathlib，别手动写斜杠（跨平台会炸）

# ============================================================
# 十、自测（40%基础 + 40%中等 + 20%挑战）
# ============================================================
# 【基础】
# 1. 判断浮点数是否相等，为什么不能用 ==？应该用什么？
# 2. json 的 dumps/loads 和 dump/load 区别是什么？
# 3. csv 读出来的数字是什么类型？要计算怎么办？
#
# 【中等】
# 4. 写代码：用 random.seed(7) 后随机生成 3 个 1~10 的整数，
#    验证两次运行结果一致（可复现）。
# 5. 用 datetime 计算：今天 + 14 天是哪天？（并格式化输出）
# 6. 浅拷贝和深拷贝的根本区别？举例说明什么时候必须用深拷贝。
#
# 【挑战】
# 7. 用 csv 写一个"实验记录表"：表头[日期,药物,浓度,吸光度]，
#    写入 3 行数据，再读出来打印。（药代/分析实验常用）
# 8. 解释：为什么 a = b 改 b 会连累 a，而 copy.copy 有时也会连累？
#    什么时候 copy.copy 就够、什么时候必须 deepcopy？
