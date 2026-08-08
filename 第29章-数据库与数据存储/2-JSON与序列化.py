# ============================================================
# 数据库 ② — JSON 与数据序列化
# ============================================================
# 数据存储的几种格式，各有用武之地：
#   CSV/Excel：人看得懂，表格数据
#   JSON：程序间交换，API 的标准格式
#   pickle：Python 对象原样存（含自定义对象）
#   SQLite：大数据量查询（上一节）

import json

# ============================================================
# 一、JSON：Python 字典 ↔ 字符串/文件
# ============================================================
data = {
    "项目": "标准曲线",
    "样品数": 7,
    "浓度": [0, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0],
    "拟合": {"斜率": 0.498, "截距": 0.003, "R2": 0.9995},
    "备注": None,
}

# 字典 → JSON字符串
json_str = json.dumps(data, ensure_ascii=False, indent=2)
print(json_str)          # ensure_ascii=False 保留中文，indent 美化

# JSON字符串 → 字典
back = json.loads(json_str)
print(back["拟合"]["斜率"])    # → 0.498

# 字典 → 文件
with open("result.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 文件 → 字典
with open("result.json", encoding="utf-8") as f:
    loaded = json.load(f)
print(loaded["项目"])     # → 标准曲线

# ============================================================
# 二、pickle：Python 对象原样保存
# ============================================================
import pickle

# pickle 可以存任何 Python 对象（含函数、类实例）
class Drug:
    def __init__(self, name, price):
        self.name = name
        self.price = price

d = Drug("氯雷他定", 22.8)

# 保存
with open("drug.pkl", "wb") as f:      # 二进制模式
    pickle.dump(d, f)

# 读取
with open("drug.pkl", "rb") as f:
    d2 = pickle.load(f)
print(d2.name, d2.price)    # → 氯雷他定 22.8（类对象完整恢复）

# pickle 的应用（你已经见过！）：
#   sklearn 模型保存用 joblib（就是 pickle 的优化版，第15章）
#   import joblib
#   joblib.dump(model, "model.pkl")
#   model = joblib.load("model.pkl")

# ⚠️ 安全提醒：永远不要加载来路不明的 pickle 文件（可执行恶意代码）

# ============================================================
# 三、JSON vs pickle 怎么选？
# ============================================================
# JSON：
#   + 跨语言通用（别的程序也能读）
#   + 人类可读、可手动编辑
#   + 适合 API/配置文件/数据交换
#   - 只支持基本类型
#
# pickle：
#   + 存任何 Python 对象
#   + 读回速度快
#   - 只有 Python 能用
#   - 有安全风险
#
# 结论：数据交换用 JSON，模型/对象持久化用 pickle/joblib

# ============================================================
# 四、CSV 深入（表格数据）
# ============================================================
import csv

# 写 CSV
with open("samples.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["样品", "浓度", "吸光度"])
    writer.writerow(["A1", 0.5, 0.26])
    writer.writerow(["A2", 1.0, 0.52])

# 读 CSV
with open("samples.csv", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)    # → {'样品': 'A1', '浓度': '0.5', '吸光度': '0.26'}

# 但日常更推荐 pandas：
# import pandas as pd
# df = pd.read_csv("samples.csv")
# df.to_csv("out.csv", index=False)

# ============================================================
# 五、配置文件的常用格式
# ============================================================
# 小型配置：直接写 .py 或 .json
# 环境变量：os.environ（第16章）

# ============================================================
# 六、总结：数据存储决策表
# ============================================================
# 表格数据、人要看的  → CSV / Excel（pandas）
# 程序交换、API       → JSON
# 模型/对象持久化     → pickle / joblib
# 大量数据、要查询    → SQLite
# 简单配置           → JSON / .py
#
# 原则：能用简单的别用复杂的，选"最合适"不选"最强大"

# ============================================================
# 六、易错点汇总
# ============================================================
# 1. JSON 的键必须是字符串，Python 元组会变列表，
#    自定义对象要写默认转换（default=）才能 dumps
# 2. json.dumps 里 ensure_ascii=False 才能保留中文
# 3. loads 解析失败会抛异常，要 try/except 处理
# 4. dump/load 是文件，dumps/loads 是字符串——别混
# 5. 复杂嵌套数据（字典套列表套字典）JSON 都能存，
#    但太深的别硬塞 JSON，考虑数据库
# 6. 存储选择：简单配置用 JSON，大量结构化数据用 SQLite

# ============================================================
# 七、自测（40%基础 + 40%中等 + 20%挑战）
# ============================================================
# 【基础】
# 1. dump/load 和 dumps/loads 的区别？
# 2. 中文怎么在 JSON 里保留？
# 3. JSON 键必须是什么类型？
#
# 【中等】
# 4. 把字典序列化到文件再读回来。
# 5. 处理 loads 解析失败的异常。
# 6. 把自定义对象序列化成 JSON。
#
# 【挑战】
# 7. 写一个实验记录：用 JSON 保存并读回。
# 8. 对比 JSON 和 SQLite 的适用场景，各举一个例子。
