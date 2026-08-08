# ============================================================
# 📘 第8章·第2节：类的属性与方法 — 深入理解
# ============================================================
# 上一节学了怎么定义一个类。这一节深入两类东西：
#   · 属性：对象/类身上存的数据（名词）
#   · 方法：对象/类能做的操作（动词）
# 学完你要能回答：
#   1. 实例属性和类属性有什么区别？各自什么时候用？
#   2. 实例方法/类方法/静态方法，三种方法分别什么时候用？
#   3. __str__、__repr__ 这种"魔法方法"是干嘛的？
#   4. Python 的"私有属性"到底是怎么回事？

# ============================================================
# 一、实例属性 vs 类属性 —— 每个对象独有 vs 所有对象共享
# ============================================================
class Car:
    wheels = 4            # 【类属性】写在类体里、不写 self. → 所有对象共享
    def __init__(self, brand):
        self.brand = brand  # 【实例属性】写在 self. 后面 → 每个对象独有

c1 = Car("宝马")
c2 = Car("奔驰")

print(c1.brand)     # → 宝马（实例属性，各自不同）
print(c2.brand)     # → 奔驰
print(c1.wheels)    # → 4（类属性，共享）
print(c2.wheels)    # → 4
print(Car.wheels)   # → 4（类属性也能通过类名访问）

# 修改类属性：所有对象一起变
Car.wheels = 6
print(c1.wheels, c2.wheels)   # → 6 6（一起变）

# ---------- 深入理解：属性的"查找顺序" ----------
# 当你写 c1.wheels 时，Python 的查找顺序是：
#   ① 先找 c1 这个【对象自己】身上有没有 wheels（实例属性）
#   ② 没有 → 再去【类 Car】身上找 wheels（类属性）
# 这就是为什么类属性对所有对象"共享"：因为它们其实都存在类身上，
# 对象只是"查得到"而已。
#
# ⚠️ 一个经典陷阱（务必记住）：
#   通过对象给属性赋值（c1.wheels = 8）不会改类属性！
#   它会在 c1 自己身上【新建一个实例属性】，把类属性"盖住"：
#   c1.wheels = 8   → c1 从此用自己的 8（实例属性）
#   c2.wheels       → 还是 4（类属性没被动过）
#   想改类属性，必须用类名：Car.wheels = 8

# ---------- 什么时候用哪个？（药学场景）----------
# · 实例属性：每个对象都不同 → 药名、价格、剂量
# · 类属性：所有对象一样 / 用来统计 → 单位换算常数、创建计数
class Drug:
    VAT_RATE = 0.13          # 类属性：所有药共享的税率
    count = 0                # 类属性：统计创建了几个药

    def __init__(self, name, price):
        self.name = name     # 实例属性
        self.price = price
        Drug.count += 1      # 每造一个药，计数+1

    def final_price(self):
        return self.price * (1 + Drug.VAT_RATE)   # 用类属性算含税价

d1 = Drug("氯雷他定", 20)
d2 = Drug("阿莫西林", 15)
print(d1.final_price())   # → 22.6
print(Drug.count)         # → 2（统计功能，类属性的经典用法）

# ============================================================
# 二、方法类型：实例方法 / 类方法 / 静态方法
# ============================================================
class Tool:
    count = 0                       # 类属性

    def __init__(self, name):
        self.name = name
        Tool.count += 1             # 每建一个对象，计数+1

    # ① 实例方法（最常用）：第一个参数 self，能访问【对象】的一切
    def use(self):
        print(f"使用 {self.name}")

    # ② 类方法：装饰器 @classmethod，第一个参数 cls（类本身）
    @classmethod
    def how_many(cls):
        print(f"共创建了 {cls.count} 个工具")   # 通过 cls 访问类属性

    # ③ 静态方法：装饰器 @staticmethod，没有 self 也没有 cls
    @staticmethod
    def help():
        print("工具帮助信息")   # 不碰任何对象/类的数据

t1 = Tool("锤子")
t2 = Tool("螺丝刀")
t1.use()            # → 使用 锤子（实例方法：通过对象调）
Tool.how_many()     # → 共创建了 2 个工具（类方法：通过类调）
Tool.help()         # → 工具帮助信息（静态方法：通过类调）

# ---------- 三种方法怎么选？（记忆法）----------
# · 需要访问【对象的数据】(self.xxx)        → 实例方法
# · 需要访问【类的东西】(cls.xxx) 但不需对象 → 类方法
# · 跟这个类只是"顺便归类"，不碰任何数据      → 静态方法
#
# 用 cls 而不是类名的好处：子类继承时，cls 会自动指向子类（下一节讲），
# 代码更灵活。这也是为什么写 @classmethod 时用 cls.count 而非 Tool.count。
#
# 实例方法 vs 类方法也能互相转换调用：
#   Tool.how_many()  等价于  t1.how_many()   （都能调，但语义上类方法
#   一般用类名调更清晰）


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
# 三、魔法方法：__str__ / __repr__ — 对象打印成什么
# ============================================================
# 双下划线开头结尾的方法叫【魔法方法】（dunder method），
# Python 会在特定时机自动调用它们。
# 不定义 __str__ 时，print(对象) 显示难看的内存地址：
#   <__main__.Point object at 0x000001A2...>

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        """str() / print() 时自动调用：给人看的友好描述"""
        return f"({self.x}, {self.y})"

    def __repr__(self):
        """repr() 时自动调用：给调试/开发者看的"精确"描述"""
        return f"Point({self.x}, {self.y})"

