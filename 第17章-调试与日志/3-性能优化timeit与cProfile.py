# ============================================================
# 调试与日志 ③ — 性能优化（timeit / cProfile）
# ============================================================
# 数据量一大，代码快慢差别巨大。
# 学会：怎么测时间、怎么找瓶颈、怎么写更快的代码。

import time
import timeit

# ============================================================
# 一、测时间的基本方法
# ============================================================
# 方法1：time.time() 包起来（简单）
start = time.time()
total = sum(range(1_000_000))
end = time.time()
print(f"耗时 {end - start:.4f} 秒")

# 方法2：time.perf_counter()（更精确，推荐）
start = time.perf_counter()
total = sum(range(1_000_000))
elapsed = time.perf_counter() - start
print(f"耗时 {elapsed * 1000:.2f} 毫秒")

# ============================================================
# 二、timeit：精确测多次取平均
# ============================================================
# 为什么需要 timeit？
#   单次测时间受系统波动影响大 → 多次取平均才准

# 测一段代码（字符串形式）
t = timeit.timeit("sum(range(1000))", number=10000)
print(f"10000次平均: {t/10000*1e6:.2f} 微秒/次")

# 对比两种写法哪个快
t_list = timeit.timeit("[x**2 for x in range(1000)]", number=1000)
t_gen = timeit.timeit("sum(x**2 for x in range(1000))", number=1000)
print(f"列表推导式: {t_list*1000:.2f} 毫秒/1000次")
print(f"生成器:     {t_gen*1000:.2f} 毫秒/1000次")

# 在 VS Code 里可以直接用魔法命令（Jupyter）
# %time 单次计时  %timeit 多次计时取平均

# ============================================================
# 三、找瓶颈：cProfile 性能剖析
# ============================================================
# 程序慢，先别猜哪里慢——用剖析器"测"出来
import cProfile
import pstats
import io

def slow_function():
    total = 0
    for i in range(10000):
        total += i ** 2
    return total

def medium_function():
    return [x * 2 for x in range(10000)]

def main():
    slow_function()
    medium_function()
    slow_function()

# 剖析 main() 的运行
profiler = cProfile.Profile()
profiler.enable()
main()
profiler.disable()

# 输出结果（按累计时间排序）
result = io.StringIO()
stats = pstats.Stats(profiler, stream=result)
stats.sort_stats("cumulative").print_stats(5)
print(result.getvalue())
# 会看到：哪个函数被调用几次、每次耗时多少
# 关注 cumtime（累计时间）最大的就是瓶颈

# ============================================================
# 四、写更快的代码（性能心法）
# ============================================================
# ① 用内置函数（C语言实现，比Python循环快）
# 慢：手动循环求和
# 快：sum()
nums = list(range(100000))
start = time.perf_counter()
s = sum(nums)              # 内置，快
print(f"sum(): {time.perf_counter()-start:.5f}s")

# ② 用推导式代替手动循环
# 慢：
# result = []
# for x in nums:
#     if x % 2 == 0:
#         result.append(x)
# 快：
# result = [x for x in nums if x % 2 == 0]

# ③ 用 numpy 向量化（数据处理主力，第19章）
# Python 循环处理百万级数据很慢，numpy 快百倍

# ④ 避免重复计算
# 慢：循环里每次都调用 len()
# 快：先算出长度存变量

# ⑤ 字符串拼接用 join 不用 +
# 慢：s = s + str(x)  （每次创建新字符串）
# 快："".join([...])

# ⑥ 字典/集合查找比列表快（in 操作）
# 在 100 万元素里判断存在：
#   列表 in：O(n) 慢
#   集合 in：O(1) 快
big_list = list(range(100000))
big_set = set(big_list)
start = time.perf_counter()
print(99999 in big_list)
print(f"列表查找: {time.perf_counter()-start:.5f}s")
start = time.perf_counter()
print(99999 in big_set)
print(f"集合查找: {time.perf_counter()-start:.5f}s")

# ============================================================
# 五、实战：优化一个数据处理函数
# ============================================================
# 原始（慢版）
def slow_process(data):
    result = []
    for d in data:
        if d > 0:
            result.append(d * 2)
    return result

# 优化版（推导式）
def fast_process(data):
    return [d * 2 for d in data if d > 0]

# 验证结果一样
data = list(range(-500, 500))
print(slow_process(data) == fast_process(data))   # → True

# 对比速度
t_slow = timeit.timeit("slow_process(data)", globals=globals(), number=100)
t_fast = timeit.timeit("fast_process(data)", globals=globals(), number=100)
print(f"慢版: {t_slow*1000:.2f}ms  快版: {t_fast*1000:.2f}ms  "
      f"快 {t_slow/t_fast:.1f} 倍")

# ============================================================
# 六、总结
# ============================================================
# 测时间：time.perf_counter() / timeit
# 找瓶颈：cProfile（别猜，去测）
# 优化招：内置函数 / 推导式 / numpy向量化 / 集合查找 / join拼接
# 心法：先让它跑对，再让它跑快（性能优化放最后）
