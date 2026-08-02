a = 0
for i in range(1,1001):
    for j in range(1,i):
        if i % j == 0:
            a += j
        if i == a:
            print(i)