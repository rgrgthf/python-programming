# ============================================================
# 面向对象进阶 ① — property 与封装进阶
# ============================================================
# 第8章学了类的基础。这一节把 OOP 的"高级装备"补齐：
# property 属性、只读属性、数据校验、类方法/静态方法。
# 写工具类、SDK 时必用。

# ============================================================
# 一、property：把方法变成属性
# ============================================================
# 场景：不想直接暴露数据，但想用"取值"的方式访问
class Drug:
    def __init__(self, name, price):
        self.name = name
        self._price = price      # 下划线 = "内部数据，别乱碰"

    @property
    def price(self):
        """读取价格（可以加逻辑）"""
        return self._price

    @price.setter
    def price(self, value):
        """设置价格（可以校验）"""
        if value < 0:
            raise ValueError("价格不能为负")
        self._price = value

d = Drug("氯雷他定", 20)
print(d.price)       # → 20（像属性一样用，不是 d.price()）
d.price = 25         # → 触发 setter
print(d.price)       # → 25
# d.price = -5       # → ValueError: 价格不能为负（自动拦截）

# 好处：外部代码用法不变（d.price），内部逻辑随便加

# ============================================================
# 二、只读属性（只有 @property，没有 setter）
# ============================================================
class Molecule:
    def __init__(self, smiles):
        self._smiles = smiles
        self._atoms = len(smiles)   # 模拟原子数计算

    @property
    def atoms(self):
        """只读：外部不能修改原子数"""
        return self._atoms

m = Molecule("CCO")
print(m.atoms)     # → 3
# m.atoms = 5      # → AttributeError（没有 setter，只读）

# ============================================================
# 三、property 实战：计算属性（不存数据，实时算）
# ============================================================
class Sample:
    def __init__(self, conc, volume):
        self.conc = conc      # 浓度
        self.volume = volume  # 体积

    @property
    def amount(self):
        """计算属性：含量 = 浓度 × 体积（不占用存储）"""
        return self.conc * self.volume

s = Sample(2.5, 100)
print(s.amount)    # → 250.0
s.volume = 200     # 改体积后
print(s.amount)    # → 500.0（自动重新计算）

# ============================================================
# 四、@classmethod 类方法（第8章学过，这里复习+实战）
# ============================================================
# 类方法：不依赖实例，操作的是类本身（cls）
class Drug:
    total = 0          # 类属性

    def __init__(self, name):
        self.name = name
        Drug.total += 1

    @classmethod
    def from_dict(cls, data):
        """工厂方法：从字典创建实例"""
        return cls(data["name"])

    @classmethod
    def show_total(cls):
        print(f"已创建 {cls.total} 个药品")

a = Drug("阿司匹林")
b = Drug("布洛芬")
Drug.show_total()            # → 已创建 2 个药品
c = Drug.from_dict({"name": "对乙酰氨基酚"})
Drug.show_total()            # → 已创建 3 个药品

# ============================================================
# 五、@staticmethod 静态方法（和类无关的工具函数）
# ============================================================
class Drug:
    @staticmethod
    def is_valid_name(name):
        """与实例无关的校验工具"""
        return len(name) > 1 and name.isalpha()

    @staticmethod
    def parse_price(text):
        """从字符串解析价格"""
        try:
            return float(text.replace("元", ""))
        except ValueError:
            return None

print(Drug.is_valid_name("阿司匹林"))   # → True
print(Drug.is_valid_name(""))           # → False
print(Drug.parse_price("25元"))         # → 25.0

# 区别总结：
#   实例方法 self    → 需要实例，操作实例数据
#   类方法 cls      → 不需要实例，操作类属性/做工厂
#   静态方法 无      → 纯工具函数，放在类里只是归类

# ============================================================
# 六、__slots__：节省内存（处理大量对象时）
# ============================================================
# 默认每个实例都有 __dict__（字典存属性，浪费内存）
# __slots__ 固定属性名，内存大减

class Small:
    __slots__ = ["x", "y"]
    def __init__(self, x, y):
        self.x = x
        self.y = y

# 当你创建几十万个对象（比如海量分子）时，用 __slots__ 省内存
# 缺点：不能添加 slots 之外的属性

# ============================================================
# 七、总结
# ============================================================
# @property      把方法变属性 + 加校验/计算
# @xxx.setter    设置时拦截校验
# @classmethod   工厂方法 / 操作类属性
# @staticmethod  类里的工具函数
# __slots__      大量实例时省内存（了解）
