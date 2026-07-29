#逻辑运算符是对比较结果（True或False）进行逻辑运算的运算符其结果仍是布尔值
#and：两个条件都为真时，结果才为真
#or：只要有一个条件为真，则结果就为真
#not：取反
print(True and True)
print(True and False)
print(False and True)
print(False and False)
a=3>2
b=7>2
print(3>2 and 7>2)
print(3<2 and 7>2)
print(3>2 and 7<2)
print(3<2 and 7<2)
print(a or b)
print(a or not b)
print(not a or b)
print(not a or not b)

print(not a and 10/0)
#原本是10/0会报错，但and和or的结合方向是从左到右的
#not a的值是False，所以10/0不会运算也就不会报错
print(a or 10/0)
#10/0会报错，但是a的值是True，所以不会报错