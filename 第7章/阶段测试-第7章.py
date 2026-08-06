# ============================================================
# 第七章 阶段测试 — 文件操作与异常处理
# ============================================================
# 共 12 题：简答、读代码、找 bug、编程题
# 注意：编程题先写代码，再在本地运行验证
# ============================================================


# ========== 一、文件模式 ==========

# 1.【简答】文件打开模式 "r" / "w" / "a" 各代表什么？
#     "w" 和 "a" 最大的区别是什么？文件不存在时分别会怎样？
# 你的答案：
'''
"r"代表只读，"w"代表写入，"a"代表追加
w与a的区别在于，w模式会删掉文件原有的内容再写，a模式则在原有内容之后追加内容
文件不存在时，w和a都会自动创建
'''

# 2.【简答】为什么读取中文文件通常要写 encoding="utf-8"？
#     不写会发生什么？
# 你的答案：
"""
utf-8是中文的编码方式，如果不强调编码方式，windows系统默认GBF，可能会出现乱码或报错
"""

# ========== 二、文件的读取 ==========

# 3.【读代码】同上假设，写出输出结果：
f = open("练习输出/test.txt", "r", encoding="utf-8")
print(f.readline())
print(f.readline())
print(f.read())
f.close()
# 你的答案：
# ⏳ 已移至「重做练习5-文件操作.py」第 1 题
# 参考：文件有"当前位置指针"，read() 读剩余内容
#   readline() → 第一行
#   readline() → 第二行
#   read()     → 第三行

# 4.【读代码】同上假设，写出输出结果：
f = open("练习输出/test.txt", "r", encoding="utf-8")
lines = f.readlines()
print(len(lines))
print(lines[0].strip())
f.close()
# 你的答案：
'''
3
第一行

'''

# ========== 三、with 语句 ==========

# 5.【简答】with open(...) as f: 相比手动 open()/close() 有什么好处？
#     就算中间代码出错，with 也会保证什么？
# 你的答案：
'''
相比手动open/close，with open() as f的好处是不用手动关闭文件
即使代码中间出错，with也会保证文件被关闭
'''

# ========== 四、os 模块 ==========

# 6.【简答】os.path.exists()、os.path.isfile()、os.path.isdir() 分别判断什么？
#     使用 os 模块前需要先做什么？
# 你的答案：
# ⏳ 已移至「重做练习5-文件操作.py」第 2 题
# 参考：
#   exists(path) → 路径存在吗（不管文件还是目录）
#   isfile(path) → 存在且是文件吗
#   isdir(path)  → 存在且是目录吗
#   使用前先 import os

# ========== 五、异常处理 ==========

# 7.【读代码】写出输出结果：
try:
    print(10 / 0)
except ZeroDivisionError:
    print("除零错误")
else:
    print("成功")
finally:
    print("结束")
# 你的答案：
'''
除零错误
结束
'''

# 8.【找 bug】下面的代码想往文件里写数字，但运行报错，为什么？怎么改？
# f = open("test.txt", "w", encoding="utf-8")
# f.write(123)
# f.close()
# 你的答案（指出错误 + 修正）：
'''
写入只接受字符串，123属于int，需用str转换类型，即：f.write(str(123))
'''

# ========== 六、编程题 ==========

# 9.【编程】把 1~20 的偶数写入文件 evens.txt，每行一个。
#     提示：with open + for 循环 + write
print("第9题（你的代码写在下面）：")
# 你的代码：
# ⏳ 已移至「重做练习5-文件操作.py」第 3 题
# 参考（注意"偶数"两个字！）：
# with open("evens.txt", "w", encoding="utf-8") as f:
#     for i in range(1, 21):
#         if i % 2 == 0:
#             f.write(str(i) + "\n")

# 10.【编程】读取第 9 题生成的 evens.txt，
#     统计一共有多少个数字，并求它们的和。
#     提示：for line in f → int(line.strip())
print("第10题（你的代码写在下面）：")
# 你的代码：
# ⏳ 已移至「重做练习5-文件操作.py」第 4 题
# 参考：
# total = 0
# count = 0
# with open("evens.txt", "r", encoding="utf-8") as f:   # encoding 别拼错！
#     for line in f:
#         count += 1
#         total += int(line.strip())
# print("个数：", count, "和：", total)

# 11.【编程】写一个函数 safe_divide(a, b)：
#     能正常返回 a/b；b 为 0 时用 try/except 捕获，返回 None 并提示"除数不能为 0"。
print("第11题（你的代码写在下面）：")
# 你的代码：
# ⏳ 已移至「重做练习5-文件操作.py」第 5 题
# 参考（except 单独一行 + 用 return）：
# def safe_divide(a, b):
#     try:
#         return a / b
#     except ZeroDivisionError:
#         print("除数不能为 0")
#         return None

# 12.【综合编程】写一个函数 count_words_in_file(文件名)：
#     读取文件，统计每个单词出现次数，返回字典。
#     提示：for line in f → line.split() 切单词 → 字典统计
print("第12题（你的代码写在下面）：")
# 你的代码：
# ⏳ 已移至「重做练习5-文件操作.py」第 6 题
# 参考（嵌套循环遍历单词 + 别忘了 return）：
# def count_words_in_file(filename):
#     count = {}
#     with open(filename, "r", encoding="utf-8") as f:
#         for line in f:
#             for w in line.split():
#                 count[w] = count.get(w, 0) + 1
#     return count


# ============================================================
# 做完告诉我，我来批改！
# ============================================================
