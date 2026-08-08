# ============================================================
# Python 进阶 ① — 装饰器（Decorator）
# ============================================================
# 装饰器 = "在不修改原函数的情况下，给函数加功能"。
# 用途：日志、计时、权限检查、缓存——写框架和工具必备。
# 你其实已经用过装饰器：@classmethod、@staticmethod、@property

# ============================================================
# 一、先理解"函数也是对象"
# ============================================================
def greet(name):
    return f"你好，{name}"

# 函数可以赋值给变量
f = greet
print(f("小明"))        # → 你好，小明

# 函数可以作为参数传入
def run(func, arg):
    return func(arg)
print(run(greet, "小红"))   # → 你好，小红

# 函数可以返回函数
def outer():
    def inner():
        print("我是内部函数")
    return inner          # 返回函数本身（不加括号！）
fn = outer()
fn()                      # → 我是内部函数

# 这就是装饰器的基础：函数是一等公民

# ============================================================
# 二、最简单的装饰器
# ============================================================
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("== 函数执行前 ==")
        result = func(*args, **kwargs)
        print("== 函数执行后 ==")
        return result
    return wrapper

@my_decorator
def say_hello(name):
    return f"你好，{name}"

print(say_hello("小明"))
# 输出：
# == 函数执行前 ==
# == 函数执行后 ==
# 你好，小明

# @my_decorator 等价于：say_hello = my_decorator(say_hello)

# ============================================================
# 三、实用案例：计时器（科研常用！）
# ============================================================
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} 耗时 {end - start:.4f} 秒")
        return result
    return wrapper

@timer
def slow_calc():
    time.sleep(0.2)
    return 42

slow_calc()    # → slow_calc 耗时 0.2002 秒

# 案例：日志装饰器
def log(func):
    def wrapper(*args, **kwargs):
        print(f"调用 {func.__name__}，参数 {args}")
        return func(*args, **kwargs)
    return wrapper

@log
def add(a, b):
    return a + b
add(3, 5)    # → 调用 add，参数 (3, 5)

# ============================================================
# 四、带参数的装饰器
# ============================================================
# 有些装饰器本身要参数（如 @retry(3)）
def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def hello():
    print("你好！")

hello()    # 打印3次"你好！"

# ============================================================
# 五、装饰器实战：重试（网络/数据获取常用）
# ============================================================
def retry(max_attempts=3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"第{attempt}次失败：{e}")
                    if attempt == max_attempts:
                        raise
        return wrapper
    return decorator

@retry(max_attempts=3)
def unstable_network():
    import random
    if random.random() < 0.6:
        raise ConnectionError("网络错误")
    return "数据获取成功"

# print(unstable_network())   # 失败会自动重试最多3次

# ============================================================
# 六、@wraps — 保留原函数的元信息
# ============================================================
from functools import wraps

def my_deco(func):
    @wraps(func)          # 保留 func 的 __name__/__doc__
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_deco
def important():
    """重要函数"""
    pass

print(important.__name__)   # → important（没@wraps会变wrapper）
print(important.__doc__)    # → 重要函数

# 写装饰器时习惯加上 @wraps（规范）

# ============================================================
# 七、装饰器应用场景总结
# ============================================================
# 1. 计时/性能分析（@timer）
# 2. 日志记录（@log）
# 3. 权限/登录检查（Web框架常见）
# 4. 重试机制（@retry）
# 5. 缓存结果（@functools.lru_cache，内置！）

# ============================================================
# 八、易错点汇总
# ============================================================
# 1. @装饰器 的本质：say_hello = my_decorator(say_hello)
#    ——装饰器必须【返回一个函数】（wrapper），忘了 return wrapper 就崩
# 2. wrapper 必须用 *args, **kwargs 接住任意参数，
#    否则原函数带参数时调用就报错
# 3. wrapper 里【要 return 原函数的结果】，
#    忘了 return → 被装饰的函数永远返回 None
# 4. 带参数的装饰器 @retry(3) 需要【三层嵌套】：
#    repeat(n) → decorator(func) → wrapper(*args)
# 5. 写装饰器习惯加 @wraps，否则函数名和文档字符串会丢
# 6. 装饰器在【定义时】就执行（import 时），不是调用时——理解这个时机

# ============================================================
# 九、自测（40%基础 + 40%中等 + 20%挑战）
# ============================================================
# 【基础】
# 1. @my_decorator 等价于哪行代码？
# 2. 装饰器的 wrapper 为什么需要 *args, **kwargs？
# 3. 忘了在 wrapper 里 return 原函数结果，会发生什么？
#
# 【中等】
# 4. 写一个 timer 装饰器，统计函数耗时并打印。
# 5. 写一个 @log 装饰器：调用前打印函数名和参数。
# 6. 解释带参数装饰器 @repeat(3) 的三层嵌套结构。
#
# 【挑战】
# 7. 写一个 @retry(3) 装饰器：函数抛异常就重试，最多 3 次。
# 8. 为什么说装饰器在"定义时"执行？用 print 验证这个时机。
# 6. 参数校验
#
# 内置装饰器回顾：@classmethod @staticmethod @property
# functools.lru_cache：自动缓存函数结果（加速递归！）
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(50))    # → 12586269025（加了缓存瞬间算完）
# 没有缓存时 fib(50) 会卡死，这就是装饰器的威力！
