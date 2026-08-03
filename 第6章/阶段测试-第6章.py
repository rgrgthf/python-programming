# ============================================================
# 第六章 阶段测试 — 函数
# ============================================================
# 共 15 题：读代码、简答、找 bug、编程题
# ============================================================


# ========== 一、函数的定义与调用 ==========

# 1.【读代码】写出输出结果：
print("第1题：")
def greet(name):
    return "你好，" + name

print(greet("小明"))
print(greet("小红"))
# 你的答案：
"""
第1题：
你好，小明
你好，小红

"""

# 2.【读代码】写出输出结果（默认参数）：
print("第2题：")
def f(a, b=10, c=20):
    return a + b + c

print(f(1))
print(f(1, 2))
print(f(1, 2, 3))
print(f(1, c=5))
# 你的答案：
"""
第2题：
31
23
6
16

"""

# 3.【读代码】写出输出结果（*args）：
print("第3题：")
def func(*nums):
    return sum(nums)

print(func(1, 2, 3))
print(func())
print(func(5))
# 你的答案：
'''
第3题：
6
0
5

'''

# ========== 二、返回值 ==========

# 4.【简答】下面两个函数有什么本质区别？
# def f1(x):
#     return x * 2
# def f2(x):
#     print(x * 2)
# 你的答案：
"""
def1有return，返回值是x**2，def2没有return，返回值是None
"""

# ========== 三、作用域 ==========

# 5.【读代码】写出输出结果：
print("第5题：")
x = 10
def f():
    x = 20
    print(x)
f()
print(x)
# 你的答案：
'''
第5题：
20
10

'''

# 6.【读代码】写出输出结果（global）：
print("第6题：")
x = 10
def f():
    global x
    x = 20
f()
print(x)
# 你的答案：
'''
第6题：
20
20

'''

# 7.【简答】为什么函数里对列表调用 append() 会改变外面的列表？
#     有什么办法避免？
# 你的答案：
'''
因为列表是可变类型，避免办法是传副本[:]
'''

# ========== 四、lambda 和 sorted ==========

# 8.【读代码】写出输出结果：
print("第8题：")
words = ["bb", "a", "ccc", "dddd"]
print(sorted(words, key=len))
print(sorted(words, key=lambda w: len(w), reverse=True))
# 你的答案：
'''
第8题：
[a,bb,ccc,dddd]
[dddd,ccc,bb,a]
'''

# ========== 五、递归 ==========

# 9.【读代码】写出输出结果：
print("第9题：")
def f(n):
    if n <= 1:
        return 1
    return n * f(n - 1)
print(f(4))
# 你的答案：
'''
第9题：
24

'''

# 10.【简答】递归必须满足哪两个条件？缺了会怎样？
# 你的答案：
"""
需要满足基线条件，缺了会导致无限递归，最终栈溢出
还要递归条件，把问题变小
"""

# ========== 六、找 bug ==========

# 11.【找 bug】下面函数想统计字符次数并返回结果，但调用后得到 None，为什么？怎么改？
# def count_chars(s):
#     count = {}
#     for ch in s:
#         count[ch] = count.get(ch, 0) + 1
#     print(count)          # ← ?
# result = count_chars("hello")
# print(result)             # → None
# 你的答案（指出错误 + 修正）：
'''
def count_chars(s)中没有return，返回值默认为None，所以输出结果为None，改正建议是把函数中
print(count)改为return count
'''

# ========== 七、编程题 ==========

# 12.【编程】写一个函数 is_even(n)，判断 n 是否为偶数，返回 True/False。
#     然后用它输出 1~20 中的所有偶数。
print("第12题（你的代码写在下面）：")
# 你的代码：
def is_even(n):
    if n % 2 == 0:
        return True
    return False
for i in range(1,21):
    if is_even(i):
        print(i)

# 13.【编程】写一个函数 factorial(n)，用【循环】求 n!。
#     然后打印 5! 和 10!。
print("第13题（你的代码写在下面）：")
# 你的代码：
# ⏳ 已移至「重做练习4-函数.py」第 1 题
# 参考（循环版）：
# def factorial(n):
#     result = 1
#     for i in range(1, n + 1):
#         result *= i
#     return result
# print(factorial(5))   # → 120
# print(factorial(10))  # → 3628800

# 14.【编程】写一个递归函数 fib(n)，返回斐波那契数列第 n 项。
#     （f(0)=0, f(1)=1, f(n)=f(n-1)+f(n-2)）
#     然后打印 fib(10)。
print("第14题（你的代码写在下面）：")
# 你的代码：
def fib(n):
    if n <= 1:
        return n
    return fib(n-1)+fib(n-2)
print(fib(10))

# 15.【综合编程】写一个函数 word_count(text)，
#     参数是英文文本字符串，返回一个字典（单词→次数）。
#     再用这个函数统计 "the quick brown fox jumps over the lazy dog the fox"
#     并输出出现次数最多的单词及次数。
print("第15题（你的代码写在下面）：")
# 你的代码：
# ⏳ 已移至「重做练习4-函数.py」第 2 题
# 参考（注意：统计【单词】，先 split()！）：
# def word_count(text):
#     count = {}
#     for w in text.split():
#         count[w] = count.get(w, 0) + 1
#     return count
# s = "the quick brown fox jumps over the lazy dog the fox"
# c = word_count(s)
# best = max(c, key=c.get)
# print("最多的单词：", best, "次数：", c[best])  # → the 3

# ============================================================
# 做完告诉我，我来批改！
# ============================================================
