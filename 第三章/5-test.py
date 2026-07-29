#对字符串中某个子串或区间的检索称为切片
s="Hello World"
print(s[2:7])#输出 "llo W"，从第一个l开始，到第二个o结束但不包含第二个o
print(s[:5])#输出 "Hello"，从开头到第6个字符（不包括第6个字符）
print(s[6:])#输出 "World"，从W开始到最后一个字符
print(s[-1])#输出 "d"，最后一个字符
print(s[::-1])#输出 "dlroW olleH"，整个字符串反转,其中-1的含义是步长为-1
print(s[::2])#输出 "HloWrd"，每隔一个字符取一次
print(s[::-2])#输出drWoelH，从右往左取，每隔一个字符取一次