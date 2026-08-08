# ============================================================
# 面向对象进阶 ② — 特殊方法（魔术方法）
# ============================================================
# 特殊方法 = 双下划线方法 __xxx__。
# 它们让对象支持 + - == len() print() 等内置操作。
# 写自己的"数值类""容器类"时必用。

# ============================================================
# 一、最常用的特殊方法
# ============================================================
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        """print/交互环境显示什么"""
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):
        """支持 + 运算"""
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """支持 - 运算"""
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        """支持 * 数乘"""
        return Vector(self.x * scalar, self.y * scalar)

    def __eq__(self, other):
        """支持 == 比较"""
        return self.x == other.x and self.y == other.y

    def __len__(self):
        """支持 len()"""
        return 2

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1)              # → Vector(1, 2)（__repr__）
print(v1 + v2)         # → Vector(4, 6)（__add__）
print(v1 * 3)          # → Vector(3, 6)（__mul__）
print(v1 == Vector(1, 2))  # → True（__eq__）
print(len(v1))         # → 2（__len__）

# ============================================================
# 二、实战：剂量计算类（药学例子）
# ============================================================
class Dose:
    """剂量类：支持加减和比较"""
    def __init__(self, mg):
        self.mg = mg

    def __repr__(self):
        return f"{self.mg}mg"

    def __add__(self, other):
        return Dose(self.mg + other.mg)

    def __sub__(self, other):
        return Dose(self.mg - other.mg)

    def __mul__(self, times):
        return Dose(self.mg * times)

    def __lt__(self, other):
        """支持 < 比较（排序用）"""
        return self.mg < other.mg

    def __le__(self, other):
        return self.mg <= other.mg

d1 = Dose(50)
d2 = Dose(100)
print(d1 + d2)          # → 150mg
print(d2 * 2)           # → 200mg
print(d1 < d2)          # → True

# 有了 __lt__，就能排序
doses = [Dose(100), Dose(25), Dose(50)]
sorted_doses = sorted(doses)
print(sorted_doses)     # → [25mg, 50mg, 100mg]

# ============================================================
# 三、容器类特殊方法
# ============================================================
class Plate:
    """96孔板类：像列表一样访问"""
    def __init__(self, rows=8, cols=12):
        self._wells = [["."] * cols for _ in range(rows)]

    def __getitem__(self, index):
        return self._wells[index]

    def __setitem__(self, index, value):
        self._wells[index] = value

    def __len__(self):
        return len(self._wells)

    def __repr__(self):
        return f"Plate({len(self._wells)}行x{len(self._wells[0])}列)"

p = Plate()
p[0][0] = "A1样品"      # 像列表一样赋值
print(p[0][0])          # → A1样品
print(len(p))           # → 8
print(p)                # → Plate(8行x12列)

# ============================================================
# 四、字符串相关：__str__ vs __repr__
# ============================================================
# __str__：给用户看（print）
# __repr__：给开发者看（调试/交互环境）
class Sample:
    def __init__(self, id, value):
        self.id = id
        self.value = value

    def __str__(self):
        return f"样品{self.id}（值{self.value}）"

    def __repr__(self):
        return f"Sample(id={self.id!r}, value={self.value!r})"

s = Sample("A1", 0.523)
print(s)               # → 样品A1（值0.523）（__str__）
print(repr(s))         # → Sample(id='A1', value=0.523)（__repr__）

# ============================================================
# 五、其他常用特殊方法速查
# ============================================================
# __bool__       bool(obj) 时调用
# __hash__       hash(obj) 时调用（对象进集合/字典键）
# __contains__   "x in obj" 时调用
# __call__       对象当函数调用 obj()
# __iter__       迭代（for）
# __enter__/__exit__  with 语句（上下文管理器，第13章学过）
# __getitem__    支持 obj[key]
# __setitem__    支持 obj[key] = value

# __call__ 例子：可调用对象
class Power:
    def __init__(self, n):
        self.n = n
    def __call__(self, x):
        return x ** self.n

square = Power(2)
cube = Power(3)
print(square(5))    # → 25（对象当函数用）
print(cube(2))      # → 8

# ============================================================
# 六、总结
# ============================================================
# 特殊方法让自定义类"像内置类型一样好用"
# 最常用：__init__ __repr__ __str__ __eq__ __lt__ __add__

# ============================================================
# 七、易错点汇总
# ============================================================
# 1. __repr__ 和 __str__：__str__ 给用户（print），
#    __repr__ 给开发者；没写 __str__ 时 print 会退用 __repr__
# 2. __eq__ 只定义了相等，不自动定义不等；
#    __lt__ 只定义了小于，sorted 可能还需要其他比较
# 3. 特殊方法由 Python 自动调用，你【不要直接调用】
#    （写 v1.__add__(v2) 没人这么干，写 v1 + v2）
# 4. __hash__ 和 __eq__ 一起定义才一致；
#    定义了 __eq__ 没定义 __hash__，对象就不能进集合/当字典键
# 5. __getitem__/__len__ 实现后，对象才能像序列一样用
# 6. 实现 __call__ 后对象可调用，但别滥用（可读性）

# ============================================================
# 八、自测（40%基础 + 40%中等 + 20%挑战）
# ============================================================
# 【基础】
# 1. __str__ 和 __repr__ 分别在什么时候被调用？
# 2. __add__ 能让对象支持什么操作？
# 3. 特殊方法需要自己调用吗？为什么？
#
# 【中等】
# 4. 给 Dose 类补 __eq__，让 Dose(50) == Dose(50) 返回 True。
# 5. 写一个 __lt__，让 Dose 列表能 sorted() 排序。
# 6. 解释 __eq__ 和 __hash__ 的关系，为什么不一起定义会出问题。
#
# 【挑战】
# 7. 实现 __getitem__/__setitem__/__len__ 的"96孔板"类（参考第三节）。
# 8. 给 Dose 类实现 __call__，让 Dose(50)(2) == 100mg（代表"加倍"）。
# 进阶：__getitem__ __call__ __len__ __contains__
# 看到双下划线方法 = 某个内置操作被定制了
