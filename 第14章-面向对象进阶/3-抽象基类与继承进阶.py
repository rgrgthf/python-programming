# ============================================================
# 面向对象进阶 ③ — 抽象基类 ABC 与继承进阶
# ============================================================
# ABC（Abstract Base Class）= 抽象基类：
# 定义"模板"，规定子类必须实现哪些方法。
# 适合设计框架/接口，保证子类行为一致。

from abc import ABC, abstractmethod

# ============================================================
# 一、基本用法
# ============================================================
class Animal(ABC):
    @abstractmethod
    def speak(self):
        """子类必须实现这个方法"""
        pass

    @abstractmethod
    def move(self):
        pass

# 直接实例化会报错（因为方法没实现）
# a = Animal()   # → TypeError: Can't instantiate abstract class

class Dog(Animal):
    def speak(self):
        return "汪汪！"
    def move(self):
        return "四条腿跑"

class Cat(Animal):
    def speak(self):
        return "喵~"
    def move(self):
        return "静悄悄地走"

d = Dog()
c = Cat()
print(d.speak(), d.move())   # → 汪汪！ 四条腿跑
print(c.speak(), c.move())   # → 喵~ 静悄悄地走

# 子类如果漏实现某个方法，实例化就报错（强制完整！）

# ============================================================
# 二、实战：实验数据处理器接口
# ============================================================
# 场景：不同仪器导出的数据格式不同，但都要经过
#       "读取 → 清洗 → 分析 → 输出" 的流程
class DataProcessor(ABC):
    """所有数据处理器的统一接口"""

    @abstractmethod
    def load(self, path):
        """读取原始数据"""
        pass

    @abstractmethod
    def clean(self):
        """清洗数据"""
        pass

    @abstractmethod
    def analyze(self):
        """分析并返回结果"""
        pass

    def run(self, path):
        """模板方法：固定流程，子类只需实现上面三步"""
        self.load(path)
        self.clean()
        return self.analyze()


class SpectroProcessor(DataProcessor):
    """光谱仪数据处理器"""
    def load(self, path):
        print(f"[光谱] 读取文件 {path}")
        self.data = [0.5, 1.0, 0.8]

    def clean(self):
        print("[光谱] 基线校正...")
        self.data = [x - 0.05 for x in self.data]

    def analyze(self):
        print(f"[光谱] 平均吸光度: {sum(self.data)/len(self.data):.3f}")
        return sum(self.data) / len(self.data)


class HPLCProcessor(DataProcessor):
    """液相色谱数据处理器"""
    def load(self, path):
        print(f"[HPLC] 读取文件 {path}")
        self.data = {"峰1": 12.5, "峰2": 8.3}

    def clean(self):
        print("[HPLC] 去噪声...")

    def analyze(self):
        print(f"[HPLC] 主峰保留时间: {max(self.data.values())} min")
        return max(self.data.values())


# 用统一的 run() 接口处理不同数据
p1 = SpectroProcessor()
p1.run("data/sp1.csv")

p2 = HPLCProcessor()
p2.run("data/hplc1.dat")

# 好处：
#   1. 保证所有处理器结构一致
#   2. 新仪器只需继承 DataProcessor 实现三步
#   3. run() 模板方法固定了流程

# ============================================================
# 三、isinstance 与多态
# ============================================================
# 面向对象三大特性之一：多态（同一接口，不同实现）
def process_all(processors):
    """传入任意数量的处理器，统一处理"""
    for p in processors:
        if isinstance(p, DataProcessor):   # 检查是不是处理器家族
            p.run("data/test")

process_all([SpectroProcessor(), HPLCProcessor()])

# ============================================================
# 四、MRO 与多重继承（了解）
# ============================================================
# Python 支持多继承，查找顺序 MRO（Method Resolution Order）
class A:
    def hello(self):
        return "A"
class B:
    def hello(self):
        return "B"
class C(A, B):      # 从左到右优先
    pass

print(C().hello())   # → A（先找 A）

# 查看 MRO 顺序
print(C.__mro__)     # → C → A → B → object

# ============================================================
# 五、super() 的正确用法
# ============================================================
class Base:
    def __init__(self, name):
        self.name = name

class Extended(Base):
    def __init__(self, name, extra):
        super().__init__(name)      # 调用父类初始化
        self.extra = extra

e = Extended("样品", 42)
print(e.name, e.extra)   # → 样品 42

# ============================================================
# 六、总结
# ============================================================
# ABC + @abstractmethod：定义接口模板，强制子类实现
# 模板方法模式：run() 固定流程，子类填细节
# 多态：isinstance 检查 + 统一接口调用
# super()：正确调用父类方法
# 应用场景：写工具库/SDK、插件系统、统一处理多格式数据