p = Point(3, 4)
print(p)          # → (3, 4)（__str__ 生效）
print(repr(p))    # → Point(3, 4)（__repr__ 生效）
# 约定：__repr__ 最好能"重新构造这个对象"（字符串可被 eval 还原）
# 经验：优先实现 __repr__，__str__ 没定义时会【退而用 __repr__】。
#
# 药学应用：给药品类加 __str__，打印对象直接显示药名价格
class Drug2:
    def __init__(self, name, price):
        self.name, self.price = name, price
    def __str__(self):
        return f"{self.name}({self.price}元)"

print(Drug2("布洛芬", 18))   # → 布洛芬(18元)，不再是一串地址

# ============================================================
# 四、属性保护约定 — Python 没有真正的"私有"
# ============================================================
# 别的语言有 private（私有），Python 没有，靠【命名约定】：
#   self.name    → 公开：所有人都能访问
#   self._name   → 约定"内部使用"：程序员自觉别碰（下划线="请别动"）
#   self.__name  → 双下划线：触发【名称改写】，勉强算私有

class Bank:
    def __init__(self, money):
        self._money = money     # 单下划线：约定内部，但外部仍能访问

    def get_money(self):        # 通过方法访问（这就是"封装"）
        return self._money

b = Bank(1000)
print(b.get_money())    # → 1000（推荐方式：走方法）
print(b._money)         # → 1000（技术上讲还是能直接访问，只是不推荐）

# ---------- 双下划线 __xxx 的"名称改写" ----------
class Secret:
    def __init__(self):
        self.__code = 123   # 双下划线

s = Secret()
# print(s.__code)   # ← 报错！AttributeError
# 但真相是：Python 把它改名成了 _Secret__code（偷偷改了名字）
print(s._Secret__code)   # → 123（绕个弯还是能拿到）
# 结论：__xxx 不是安全机制，只是"防手滑"，防止和子类属性冲突。
#
# 一句话：Python 的私有靠【自觉 + 约定】，不靠强制。
# 团队里约定用 _ 开头表示"内部"，就足够了。


# ============================================================
# 五、实战：抽奖系统（类 + 随机）—— 含"不重复抽取"
# ============================================================
import random

class Lottery:
    def __init__(self, items):
        self.items = items

    def draw(self):              # 抽 1 个
        return random.choice(self.items)

    def draw_many(self, n):      # 抽 n 个（可能重复）
        return [self.draw() for _ in range(n)]

    def draw_unique(self, n):    # ① 抽 n 个，不重复（random.sample 一步到位）
        return random.sample(self.items, n)

    def draw_unique_manual(self, n):   # ② 手动"抽完不放回"（练手版）
        copy = self.items[:]      # 复制一份，别动原列表
        result = []
        for _ in range(n):
            x = random.choice(copy)   # 抽一个
            copy.remove(x)            # 从副本里删掉（不放回）
            result.append(x)
        return result

lotto = Lottery(["A", "B", "C", "D", "E"])
print(lotto.draw())               # 随机抽一个
print(lotto.draw_many(3))         # 随机抽 3 个（可能重复）
print(lotto.draw_unique(3))       # 抽 3 个不重复
print(lotto.draw_unique_manual(3))# 手动版：抽 3 个不重复

# ---------- 不重复抽取的两种思路（重要）----------
# ① random.sample(序列, n)：库函数一步到位，最省事
#    random.sample([1,2,3,4,5], 2) → 随机取2个，不重复
# ② 手动"抽完不放回"：理解原理（自己实现一遍更有价值）
#    复制列表 → 每次 choice 抽一个 → remove 掉 → 再抽
# 两者结果一样，②更锻炼思维。
#
# ⚠️ 注意：手动版要【复制】self.items 再删，
#    直接对 self.items 操作会把原列表改坏！
#    复制用 [:] 切片 或 list()，都是"浅拷贝"。
#
# 药学延伸：这套"随机不重复"逻辑 = 抽样/分组实验里
#   随机分组、随机抽样的基础（比如把 30 只小鼠随机分 3 组）。

# ============================================================
# 六、易错点汇总
# ============================================================
# 1. 类属性 vs 实例属性：通过对象赋值（c1.wheels=8）只会新建
#    实例属性，改不到类属性；改类属性必须 Car.wheels = 8
# 2. 三种方法：访问 self → 实例方法；访问 cls → 类方法；
#    都不访问 → 静态方法。别混用（@classmethod 里写 self 会乱）
# 3. 魔法方法别自己调用：__str__ 由 print() 自动调，
#    你手写 p.__str__() 也能调，但没人这么写
# 4. _ 和 __ 不是真私有：它们是约定/改名，不是安全锁
# 5. 抽奖不重复时：先复制再删，别动原列表

# ============================================================
# 七、自测（40%基础 + 40%中等 + 20%挑战）
# ============================================================
# 【基础】
# 1. 类属性和实例属性的根本区别是什么？各举一个药学例子。
# 2. 三种方法（实例/类/静态）分别什么时候用？
# 3. __str__ 和 __repr__ 分别在什么时候被自动调用？
#
# 【中等】
# 4. 为什么 Car.wheels = 6 能让所有对象都变，
#    而 c1.wheels = 8 只让 c1 变？结合"查找顺序"解释。
# 5. 给 Drug 类写 __str__，让 print(药) 输出"xx药，xx元/盒"。
# 6. _name 和 __name 在"能否被外部访问"上有何实际区别？
#
# 【挑战】
# 7. 写一个 Student 类：用类属性统计总人数，用实例方法
#    记录每个学生的成绩，再写一个类方法打印平均分。
# 8. 为什么说 Python 的私有"防君子不防小人"？
#    举一个 __name 名称改写的例子说明。
#
# （写不出来就回上文重读对应小节，这些题都是本节验收标准）
