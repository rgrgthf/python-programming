# ============================================================
# 第五章 阶段测试 — 列表 / 元组 / 字典 / 集合
# ============================================================
# 共 14 题：读代码、简答、找 bug、编程题
# 每题下方写答案，编程题写完整代码
# ============================================================


# ========== 一、列表 ==========

# 1.【读代码】写出输出结果：
print("第1题：")
lst = [1, 2, 3]
lst.append(4)
lst.insert(0, 0)
lst.pop()
lst[1] = 100
print(lst)
# 你的答案：
# ⏳ 已移至「重做练习3-数据结构.py」第 1 题
# 参考：lst=[1,2,3]→append→[1,2,3,4]→insert→[0,1,2,3,4]→pop→[0,1,2,3]→lst[1]=100→[0,100,2,3]

# 2.【读代码】写出输出结果（切片）：
print("第2题：")
lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(lst[2:6])
print(lst[-3:])
print(lst[::3])
print(lst[::-1][:3])
# 你的答案：
"""
第2题：
[2, 3, 4, 5]
[7, 8, 9]
[0,3,6,9]
[9,8,7]
"""

# 3.【读代码】写出输出结果（append vs extend）：
print("第3题：")
a = [1, 2]
a.append([3, 4])
b = [1, 2]
b.extend([3, 4])
print(a)
print(b)
# 你的答案：
"""
第3题：
[1,2,[3,4]]
[1,2,3,4]
"""

# 4.【简答】下面代码有什么问题？应该怎么改？
# lst = [3, 1, 2]
# print(lst.sort())
# 你的答案：
# ⏳ 已移至「重做练习3-数据结构.py」第 2 题
# 参考：sort() 原地排序并返回 None，print 出来是 None。
#      应写成：lst.sort(); print(lst)，或用 print(sorted(lst))


# ========== 二、元组 ==========

# 5.【读代码】写出 type() 的结果：
print("第5题：")
print(type((5)))
print(type((5,)))
print(type(()))
print(type((1, 2)))
# 你的答案：
"""
第5题：
int
tuple
tuple
tuple
"""

# 6.【简答】a, b = b, a 能交换两个变量的值，底层原理是什么？
# 你的答案：
"""
底层原理是元组的解包，b,a相当于一个元组，a, b = b, a相当于把这个元组解包给a,b
"""

# ========== 三、字典 ==========

# 7.【读代码】写出输出结果：
print("第7题：")
d = {"a": 1, "b": 2}
d["c"] = 3
d["a"] = 10
print(d)
print(d.get("x"))
print(d.get("x", 0))
print(list(d.keys()))
print(list(d.values()))
# 你的答案：
# ✏️ 订正：d.get("x") 不写默认值时返回 None（不是报错）
#   print(d)             → {'a': 10, 'b': 2, 'c': 3}
#   print(d.get("x"))    → None
#   print(d.get("x", 0)) → 0

# 8.【找 bug】下面代码想统计单词出现次数，但运行报错，为什么？怎么改？
# words = ["apple", "banana", "apple"]
# counts = {}
# for w in words:
#     counts[w] += 1
# print(counts)
# 你的答案（指出错误 + 写出修正代码）：
"""
bug出在counts[w] += 1，应该写成counts[w] = counts.get(w,0) + 1
"""

# 9.【简答】为什么列表不能当作字典的键？哪些类型可以当键？
# 你的答案：
# ✏️ 订正：除了 str 和 tuple，数字（int/float）也可以当键！
#   可当键：str、int、float、tuple（都是不可变类型）
#   不能当键：list、dict、set（都是可变类型）

# ========== 四、集合 ==========

# 10.【读代码】写出输出结果：
print("第10题：")
A = {1, 2, 3, 4}
B = {3, 4, 5}
print(A | B)
print(A & B)
print(A - B)
print(A ^ B)
print(list(set([1, 2, 2, 3, 3, 3])))
# 你的答案：
"""
第10题：
{1,2,3,4,5}
{3,4}
{1,2}
{1,2,5}
[1,2,3]
"""

# ========== 五、编程题 ==========

# 11.【编程】给一个列表 [5, 3, 8, 3, 1, 8, 5, 9]，去重后按升序输出。
print("第11题（你的代码写在下面）：")
# 你的答案：
# ⏳ 已移至「重做练习3-数据结构.py」第 3 题
# 参考：
# lst = [5, 3, 8, 3, 1, 8, 5, 9]
# unique = sorted(set(lst))
# print(unique)  # → [1, 3, 5, 8, 9]

# 12.【编程】统计句子 "the quick brown fox jumps over the lazy dog the fox"
#     中每个单词出现的次数（用字典），并输出出现次数最多的单词。
print("第12题（你的代码写在下面）：")
# 你的答案：
# ⏳ 已移至「重做练习3-数据结构.py」第 4 题
# 参考：
# s = "the quick brown fox jumps over the lazy dog the fox"
# count = {}
# for w in s.split():
#     count[w] = count.get(w, 0) + 1
# print(count)
# print(max(count, key=count.get))  # → the

# 13.【编程】用列表推导式（或循环）生成 1~20 中偶数的平方列表。
#     例：2²=4, 4²=16, ... → [4, 16, 36, ...]
print("第13题（你的代码写在下面）：")
# 你的答案：
event = []
for i in range(1,21):
    if i % 2 ==0:
        event.append(i**2)
print(event)

# 14.【综合编程】输入一段英文文本（示例：s = "hello world hello python world python python"），
#     统计每个单词出现次数，输出：
#     ① 出现了哪些不同的单词
#     ② 出现次数最多的单词及次数
#     提示：用 split() 切分 → 字典统计 → max() 找最大
print("第14题（你的代码写在下面）：")
# 你的答案：
# ⏳ 已移至「重做练习3-数据结构.py」第 5 题
# 参考：
# s = "hello world hello python world python python"
# count = {}
# for w in s.split():
#     count[w] = count.get(w, 0) + 1
# print("不同单词：", set(count.keys()))        # ①
# best = max(count, key=count.get)             # ②
# print("最多：", best, count[best])

# ============================================================
# 做完告诉我，我来批改！
# ============================================================
