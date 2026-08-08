# ============================================================
# keyword 模块 — 查看和检测 Python 关键字
# ============================================================
import keyword#把 Python 内置的 keyword 模块加载进来

# ① 查看所有关键字（返回列表）
print(keyword.kwlist)#把 Python 内置的 keyword 模块加载进来
# Python 3.10+ 的输出示例：
# ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await',
#  'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
#  'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
#  'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return',
#  'try', 'while', 'with', 'yield']

# ② 查看关键字个数
print(len(keyword.kwlist))  # 当前版本的关键字数量（不同版本可能不同）

# ③ 判断某个词是否为关键字
print(keyword.iskeyword("if"))     # True — if 是关键字
print(keyword.iskeyword("print"))  # False — print 是内置函数，不是关键字
print(keyword.iskeyword("False"))  # True — False 是关键字

# ④ 软关键字（Soft Keywords）
# Python 3.10 引入了 match / case，它们是"软关键字"：
# 在某些上下文中是关键字，在其他地方仍可用作标识符
if hasattr(keyword, "softkwlist"):
    print(keyword.softkwlist)  # ['_', 'case', 'match']

# ============================================================
# 注意：关键字严格区分大小写！
# ============================================================
false = 100  # ✅ false（小写）不是关键字，可作变量名
# False = 100  # ❌ False（首字母大写）是关键字，不能用作变量名

# ============================================================
# 三、易错点 + 自测
# ============================================================
# 1. 关键字（True/False/None/if/for...）不能当变量名
# 2. 查看关键字：keyword.kwlist
# 3. 大小写敏感：true ≠ True
# 【基础】什么是关键字？【挑战】为什么 true 不等于 True？