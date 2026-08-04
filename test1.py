with open("evens.txt","r",encoding="utf-8") as f:
    count = 0
    sum = 0
    for line in f:
        count += 1
        sum += int(line.strip())
print("数字个数：",count,"和",sum)