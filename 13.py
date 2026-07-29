import math

def TriangleArea(a, b, c):
    """
    计算三角形的面积（海伦公式）
    参数a,b,c: 三角形的三条边长
    返回: 三角形的面积；若不能构成三角形，返回None
    """
    # 先判断是否能构成三角形（任意两边之和大于第三边）
    if a + b > c and a + c > b and b + c > a:
        # 计算半周长
        c_semi = (a + b + c) / 2
        # 海伦公式计算面积
        area = math.sqrt(c_semi * (c_semi - a) * (c_semi - b) * (c_semi - c))
        return area
    else:
        print("输入的三边无法构成三角形")
        return None


# 测试示例
if __name__ == "__main__":
    print(TriangleArea(3, 4, 5))  # 输出6.0（直角三角形面积）
    print(TriangleArea(1, 2, 3))  # 输出提示+None（无法构成三角形）