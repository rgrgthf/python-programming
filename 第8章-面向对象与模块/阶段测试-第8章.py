# ============================================================
# 第八章 阶段测试 — 面向对象 / 模块 / 标准库 / 调试
# ============================================================
# 共 12 题：读代码、简答、编程
# ============================================================


# ========== 一、类与对象 ==========

# 1.【读代码】写出输出结果：
print("第1题：")
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


# 2.【简答】self 是什么？为什么方法定义时第一个参数是 self？
# 你的答案：


# 3.【读代码】写出输出结果（类属性 vs 实例属性）：
print("第3题：")
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


# 4.【读代码】写出输出结果（继承 + 重写）：
print("第4题：")
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


# 5.【简答】什么时候用继承？判断"is-a"和"has-a"。
# 你的答案：


# ========== 二、模块 ==========

# 6.【简答】直接运行一个文件时 __name__ 等于什么？
#     被 import 时等于什么？if __name__ == "__main__" 的作用？
# 你的答案：


# ========== 三、标准库 ==========

# 7.【读代码】写出输出结果：
print("第7题：")
import math
print(math.ceil(3.2), math.floor(3.8))
print(math.sqrt(16))
# 你的答案：


# 8.【编程】用 random 生成 5 个 1~50 的随机整数并打印；
#     再用 random.choice 从 ["A","B","C"] 随机选一个。
print("第8题（你的代码）：")
# 你的代码：


# 9.【编程】用 json 把一个字典 {"name": "小明", "scores": [90, 85]}
#     转成字符串，再转回字典，验证 name 值。
print("第9题（你的代码）：")
# 你的代码：


# ========== 四、调试 ==========

# 10.【简答】看到如下报错，你第一件事看哪一行？
#   Traceback (most recent call last):
#     File "x.py", line 5, in <module>
#       print(lst[10])
#   IndexError: list index out of range
# 错误类型是什么？问题出在哪？
# 你的答案：


# 11.【找 bug】下面代码想"输入年龄加1"，为什么报错？怎么改？
# age = input("年龄：")
# print(age + 1)
# 你的答案：


# 12.【综合编程】定义一个类 Student：
#     - __init__(name, score)
#     - 方法 report()：score>=60 打印"及格"，否则"不及格"
#     - 类属性 count 统计创建了多少个学生
#     创建 3 个学生对象，调用 report，打印总人数。
print("第12题（你的代码）：")
# 你的代码：
