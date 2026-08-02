# ============================================================
# 重做练习 — 编程题（从阶段测试中拎出，独立再练）
# ============================================================
# 说明：这 6 道是从阶段测试中拎出、需要再练的编程题。
# 建议先用纸笔理清思路，再动手写代码，最后运行验证。
# 做完后找我批改，我会给出参考实现。
# ============================================================


# 1. 输出 1~200 之间所有能被 3 整除但不能被 5 整除的数，每行 10 个。
# 提示：用一个计数器，每输出一个就 +1，满 10 个就换行（print()）
# 你的代码：
count = 0
for i in range(1,201):
    if i % 3 == 0 and i % 5 != 0:
        print(i,end=" ")
        count += 1
        if count % 10 == 0:
            print()

# 2. 打印 5 行的菱形（上半 3 行 + 下半 2 行）：
#      *
#     ***
#    *****
#     ***
#      *
# 提示：每行 = 空格 + 星号，上半星号 1,3,5 递增，下半 3,1 递减
# 你的代码：
n = 3
for i in range(1,n+1):
    print(" "*(n-i)+"*"*(2*i-1))
for i in range(n-1,0,-1):
    print(" "*(n-i)+"*"*(2*i-1))

# 3. 用 for-else 找出 100~200 之间第一个质数，并输出它。
# 提示：判断质数只需试到 √n；找到后要 break 结束外层循环
# 你的代码：
for i in range(100,201):
    for j in range(2,int(i**0.5)+1):
        if i % j == 0:
            break
    else:
        print("第一个质数是：",i)
        break
    

# 4. 猜数字游戏升级版：程序随机生成 1~100 的数，
#    用户每次猜完给出"大了/小了"提示，并统计猜测次数；
#    如果超过 7 次还没猜中，输出"次数用尽"并结束。
# 提示：循环条件要包含"次数 < 7"，猜中与否用 if-else 分流
# 你的代码：
import random
target = random.randint(1,100)
guess = 0
count = 0
while guess != target and count < 7:
    guess = int(input("请输入一个数字(1~100):"))
    count +=1
    if guess > target:
        print("大了")
    if guess < target:
        print("小了")
if guess == target:
    print("您猜中了！用了",count,"次")
else:
    print("次数用尽")

# 5. 统计字符串 "hello python, hello world" 中每个字符出现的次数，
#    只统计字母（忽略空格和逗号），用字典存结果，最后输出。
# 提示：字典 key 是字符，value 是次数；遇到新字符先初始化成 1
# 你的代码：
s = "hello python, hello world"
count = {}
for i in s:
    if i.isalpha():
        if i in count:
            count[i] += 1
        else:
            count[i] = 1
print(count)


# 6. 斐波那契数列：前两个数是 0、1，之后每个数是前两个数之和。
#    输出前 20 个斐波那契数，每行 5 个。
#    提示：0 1 1 2 3 5 8 13 ...，用 a, b = b, a + b 递推
# 你的代码：
a,b = 0,1
count = 0
while True:
    print(a,end=" ")
    a,b = b,a+b
    count += 1
    if count % 5 == 0:
        print()
    if count == 20:
        break