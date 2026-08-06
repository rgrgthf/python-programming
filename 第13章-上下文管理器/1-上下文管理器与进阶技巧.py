# ============================================================
# Python 进阶 ③ — 上下文管理器与进阶技巧
# ============================================================
# 上下文管理器 = with 语句背后的机制。
# 你已经天天用 with open()：这一节搞懂它为什么"自动关闭"。

# ============================================================
# 一、with 的工作原理
# ============================================================
# with 语句其实是在调用两个"魔法方法"：
#   __enter__()：进入 with 时执行（返回 as 后面的变量）
#   __exit__()：离开 with 时执行（无论正常还是异常都执行！）
#
# 这就是为什么 with 能保证文件一定被关闭。

# ============================================================
# 二、自己写上下文管理器（类方式）
# ============================================================
class Timer:
    """用 with 计时的上下文管理器"""
    def __enter__(self):
        import time
        self.start = time.time()
        return self          # as t 拿到的就是这里返回的

    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        print(f"耗时 {time.time() - self.start:.4f} 秒")
        # 返回 False = 不吞掉异常；返回 True = 异常被"吃掉"
        return False

with Timer() as t:
    total = 0
    for i in range(1000000):
        total += i
# → 耗时 0.1x 秒

# ============================================================
# 三、contextlib 快捷写法
# ============================================================
from contextlib import contextmanager

@contextmanager
def timer():
    import time
    start = time.time()
    try:
        yield               # with 块内的代码在这里执行
    finally:
        print(f"耗时 {time.time() - start:.4f} 秒")

with timer():
    sum(range(1000000))
# → 耗时 0.0x 秒
# @contextmanager + yield 是写上下文管理器的最简方式

# ============================================================
# 四、内置的上下文管理器
# ============================================================
# 1. with open() — 文件（最常用）
# 2. with ThreadPoolExecutor() — 线程池
# 3. 临时文件/目录
import tempfile
with tempfile.TemporaryDirectory() as tmpdir:
    print("临时目录：", tmpdir)   # 用完自动删除

# ============================================================
# 五、进阶技巧：异常处理的完整姿势
# ============================================================
# ① 多个 except 从具体到通用
try:
    num = int(input("数字："))
    result = 10 / num
except (ValueError, ZeroDivisionError):   # 可以合并
    print("输入无效或除零")
except Exception as e:                    # 兜底
    print(f"未知错误：{e}")

# ② raise 手动抛出异常
def check_positive(n):
    if n <= 0:
        raise ValueError("必须是正数")     # 主动报错
    return n
# check_positive(-5)   # → ValueError: 必须是正数

# ③ 自定义异常类（进阶）
class DataError(Exception):
    """自定义的数据错误"""
    pass

# raise DataError("数据格式错误")

# ============================================================
# 六、Python 进阶实用技巧合集
# ============================================================
# ① 多变量交换/解包（早已会用）
a, b = b, a

# ② * 解包
lst = [1, 2, 3]
print(*lst)            # → 1 2 3（拆开传入 print）

def f(a, b, c):
    return a + b + c
print(f(*lst))         # → 6（列表解包成参数）

# ③ 字典解包
d = {"a": 1, "b": 2}
print(f(**d))          # → 3

# ④ 默认值技巧
# x = result if result is not None else 0
# 等价于：x = result or 0

# ⑤ 链式比较
x = 5
print(1 < x < 10)      # → True

# ⑥ enumerate 带起始值
for i, ch in enumerate("abc", start=1):
    print(i, ch)       # 1 a / 2 b / 3 c

# ⑦ zip 处理多列表
names = ["a", "b"]
ages = [1, 2]
for n, a in zip(names, ages):
    print(n, a)

# ⑧ 列表转字符串
print("".join(["h", "i"]))        # → hi
print(", ".join(["1", "2", "3"])) # → 1, 2, 3

# ============================================================
# 七、性能与风格建议（老师建议）
# ============================================================
# 1. 用 with 管理资源（文件/连接），别手动 close
# 2. 大循环里避免不必要的重复计算
# 3. 用生成器处理大数据
# 4. 函数单一职责：一个函数只干一件事
# 5. 变量命名清晰 > 注释啰嗦
# 6. 写代码前先想清楚数据结构（列表/字典/集合怎么选）
# 7. 学会读 traceback：先看最后一行
