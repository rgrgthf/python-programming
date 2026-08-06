# ============================================================
# 重做练习 6 — 综合测验补漏册（第 6、12、15 题）
# ============================================================
# 三题各配详细引导，尤其斐波那契会分步走。
# 做完运行验证再交！
# ============================================================


# 1. 追踪 *args：写出输出，并解释 f(1, 2, 3, 4) 每一步怎么算的
def f(a, b=2, *rest):
    return a + b + sum(rest)

print(f(1))
print(f(1, 2, 3, 4))
# 提示：
#   f(1)       → a=1, b=2, rest=()        → 1+2+0
#   f(1,2,3,4) → a=1, b=2, rest=(3,4)     → 1+2+(3+4)
# 你的答案（写出每个参数的值和最终结果）：
'''
3
10

'''

# 2. 修正 is_prime：判断质数的正确逻辑
# 上次的问题：在第一个"不能整除"时就返回 True，逻辑反了
# 提示：要"全部试完都没有因子"才算质数
#   for i in range(2, int(n**0.5)+1):
#       if n % i == 0:     # 找到因子 → 不是质数
#           return False
#   return True            # 全部试完 → 才是质数
# 完成后用 is_prime(9) 和 is_prime(7) 验证（应返回 False 和 True）
# 你的代码：
def is_prime(n):
    if n <= 2:
        return False
    for i in range(2,int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
print(is_prime(9),is_prime(7))

# 3. 斐波那契：用函数 fib(n) 生成前 n 个数（返回列表），写入 fib.txt
#
# 【分步引导】别急着写整题，先一步步来：
#
# 第①步：先用循环打印前 5 个斐波那契数（用 a, b = b, a + b）
#   a, b = 0, 1
#   for _ in range(5):
#       print(a)          # 存的是 a
#       a, b = b, a + b   # 滚动
#   预期输出：0 1 1 2 3
#
# 第②步：把"打印"改成"存进列表"（+1 行）
#   fibs = []             # 新建空列表
#   fibs.append(a)        # 把 a 存进去
#   返回 fibs
#
# 第③步：把列表写入文件（用 with + for 循环）
#   with open("fib.txt", "w", encoding="utf-8") as f:
#       for x in fibs:
#           f.write(str(x) + " ")    # 空格分隔
#
# 三步都通了，把最终完整代码写在这里：
# 你的代码：
def fib(n):
    fibs = []
    a,b = 0,1
    for _ in range(n):
        fibs.append(a)
        a,b = b,a+b
    return fibs
fib(50)
with open("fib.txt","w",encoding="utf-8") as f:
    for i in fib(50):
        f.write(str(i)+" ")
# ============================================================
# 提交前自查：
#   ① 每题都运行过了吗？
#   ② is_prime(9) 是不是 False？is_prime(7) 是不是 True？
#   ③ fib.txt 里是不是 0 1 1 2 3 5 8 ... ？
# ============================================================
