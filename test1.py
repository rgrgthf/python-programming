class Drug:
    def __init__(self,name,price):
        self.name = name
        self.price = price

    def show(self):
        print(f"{self.name}药片，{self.price}元")

d = Drug("氯雷他定",20)
d.show()

class Cat:
    def __init__(self,name,color):
        self.name = name
        self.color = color

    def meow(self):
        print(f"{self.name}:喵~")

    def show_color(self):
        print(f"{self.name}是{self.color}的!")

cat1 = Cat("小白","黑色")
cat1.meow()
cat1.show_color()