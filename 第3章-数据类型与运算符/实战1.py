#输入一个四位整数，分别输出千位、百位、十位和个位的数字
num=int(input("请输入一个四位整数："))
print("个位上的数字为：",num%10)
print("十位上的数字为：",num//10%10)
print("百位上的数字为：",num//100%10)
print("千位上的数字为：",num//1000)


#第二种办法，用索引
num_str=str(num)
print("个位上的数字为：",num_str[3])
print("十位上的数字为：",num_str[2])
print("百位上的数字为：",num_str[1])
print("千位上的数字为：",num_str[0])