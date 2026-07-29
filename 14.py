# 实验指导5.5-1：列表的基本操作（示例：创建、增删改查）
def list_operations():
    # 创建列表
    fruits = ["苹果", "香蕉", "橙子"]
    print("初始列表：", fruits)
    
    # 增加元素
    fruits.append("葡萄")
    print("添加后：", fruits)
    
    # 删除元素
    del fruits[1]
    print("删除索引1后：", fruits)
    
    # 修改元素
    fruits[0] = "西瓜"
    print("修改后：", fruits)
    
    # 查找元素
    print("是否包含橙子：", "橙子" in fruits)


# 实验指导5.5-3：元组的基本操作（示例：创建、访问、拼接）
def tuple_operations():
    # 创建元组
    nums = (1, 2, 3, 4)
    print("初始元组：", nums)
    
    # 访问元素
    print("元组第2个元素：", nums[1])
    
    # 元组拼接
    new_nums = nums + (5, 6)
    print("拼接后元组：", new_nums)


# 执行操作
if __name__ == "__main__":
    list_operations()
    print("-" * 20)
    tuple_operations()
