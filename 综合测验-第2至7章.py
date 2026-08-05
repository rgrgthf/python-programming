# ============================================================
# 综合测验 — 第2至7章（全部内容大混合）
# ============================================================
# 共 16 题：覆盖基础语法、运算符、数据结构、函数、文件、异常
# 综合题的最大特点：一道题可能要用到多个章节的知识
# ============================================================


# ========== 一、第2、3章：基础与运算符 ==========

# 1.【读代码】写出输出结果：
print("第1题：")
print("A", "B", sep="-", end="!")
print(True + 1, bool(" "), 0.1 + 0.2 == 0.3)
# 你的答案：
'''
第1题：
A-B！2 True False

'''

# 2.【读代码】写出输出结果（优先级 + 短路）：
print("第2题：")
print(2 ** 3 ** 2)
print(10 // 3 * 2 + 10 % 3)
print(3 < 5 != 4)
print(not 3 > 2 and 5 > 4 or 6 > 5)
# 你的答案：
'''
第2题：
512
7
True
True

'''

# ========== 二、第5章：数据结构 ==========

# 3.【读代码】写出输出结果（列表）：
print("第3题：")
lst = [3, 1, 2, 3]
lst.append(4)
lst.remove(3)
lst.sort(reverse=True)
print(lst)
# 你的答案：
'''
第3题：
[4,3,2,1]

'''

# 4.【读代码】写出输出结果（切片 + 元组）：
print("第4题：")
nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(nums[1:7:2])
print(nums[::-1][:4])
t = (5)
print(type(t))
# 你的答案：
'''
[1,3,5]
[9,8,7,6]
int

'''

# 5.【读代码】写出输出结果（字典 + 集合）：
print("第5题：")
d = {"a": 1, "b": 2}
d["c"] = 3
print(d.get("x", 0), d.get("b"))
A = {1, 2, 3}
B = {2, 3, 4}
print(A & B, A | B, A - B)
# 你的答案：
'''
第5题：
0 2
{2，3} {1，2，3，4} {1}

'''

# ========== 三、第6章：函数 ==========

# 6.【读代码】写出输出结果（默认参数 + *args）：
print("第6题：")
def f(a, b=2, *rest):
    return a + b + sum(rest)
print(f(1))
print(f(1, 2, 3, 4))
# 你的答案：
# ⏳ 已移至「重做练习6-综合补漏.py」第 1 题
# 参考：f(1) → a=1, b=2, rest=()    → 1+2+0 = 3
#      f(1,2,3,4) → a=1, b=2, rest=(3,4) → 1+2+7 = 10

# 7.【读代码】写出输出结果（作用域）：
print("第7题：")
x = 5
def change():
    global x
    x = 10
change()
print(x)
# 你的答案：
'''
第7题：
10

'''

# 8.【读代码】写出输出结果（lambda + sorted）：
print("第8题：")
data = [("b", 2), ("a", 3), ("c", 1)]
print(sorted(data, key=lambda t: t[1]))
# 你的答案：
'''
第8题：
[("c", 1),("b", 2),("a", 3)]
'''

# 9.【读代码】写出输出结果（递归）：
print("第9题：")
def f(n):
    if n < 2:
        return n
    return f(n - 1) + f(n - 2)
print(f(6))
# 你的答案：
'''
8

'''

# ========== 四、第7章：文件与异常 ==========

# 10.【读代码】写出输出结果：
print("第10题：")
try:
    n = int("abc")
except ValueError:
    print("值错误")
except Exception as e:
    print("其他错误", e)
else:
    print("成功")
finally:
    print("结束")
# 你的答案：
'''
第10题：
值错误
结束

'''

# 11.【简答】with open("f.txt", "w") 和 with open("f.txt", "a")
#     打开已存在的文件时，行为有什么不同？
# 你的答案：
'''
w模式的行为是清空文件内容再进行写入，a模式则是在原有内容之下进行追加，不会清空原有内容
'''

# ========== 五、综合编程题 ==========

# 12.【编程】写一个函数 is_prime(n) 判断质数，
#     用列表推导式找出 1~50 的所有质数并打印。
# 提示：质数判断试到 √n；推导式带 if 过滤
print("第12题（你的代码写在下面）：")
# 你的代码：
# ⏳ 已移至「重做练习6-综合补漏.py」第 2 题
# 参考（注意 return False 在循环里，return True 在循环外）：
# def is_prime(n):
#     if n < 2:
#         return False
#     for i in range(2, int(n**0.5) + 1):
#         if n % i == 0:
#             return False
#     return True
# primes = [n for n in range(1, 51) if is_prime(n)]
# print(primes)

# 13.【编程】给定列表 [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]：
#     ① 去重并升序输出
#     ② 统计每个数字出现次数（字典）
#     ③ 找出出现次数最多的数字及次数
# 提示：set 去重 / 字典统计 / max(count, key=count.get)
print("第13题（你的代码写在下面）：")
# 你的代码：
lst = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
print(sorted(set(lst)))
count = {}
for i in lst:
    count[i] = count.get(i,0) + 1
best = max(count,key=count.get)
print(count)
print("出现次数最多：",best,"次数：",count[best])

# 14.【编程】写一个函数 count_words(text)，统计单词出现次数返回字典。
#     然后从文件读取一段文本（自己先建一个 text.txt），调用该函数，
#     把统计结果写入 result.txt（每行：单词 次数）。
# 提示：read → split → 字典 → 写入文件（要处理 encoding）
print("第14题（你的代码写在下面）：")
# 你的代码：
def count_word(text):
    with open(text,"r",encoding="utf-8") as f:
        with open("result.txt","w",encoding="utf-8") as j:
            count = {}
            for line in f:
                for w in line.split():
                    count[w] = count.get(w,0) + 1
            for k,v in count.items():
                j.write(f"{k,v}\n")
            return count
count_word("sample.txt")


# 15.【编程】斐波那契数列，但要求：
#     用函数 fib(n) 生成前 n 个斐波那契数（返回列表），
#     再把这串数写入文件 fib.txt（空格分隔，一行）。
# 提示：列表生成 + 文件写入
print("第15题（你的代码写在下面）：")
# 你的代码：
# ⏳ 已移至「重做练习6-综合补漏.py」第 3 题（含分步引导）
# 参考：
# def fib(n):
#     fibs = []
#     a, b = 0, 1
#     for _ in range(n):
#         fibs.append(a)
#         a, b = b, a + b
#     return fibs
# nums = fib(20)
# with open("fib.txt", "w", encoding="utf-8") as f:
#     for x in nums:
#         f.write(str(x) + " ")

            

# 16.【综合大挑战】写一个函数 analyze_text(filename)：
#     读取一个文本文件，返回一个字典，包含：
#       "words": 总单词数
#       "unique": 不同单词数
#       "longest": 最长的单词
#       "top": 出现最多的单词（及次数）
#     提示：全部用已学知识（文件/字符串/字典/max key）
print("第16题（你的代码写在下面）：")
# 你的代码：
def analyze_text(filename):
    count = {}
    words = 0
    with open(filename,"r",encoding="utf-8") as f:
        for line in f:
            for w in line.split():
                count[w] = count.get(w,0) + 1
                words += 1
    best = max(count,key=count.get)
    print("words:",words)
    print("unique:",len(count))
    print("longest:",max(count,key=len))
    print("top:",best)
analyze_text("sample.txt")

# ============================================================
# 做完告诉我，我来批改！
# ============================================================
