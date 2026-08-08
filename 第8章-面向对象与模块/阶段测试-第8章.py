# ============================================================
# 📘 第八章 阶段测试（分层版）
# ============================================================
# 覆盖：面向对象 / 模块 / 标准库 / 调试
# 共 12 题 = 基础 5 题（40%）+ 中等 5 题（40%）+ 挑战 2 题（20%）
# 用法：先自己写/想答案，最后再对"参考答案"，别偷看。

# ============================================================
# 第一部分：基础题（40%）—— 概念 + 读代码
# ============================================================

# 【基础1·简答】self 是什么？为什么方法定义时第一个参数是 self？
# 你的答案：


# 【基础2·读代码】写出输出结果：
print("基础2：")
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def bark(self):
        print(f"{self.name}：汪汪！")

d = Dog("旺财", 3)
d.bark()
print(d.age)
# 你的答案：


# 【基础3·读代码】类属性 vs 实例属性，写出输出：
print("基础3：")
class Car:
    wheels = 4
    def __init__(self, brand):
        self.brand = brand

c1 = Car("宝马")
c2 = Car("奔驰")
Car.wheels = 6
print(c1.wheels, c2.wheels)
print(c1.brand, c2.brand)
# 你的答案：


# 【基础4·简答】直接运行一个文件时 __name__ 等于什么？
#     被 import 时等于什么？if __name__ == "__main__" 的作用？
# 你的答案：


# 【基础5·读报错】看到下面报错，第一件事看哪一行？错误类型？
#   Traceback (most recent call last):
#     File "x.py", line 5, in <module>
#       print(lst[10])
#   IndexError: list index out of range
# 你的答案：

# ============================================================
# 第二部分：中等题（40%）—— 继承 + 编程
# ============================================================

# 【中等1·读代码】继承 + 重写，写出输出：
print("中等1：")
class Animal:
    def speak(self):
        print("动物叫")

class Cat(Animal):
    def speak(self):
        print("喵喵喵")

class Dog(Animal):
    pass

Cat().speak()
Dog().speak()
# 你的答案：


# 【中等2·简答】什么时候用继承？判断 is-a 和 has-a，
#     各举一个药学例子。
# 你的答案：


# 【中等3·编程】用 random 生成 5 个 1~50 的随机整数并打印；
#     再用 random.choice 从 ["A","B","C"] 随机选一个。
print("中等3（你的代码）：")
# 你的代码：


# 【中等4·编程】用 json 把字典 {"name": "小明", "scores": [90, 85]}
#     转成字符串，再转回字典，打印 name 的值。
print("中等4（你的代码）：")
# 你的代码：


# 【中等5·找bug】下面代码想"输入年龄加1"，为什么报错？怎么改？
#   age = input("年龄：")
#   print(age + 1)
# 你的答案：

# ============================================================
# 第三部分：挑战题（20%）—— 综合应用
# ============================================================

# 【挑战1·综合编程】定义 Student 类：
#   - __init__(name, score)
#   - 方法 report()：score>=60 打印"及格"，否则"不及格"
#   - 类属性 count 统计创建了多少个学生
#   创建 3 个学生对象，调用 report，打印总人数。
print("挑战1（你的代码）：")
# 你的代码：


# 【挑战2·综合编程】用【多态】实现给药途径：
#   - 基类 DrugByRoute：__init__(name)，方法 route()（留空 pass）
#   - 子类 Tablet：route() 打印 "xx：口服给药"
#   - 子类 Injection：route() 打印 "xx：静脉注射"
#   - 把两个对象放进列表，循环调用 route()
print("挑战2（你的代码）：")
# 你的代码：

# ============================================================
# 参考答案（做完再对！）
# ============================================================
# 【基础1】self = 调用方法的那个对象本身。因为 d.bark() 等价于
#   Dog.bark(d)，Python 自动把 d 塞进来，方法需要 self 接住它。
# 【基础2】旺财：汪汪！
#           3
# 【基础3】6 6（Car.wheels=6 改了类属性，所有对象共享）
#           宝马 奔驰（实例属性各自独立）
# 【基础4】直接运行 = "__main__"；被 import = 模块名；
#   if __name__ == "__main__"：只有直接运行时才执行里面的测试代码
# 【基础5】先看最后一行（错误类型 IndexError），再看行号 line 5；
#   原因：lst[10] 下标越界（列表长度不够）
# 【中等1】喵喵喵（Cat 重写了 speak）
#           动物叫（Dog 继承父类，没重写）
# 【中等2】is-a（是"一种"）→ 继承：抗生素 是一种 药物；
#   has-a（"拥有"）→ 组合：处方 有 药品条目（不该继承）
# 【中等3】import random
#   nums = [random.randint(1, 50) for _ in range(5)]; print(nums)
#   print(random.choice(["A", "B", "C"]))
# 【中等4】import json
#   data = {"name": "小明", "scores": [90, 85]}
#   s = json.dumps(data, ensure_ascii=False); back = json.loads(s)
#   print(back["name"])   # → 小明
# 【中等5】input() 返回字符串，"18" + 1 会 TypeError。
#   改：age = int(input("年龄："))
# 【挑战1】class Student:
#     count = 0
#     def __init__(self, name, score):
#         self.name = name; self.score = score; Student.count += 1
#     def report(self):
#         print("及格" if self.score >= 60 else "不及格")
#   s1 = Student("小明", 85); s2 = Student("小红", 45); s3 = Student("张三", 90)
#   s1.report(); s2.report(); s3.report(); print(Student.count)  # → 3
# 【挑战2】class DrugByRoute:
#     def __init__(self, name): self.name = name
#     def route(self): pass
#   class Tablet(DrugByRoute):
#     def route(self): print(f"{self.name}：口服给药")
#   class Injection(DrugByRoute):
#     def route(self): print(f"{self.name}：静脉注射")
#   for dg in [Tablet("布洛芬片"), Injection("头孢曲松")]:
#       dg.route()
