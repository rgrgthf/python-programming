#字符串用引号表示，可以是但单引号，也可以是双引号或三引号（三引号可以跨行）
#字符串中的内容可以是任意字符，包括汉字、字母、数字、符号等。字符串可以使用加号（+）进行拼接，也可以使用乘号（*）进行重复。
#
#示例
str1 = "Hello"
print(str1)  # 输出: Hello
str2 = 'World'
print(str2)  # 输出: World
str3 = """This is a multi-line string."""
print(str3)  # 输出: This is a multi-line string.
#字符串拼接
str4 = str1 + " " + str2
print(str4)  # 输出: Hello World
#字符串重复
str5 = str1 * 3
print(str5)  # 输出: HelloHelloHello

#转义字符
#在字符串中，如果需要使用一些特殊字符，可以使用转义字符。常用的转义字符包括：
#\n 换行
#\t 制表符
#\\ 反斜杠
#\" 双引号
#\' 单引号
#示例
str6 = "Hello\nWorld"  # 换行
print(str6)  # 输出:
#Hello
#World
str7 = "Hello\tWorld"  # 制表符
print(str7)  # 输出: Hello   World
str8 = "This is a backslash: \\"  # 反斜杠
print(str8)  # 输出: This is a backslash: \
str9 = "He said: \"Hello!\""  # 双引号
print(str9)  # 输出: He said: "Hello!"

#\t 制表符的对齐原理：
#\t 不是插入固定数量的空格，而是将光标移动到下一个"制表位"（默认每8列一个）
#实际空格数 = 8 - (前面字符数 % 8)
#示例：观察 \t 前面字符长度不同时，产生的空格数也不同
print("a\tWorld")       # a 长度=1，8-(1%8)=7 → 7个空格
print("ab\tWorld")      # ab 长度=2，8-(2%8)=6 → 6个空格
print("abc\tWorld")     # abc 长度=3，8-(3%8)=5 → 5个空格
print("abcdefg\tWorld") # abcdefg 长度=7，8-(7%8)=1 → 1个空格
print("abcdefgh\tWorld")# abcdefgh 长度=8，8-(8%8)=0→跳到下一个制表位，8个空格

#原字符，使得转义字符失效的符号，用r或R
print(r"Hello\nWorld")
print(R"Hello\nWorld")

#字符串又被称为有序的字符序列，对字符串中某个字符的检索称为字符串的索引
#从正向开始计数，从0开始到n-1结束；从反向开始计数，从-1开始到-n结束
s = "Hello World"
print(s[0],s[-11])#输出 H H
print(s[6],s[-5])#输出 W W
#find()方法用于检索字符串中某个字符或子串的位置，如果找到则返回该位置的索引，否则返回-1
index = s.find("o") #返回第一个匹配的索引，如果没有找到则返回-1
print(index) #输出 4

#查找第n个匹配的索引：利用find()的start参数 + for循环，每次从上次找到位置+1继续搜索
#range(n)：从0开始生成n个整数（0,1,...,n-1），控制循环执行n次
#示例：找第2个"o"
n = 2
pos = -1
for i in range(n):           # i=0,1 → 循环2轮
    pos = s.find("o", pos + 1)  # 第1轮从0开始找→4，第2轮从5开始找→7
print(pos)  # 输出 7
