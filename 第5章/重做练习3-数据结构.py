# ============================================================
# 重做练习 3 — 数据结构错题册（第五章）
# ============================================================
# 从「阶段测试-第五章.py」中筛出的错题 + 薄弱点。
# 每题带提示（不给完整答案）。先想清楚，再动手，最后运行验证。
# ============================================================


# 1. 追踪下面的代码，写出最终输出：
lst = [1, 2, 3]
lst.append(4)
lst.insert(0, 0)
lst.pop()
lst[1] = 100
print(lst)
# 提示：一步一步画出来，每一步都别跳
# 你的答案：
'''
第1题：
[0,100,2,3]
'''

# 2. 下面代码想打印排序后的列表，但输出是 None，为什么？怎么改？
lst = [3, 1, 2]
print(lst.sort())
# 提示：sort() 是原地排序，它的返回值是什么？
# 你的答案：
"""
sort()是原地排序，返回值是None，应该改为先lst.sort(),再打印。或者print(sorted(lst))
"""

# 3. 给一个列表 [5, 3, 8, 3, 1, 8, 5, 9]，去重后按升序输出。
# 上次的问题：list(set(lst)) 没赋值、print(lst.sort()) 输出 None
# 提示：set(lst) 去重后要赋值给变量；或者用 sorted(set(lst)) 一步到位
# 你的代码：
lst = [5, 3, 8, 3, 1, 8, 5, 9]
print(sorted(set(lst)))

# 4. 统计句子 "the quick brown fox jumps over the lazy dog the fox"
#    中每个【单词】出现的次数（用字典），并输出出现次数最多的单词。
# 上次的问题：忘了 split() 切单词、字典用了 () 而不是 []、isalpha 少括号
# 提示：for w in s.split() → count[w] = count.get(w, 0) + 1
#      找最多单词用：max(count, key=count.get)
# 你的代码：
s = "the quick brown fox jumps over the lazy dog the fox"
count = {}
for w in s.split():
    count[w] = count.get(w,0) + 1
print(max(count,key=count.get))

# 5. 输入一段英文文本，统计每个单词出现次数，输出：
#    ① 有哪些不同的单词（用 set 去重）
#    ② 出现次数最多的单词及次数
# 上次的问题：split("") 空分隔符报错、values() 拼写错误
# 提示：split() 不加参数按空格切；values() 别写成 value()
# 你的代码：
s = "the quick brown fox jumps over the lazy dog the fox"
count = {}
event = s.split()
for w in event:
    count[w] = count.get(w,0) + 1
print("不同的单词有：",sorted(set(event)))
print("出现次数最多的单词是：",max(count,key=count.get))
# ✏️ 改进版：输出单词的同时也输出次数
# best = max(count, key=count.get)   # 先存下"出现最多的单词"
# print("出现最多的单词：", best, "，次数：", count[best])  # count[best] 查它的次数
# 说明：max(count, key=count.get) 返回的是【键】（单词），
#       次数要再用 count[best] 从字典里取出来

# ========== 补充：上次"部分对"的两个小点 ==========

# 6. d.get("x") 不写默认值时，返回什么？（写出代码验证）
# 你的答案：
d = {"a":1}
print(d.get("x"))   # ← 键是字符串必须加引号！（b 没定义会 NameError）
# → None（不写默认值时返回 None）

# 7. 除了字符串和元组，还有哪些类型可以当字典的键？为什么？
# 提示：想想"不可变类型"还有谁
# 你的答案：
#还有数字，int和float也属于不可变类型