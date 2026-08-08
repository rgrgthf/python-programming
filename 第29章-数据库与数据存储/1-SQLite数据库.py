# ============================================================
# 数据库 ① — SQLite 入门
# ============================================================
# 数据存文件（Excel）够用，但数据多、要查询时要用数据库。
# SQLite = 最轻量的数据库（就一个文件，无需装服务器）。
# Python 内置 sqlite3 模块，零安装。

import sqlite3

# ============================================================
# 一、连接与建表
# ============================================================
# 连接（文件不存在会自动创建）
conn = sqlite3.connect("drugs.db")
cursor = conn.cursor()

# 建表（IF NOT EXISTS 防止重复建）
cursor.execute("""
CREATE TABLE IF NOT EXISTS drugs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    formula TEXT,
    weight REAL,
    smiles TEXT
)
""")
conn.commit()   # 提交（重要！）

# ============================================================
# 二、增（INSERT）
# ============================================================
# 单条插入（用 ? 占位符，防注入，规范写法）
cursor.execute(
    "INSERT INTO drugs (name, formula, weight, smiles) VALUES (?, ?, ?, ?)",
    ("阿司匹林", "C9H8O4", 180.16, "CC(=O)OC1=CC=CC=C1C(=O)O"),
)
cursor.execute(
    "INSERT INTO drugs (name, formula, weight, smiles) VALUES (?, ?, ?, ?)",
    ("布洛芬", "C13H18O2", 206.28, "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O"),
)
conn.commit()

# ============================================================
# 三、查（SELECT）
# ============================================================
# 查询全部
cursor.execute("SELECT * FROM drugs")
rows = cursor.fetchall()
for row in rows:
    print(row)   # → (1, '阿司匹林', 'C9H8O4', 180.16, '...')

# 带条件查询（WHERE）
cursor.execute("SELECT name, weight FROM drugs WHERE weight > 200")
print(cursor.fetchall())   # → [('布洛芬', 206.28)]

# 模糊查询（LIKE）
cursor.execute("SELECT name FROM drugs WHERE name LIKE '%布%'")
print(cursor.fetchall())

# 排序（ORDER BY）
cursor.execute("SELECT name, weight FROM drugs ORDER BY weight DESC")
print(cursor.fetchall())   # 按分子量从大到小

# ============================================================
# 四、改（UPDATE）和 删（DELETE）
# ============================================================
# 更新
cursor.execute("UPDATE drugs SET weight = 180.157 WHERE name = '阿司匹林'")
conn.commit()

# 删除
# cursor.execute("DELETE FROM drugs WHERE name = '布洛芬'")
# conn.commit()

# ============================================================
# 五、更安全的写法：with 上下文（自动提交/关闭）
# ============================================================
def query_all():
    """用 with 管理连接（自动提交和关闭）"""
    with sqlite3.connect("drugs.db") as conn:
        cursor = conn.execute("SELECT * FROM drugs")
        return cursor.fetchall()

print(query_all())

# ============================================================
# 六、pandas 直接读写 SQLite（神器！）
# ============================================================
import pandas as pd

# DataFrame → 数据库
df = pd.DataFrame([
    {"name": "氯雷他定", "formula": "C22H23ClN2O2", "weight": 382.88},
    {"name": "二甲双胍", "formula": "C4H11N5", "weight": 129.16},
])
df.to_sql("drugs", conn, if_exists="append", index=False)

# 数据库 → DataFrame
df2 = pd.read_sql("SELECT * FROM drugs", conn)
print(df2)

# ============================================================
# 七、SQL 速查（会用这些就够了）
# ============================================================
# CREATE TABLE 建表
# INSERT INTO ... VALUES 增
# SELECT ... FROM ... WHERE 查
# UPDATE ... SET ... WHERE 改
# DELETE FROM ... WHERE 删
# ORDER BY 排序  LIMIT 限量  LIKE 模糊
# COUNT(*) 计数  AVG() 平均  MAX()/MIN() 最值

# 聚合查询示例
cursor.execute("SELECT COUNT(*), AVG(weight), MAX(weight) FROM drugs")
print("数量/平均/最大分子量:", cursor.fetchone())

conn.close()   # 用完关闭

# ============================================================
# 八、总结
# ============================================================
# sqlite3.connect("文件.db") → 打开
# 占位符 ? 防注入
# commit() 提交 / close() 关闭
# pandas: df.to_sql / pd.read_sql 无缝衔接
# 应用：药物库、实验记录管理、Web应用的数据存储

# ============================================================
# 五、易错点汇总
# ============================================================
# 1. 执行写操作（INSERT/UPDATE/DELETE）后必须 conn.commit()，
#    否则不生效（自动关闭连接时可能丢）
# 2. 用完要 conn.close()，或用 with 上下文管理
# 3. 【绝不用字符串拼接 SQL】——会 SQL 注入；
#    用参数化：cursor.execute("... WHERE id=?", (id,))
# 4. 查询结果 fetchall() 返回元组列表，fetchone() 取一条
# 5. 表要先建（CREATE TABLE IF NOT EXISTS），否则查询报错
# 6. 频繁读写用事务批处理，别一条条 commit

# ============================================================
# 六、自测（40%基础 + 40%中等 + 20%挑战）
# ============================================================
# 【基础】
# 1. 写操作后为什么要 commit？
# 2. fetchall 和 fetchone 的区别？
# 3. 为什么不能用字符串拼接 SQL？
#
# 【中等】
# 4. 用 sqlite3 建一个药物表并插入几条数据。
# 5. 用参数化查询防止 SQL 注入。
# 6. 查询并打印所有记录。
#
# 【挑战】
# 7. 做一个简单的药物数据库：增删查改。
# 8. 解释 SQL 注入是什么，参数化为什么安全。
