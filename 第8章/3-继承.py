# ============================================================
# 继承 — 让类"遗传"父类的属性和方法
# ============================================================
# 继承 = 新类（子类）自动拥有旧类（父类）的属性和方法。
# 好处：复用代码，不用重写；还能扩展出特有功能。

# ============================================================
# 一、基本继承
# ============================================================
class Animal:                      # 父类（基类）
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name} 在吃东西")

    def sleep(self):
        print(f"{self.name} 在睡觉")

class Dog(Animal):                 # 子类（继承 Animal）
    def bark(self):                # 子类自己的方法
        print(f"{self.name}：汪汪！")

class Cat(Animal):                 # 另一个子类
    def meow(self):
        print(f"{self.name}：喵喵！")

d = Dog("旺财")
d.eat()          # → 旺财 在吃东西（继承来的！）
d.sleep()        # → 旺财 在睡觉（继承来的！）
d.bark()         # → 旺财：汪汪！（自己的）

c = Cat("咪咪")
c.eat()          # → 咪咪 在吃东西（继承的）
c.meow()         # → 咪咪：喵喵！（自己的）
# c.bark()       # ← 报错！猫没有叫的方法


# ============================================================
# 二、方法重写 — 子类改父类的方法
# ============================================================
class Bird(Animal):
    def eat(self):                 # 重写父类的 eat
        print(f"{self.name} 在啄米吃")

    def fly(self):
        print(f"{self.name} 在飞")

bird = Bird("小黄")
bird.eat()         # → 小黄 在啄米吃（覆盖了父类的"吃东西"）
bird.sleep()       # → 小黄 在睡觉（没重写的用父类的）


# ============================================================
# 三、super() — 调用父类的方法
# ============================================================
# 子类 __init__ 不会自动调用父类的 __init__！
class Student(Animal):
    def __init__(self, name, score):
        super().__init__(name)     # 调用父类 __init__（把 name 传过去）
        self.score = score         # 再加自己的属性

    def report(self):
        print(f"{self.name} 考了 {self.score} 分")

s = Student("小明", 85)
s.report()         # → 小明 考了 85 分
s.sleep()          # → 小明 在睡觉（父类方法也能用）
# 没有 super().__init__ 时，self.name 不存在，会 AttributeError


# ============================================================
# 四、多重继承（了解，慎用）
# ============================================================
class Flyer:
    def fly(self):
        print("飞行中")

class Swimmer:
    def swim(self):
        print("游泳中")

class Duck(Flyer, Swimmer):        # 继承两个类
    pass

d = Duck()
d.fly()     # → 飞行中
d.swim()    # → 游泳中
# 多重继承能"多合一"，但容易混乱，实际开发慎用


# ============================================================
# 五、isinstance() — 判断对象属于哪个类
# ============================================================
print(isinstance(d, Duck))       # → True
print(isinstance(d, Flyer))      # → True（子类对象也是父类类型！）
print(isinstance(d, Animal))     # → False（Duck 和 Animal 没关系）

# isinstance 配合继承：父类变量可以接子类对象（多态的基础）
animals = [Dog("旺财"), Cat("咪咪"), Bird("小黄")]
for a in animals:
    a.eat()     # 每个对象调用自己的 eat（重写的用重写的）
# → 旺财 在吃东西（Animal 的）
# → 咪咪 在吃东西（Animal 的）
# → 小黄 在啄米吃（Bird 重写的）


# ============================================================
# 六、什么时候用继承？
# ============================================================
# ✅ "is-a"关系：Dog 是一只 Animal → 继承
# ❌ "has-a"关系：车有发动机 → 组合（不是继承）
#
# 判断口诀：子类 是一种 父类 吗？
#   Dog is a Animal      → 继承 ✅
#   Car has a Engine     → 组合，不是继承 ❌
