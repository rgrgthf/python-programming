# ============================================================
# 重做练习 4 — 函数错题册（第六章）
# ============================================================
# 重点攻克两个问题：
#   1. 循环版阶乘（上次用递归代替了循环）
#   2. 统计时看清"单词"还是"字符"（连续踩坑的老毛病！）
# ============================================================


# 1. 用【循环】写一个阶乘函数 factorial(n)，并打印 5! 和 10!。
# 提示：result = 1；for i in range(1, n+1): result *= i
# 你的代码：factorial(n)
def factorial(n):
    result = 1
    for i in range(1,n+1):
        result *= i
    return result
print(factorial(5))
print(factorial(10))

# 2. 写一个函数 word_count(text)，统计【单词】出现次数，
#    返回字典（单词→次数）。
#    然后用它统计 "the quick brown fox jumps over the lazy dog the fox"
#    并输出出现次数最多的单词及次数。
# 提示：text.split() 切单词 → count[w] = count.get(w, 0) + 1
# 你的代码：
def word_count(text):
    count = {}
    for w in text.split():
        count[w] = count.get(w,0) + 1
    return count
s = "the quick brown fox jumps over the lazy dog the fox"
c = word_count(s)
best = max(c,key=c.get)
print("最多：",best,"次数：",c[best])

# ============================================================
# 3.【读题训练】判断下面每道题该统计"单词"还是"字符"？
#    把答案写在注释里（不用写代码）
# ============================================================

# ① 统计一篇文章里 "the" 这个单词出现了几次
#    该用：split() 切单词  /  直接遍历字符？（圈一个）
# 你的答案：
#切单词，而且需要加条件if w == "the":

# ② 统计一段密码里数字字符（0-9）有几个
#    该用：split() 切单词  /  直接遍历字符？（圈一个）
# 你的答案：
#直接遍历字符，外加条件if ch.isdigit():

# ③ 统计一段英文里每个字母出现的次数
#    该用：split() 切单词  /  直接遍历字符？（圈一个）
# 你的答案：
#直接遍历字符，用ch.isalpha()

# ④ 统计一句话里每个单词的长度
#    该用：split() 切单词  /  直接遍历字符？（圈一个）
# 你的答案：
#用.split切单词
def word_len(text):
    count = {}
    for w in text.split():
        count[w] = len(w)
    return count
#我不知道是不是这样写
s = "the quick brown fox jumps over the lazy dog the fox"
print(word_len(s))

# ============================================================
# 4. 判断依据（看完再自己总结一遍）：
# ============================================================
# 「单词」为单位  → 先 split()，得到的是一个个 word
# 「字符」为单位  → 直接 for ch in 字符串，得到的是一个个字符
#
# 关键自问：我要的"最小单位"是词还是字母？
#   要"词" → split()
#   要"字母/符号" → 直接遍历
