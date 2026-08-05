def fib(n):
    fibs = []
    a,b = 0,1
    for _ in range(n):
        fibs.append(a)
        a,b = b,a+b
    return fibs
fib(50)
with open("fib.txt","w",encoding="utf-8") as f:
    for i in fib(50):
        f.write(str(i)+" ")