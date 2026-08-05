# ============================================================
# 类的属性与方法 — 深入理解
# ============================================================

# ============================================================
# 一、实例属性 vs 类属性
# ============================================================
class Car:
    wheels = 4            # 类属性：所有对象共享（写在类里，不写 self.）
    def __init__(self, brand):
        self.brand = brand  # 实例属性：每个对象独有

c1 = Car("宝马")
c2 = Car("奔驰")

print(c1.brand)     # → 宝马（实例属性，各自不同）
print(c2.brand)     # → 奔驰
print(c1.wheels)    # → 4（类属性，共享）
print(c2.wheels)    # → 4
print(Car.wheels)   # → 4（类属性也能通过类访问）

# 修改类属性：所有对象一起变
Car.wheels = 6
print(c1.wheels, c2.wheels)   # → 6 6（一起变）


# ============================================================
# 二、方法类型：实例方法 / 类方法 / 静态方法（了解）
# ============================================================
class Tool:
    count = 0                       # 类属性

    def __init__(self, name):
        self.name = name
        Tool.count += 1             # 每建一个对象，计数+1

    def use(self):                  # 实例方法：操作对象（最常用）
        print(f"使用 {self.name}")

    @classmethod                    # 类方法：操作类本身
    def how_many(cls):
        print(f"共创建了 {cls.count} 个工具")

    @staticmethod                   # 静态方法：跟类关系不大，只是归类放
    def help():
        print("工具帮助信息")

t1 = Tool("锤子")
t2 = Tool("螺丝刀")
t1.use()            # → 使用 锤子
Tool.how_many()     # → 共创建了 2 个工具
Tool.help()         # → 工具帮助信息


# ============================================================
# 三、__str__ 方法 — 打印对象时显示什么
# ============================================================
# 不定义 __str__ 时，print(对象) 显示难看的内存地址
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

p = Point(3, 4)
print(p)        # → (3, 4)（好看！而不是 <__main__.Point object at 0x...>）


# ============================================================
# 四、属性保护约定（了解）
# ============================================================
# Python 没有真正的 private，靠命名约定：
#   self.name   → 公开（都能访问）
#   self._name  → 约定"内部使用"（下划线开头）
#   self.__name → 双下划线，触发名称改写（勉强算私有）

class Bank:
    def __init__(self, money):
        self._money = money     # 约定内部

    def get_money(self):        # 通过方法访问（"封装"）
        return self._money

b = Bank(1000)
print(b.get_money())    # → 1000（推荐方式）
print(b._money)         # → 1000（技术上还是能访问）


# ============================================================
# 五、实战：抽奖系统（类 + 随机）
# ============================================================
import random

class Lottery:
    def __init__(self, items):
        self.items = items

    def draw(self):
        return random.choice(self.items)

    def draw_many(self, n):
        return [self.draw() for _ in range(n)]

lotto = Lottery(["A", "B", "C", "D", "E"])
print(lotto.draw())            # 随机抽一个
print(lotto.draw_many(3))      # 随机抽 3 个
