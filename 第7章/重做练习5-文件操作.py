# ============================================================
# 重做练习 5 — 文件操作错题册（第七章）
# ============================================================
# 从「阶段测试-第7章.py」中筛出的 6 道错题。
# 每题带提示（不给完整答案）。写完一定【运行验证】再交！
# 上次教训：编码拼写错、except 语法错，跑一遍就能发现。
# ============================================================


# 1. 文件指针理解：假设 test.txt 内容为三行
#     第一行
#     第二行
#     第三行
# 写出输出：
f = open("test.txt", "r", encoding="utf-8")
print(f.readline())
print(f.readline())
print(f.read())
f.close()
# 提示：read() 读的是"当前位置往后的剩余内容"，不是从头读！
# 你的答案：
'''
第一行
第二行
第三行
'''

# 2. 写出 os 三个判断方法的区别（各一句话）：
#   os.path.exists(path)  →
#   os.path.isfile(path)  →
#   os.path.isdir(path)   →
# 提示：exists 只看"在不在"；isfile/isdir 还看"是什么"
# 你的答案：
'''
os.path.exists(path)看文件是否存在
os.path.isfile(path)看是不是文件
os.path.isdir(path)看是不是目录
'''

# 3. 把 1~20 的【偶数】写入文件 evens.txt，每行一个。
# 上次的问题：忘了加偶数过滤，把所有数都写进去了
# 提示：if i % 2 == 0
# 你的代码：
with open("evens.txt","w",encoding="utf-8") as f:
    for i in range(1,21):
        if i % 2 == 0:
            f.write(str(i) + "\n")


# 4. 读取 evens.txt，统计数字个数并求和。
# 上次的问题：encoding 拼写成 encodong，程序直接报错
# 提示：写完先自查拼写，再运行；sum 别当变量名（会覆盖内置函数）
# 你的代码：
with open("evens.txt","r",encoding="utf-8") as f:
    count = 0
    total = 0
    for line in f:
        count += 1
        total += int(line.strip())
    print("数字个数：",count)
    print("和：",total)


# 5. 写 safe_divide(a, b)：成功返回 a/b；b 为 0 时捕获异常，
#    提示"除数不能为 0"，返回 None。
# 上次的问题：except 语法错误、用 print 代替 return
# 提示：except ZeroDivisionError: 要单独一行；用 return
# 你的代码：
def safe_divide(a,b):
    try:
        return a / b
    except ZeroDivisionError:
        print("除数不能为0")
        return None
a = int(input("请输入被除数："))
b = int(input("请输入除数："))
print(safe_divide(a,b))

# 6. 写 count_words_in_file(filename)：读取文件，统计每个单词
#    出现次数，返回字典。
# 上次的问题：把整个 line.split() 当键（列表不能当键！）、忘了 return
# 提示：for line in f → for w in line.split() → count[w] = count.get(w,0)+1
# 你的代码：
def count_words_in_file(filename):
    count = {}
    with open(filename,"r",encoding="utf-8")as f:
        for line in f:
            for w in line.split():
                count[w] = count.get(w, 0) + 1
    return count
print(count_words_in_file("sample.txt"))

# ============================================================
# 提交前自查清单（改掉"猴急"的毛病）：
#   ① 单词拼写对不对（encoding 不是 encodong）
#   ② 语法对不对（except 后面要换行，不能跟冒号）
#   ③ 运行一遍，看输出是否符合预期
#   ④ 题目要求有没有漏（比如"偶数"两个字）
# ============================================================
