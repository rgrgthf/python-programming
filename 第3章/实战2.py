#根据父母身高预测孩子身高，孩子身高=（父亲身高+母亲身高）*0.54
dad_height = float(input("请输入父亲的身高（单位：cm）："))
mom_height = float(input("请输入母亲的身高（单位：cm）："))
print("预测孩子的身高为：",round((dad_height+mom_height)*0.54,1),"cm",sep="")