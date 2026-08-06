# ============================================================
# 重做练习 2 — 循环逻辑错题册
# ============================================================
# 从「进阶练习-循环逻辑.py」中按"有一点不完美就算错"标准
# 筛出的 7 道错题。每题带思路提示（不给完整答案）。
# 先想清楚，再动手写，最后运行验证。做完找我批改。
# ============================================================


# 1. 求 1~100 之间所有质数的和。
# 上次的问题：else 挂错了位置、2 没有被加进去、合数被重复加
# 提示：用 for-else（else 对齐 for），且从 2 开始遍历
# 你的代码：
count = 0
for i in range(2,101):
    for j in range(2,int(i**0.5)+1):
        if i % j == 0:
            break
    else:
        count += i
print(count)

# 2. 统计字符串 "beautiful day, let's go python" 中元音字母
#    （a e i o u，不区分大小写）出现的【总次数】。
# 上次的问题：用了字典，输出的是每个字母的次数，不是总数
# 提示：只要求总数 → 一个计数器 count 就够了，遇到元音 +1
# 你的代码：
s = "beautiful day, let's go python"
count = 0
for ch in s:
    if ch in "AEIOUaeiou":
        count += 1
print(count)

# 3. 输入一个字符串，用循环把它反转并输出。
#    例：输入 "hello" → 输出 "olleh"
# 上次的问题：没思路，写了一半（range 里不能放字符串）
# 提示：倒着遍历（for i in range(len(s)-1, -1, -1)），
#      或者用"新字符往前插"技巧：rev = ch + rev
# 你的代码：
s = input("请输入一个字符串：")
rev = ""
for ch in range(len(s)-1,-1,-1):
    rev += s[ch]
print(rev)
#副本
#s = input("请输入一个字符串：")
#rev = ""
#for ch in s:
#    rev = ch + rev
#print(rev)

# 4. 判断回文数：输入一个整数，正着读和倒着读一样就是回文数。
#    例：12321 ✅，12345 ❌
# 上次的问题：空着没写
# 提示：str(num) 转字符串 → 用第 3 题的反转 → 比较 s == rev
# 你的代码：
s = input("请输入一个整数：")
rev = ""
for ch in s:
    rev = ch + rev
if s == rev:
    print("是回文数")
else:
    print("不是回文数")

# 5. 打印 5 行的数字金字塔：
#        1
#       121
#      12321
#     1234321
#    123454321
# 上次的问题：类型错误（字符串+数字）、没写出递增递减部分
# 提示：每行 = 空格 + 递增部分(1..i) + 递减部分(i-1..1)，
#      用 str(k) 拼接字符串
# 你的代码：
n = 5
for i in range(1,n+1):
    left = ""
    for ch in range(1,i+1):
        left += str(ch)
    right = ""
    for ch in range(i-1,0,-1):
        right += str(ch)
    print(" "*(n-i)+left+right)

# 6. 输入一个整数，把它各位数字倒过来输出（不转字符串，纯数学）。
#    例：输入 1234 → 输出 4321
# 上次的问题：写了一半
# 提示：rev = 0；每次 digit = num%10；rev = rev*10+digit；num//=10
# 你的代码：
num = int(input("请输入一个整数："))
rev = 0
while num > 0:
    digit = num % 10
    rev = rev * 10 + digit
    num //= 10
print(rev)
# 7. 完数（完全数）：一个数恰好等于它的所有真因子（不含自身）之和。
#     例：6 = 1+2+3，28 = 1+2+4+7+14。找出 1~1000 之间的所有完数。
# 上次的问题：因子和没在每次外层循环重置、判断条件写错（i==j）
# 提示：因子和 s 要放在外层 for 里面初始化；判断 s == i
# 你的代码：
for i in range(1,1001):
    s = 0
    for j in range(1,i):
        if i % j == 0:
            s += j
    if s == i:
        print(i)