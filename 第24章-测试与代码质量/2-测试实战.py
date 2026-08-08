# ============================================================
# 测试与代码质量 ② — 实战：给数据处理写测试
# ============================================================
# 把测试用到真实的药学数据处理场景。
# 场景：写一个"标准曲线计算浓度"模块，然后给它写测试。
# ⚠️ 需要 pytest：pip install pytest

# ============================================================
# 一、被测模块：标准曲线计算
# ============================================================
# （实际项目中会拆到单独文件 standard_curve.py）

def linear_fit(x_list, y_list):
    """线性回归：返回 (斜率, 截距)。最小二乘法。"""
    n = len(x_list)
    if n < 2:
        raise ValueError("至少需要2个点")
    if n != len(y_list):
        raise ValueError("x和y长度不一致")

    x_mean = sum(x_list) / n
    y_mean = sum(y_list) / n
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_list, y_list))
    denominator = sum((x - x_mean) ** 2 for x in x_list)
    if denominator == 0:
        raise ValueError("所有x值相同，无法拟合")

    k = numerator / denominator
    b = y_mean - k * x_mean
    return k, b


def predict_conc(absorbance, k, b):
    """由吸光度反推浓度：x = (y - b) / k"""
    if k == 0:
        raise ValueError("斜率为0，无法反推")
    return (absorbance - b) / k


def calc_r_squared(x_list, y_list, k, b):
    """计算 R²（拟合优度）"""
    y_mean = sum(y_list) / len(y_list)
    ss_res = sum((y - (k * x + b)) ** 2 for x, y in zip(x_list, y_list))
    ss_tot = sum((y - y_mean) ** 2 for y in y_list)
    if ss_tot == 0:
        return 1.0
    return 1 - ss_res / ss_tot

# ============================================================
# 二、测试：正常情况
# ============================================================
def test_linear_fit_perfect():
    """完美直线 y = 2x + 1"""
    x = [1, 2, 3, 4]
    y = [3, 5, 7, 9]
    k, b = linear_fit(x, y)
    assert k == pytest.approx(2.0)
    assert b == pytest.approx(1.0)

def test_predict_conc():
    """用拟合结果反推浓度"""
    k, b = 2.0, 1.0
    conc = predict_conc(5.0, k, b)   # (5-1)/2 = 2
    assert conc == pytest.approx(2.0)

def test_r_squared_perfect():
    """完美拟合 R²=1"""
    x = [1, 2, 3]
    y = [3, 5, 7]
    k, b = linear_fit(x, y)
    assert calc_r_squared(x, y, k, b) == pytest.approx(1.0)

# ============================================================
# 三、测试：边界和异常
# ============================================================
import pytest

def test_linear_fit_not_enough_points():
    with pytest.raises(ValueError):
        linear_fit([1], [2])

def test_linear_fit_mismatch_length():
    with pytest.raises(ValueError):
        linear_fit([1, 2], [1])

def test_linear_fit_flat_x():
    """所有x相同 → 无法拟合"""
    with pytest.raises(ValueError):
        linear_fit([1, 1, 1], [1, 2, 3])

def test_predict_conc_zero_slope():
    with pytest.raises(ValueError):
        predict_conc(1.0, 0, 0)

# ============================================================
# 四、测试：真实数据的合理性（关键！）
# ============================================================
def test_real_standard_curve():
    """真实标准曲线数据：浓度 vs 吸光度"""
    conc = [0, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0]
    abs_ = [0, 0.048, 0.125, 0.251, 0.51, 1.01, 2.49]

    k, b = linear_fit(conc, abs_)
    r2 = calc_r_squared(conc, abs_, k, b)

    # 合理性断言：
    assert k > 0                    # 斜率应为正
    assert 0.9 < r2 <= 1.0          # R² 应很高

    # 反推浓度应为正
    for a in [0.2, 0.5, 1.5]:
        c = predict_conc(a, k, b)
        assert c > 0

# ============================================================
# 五、运行方式回顾
# ============================================================
# 终端：
#   python -m pytest 2-测试实战.py -v
#   python -m pytest -v          # 整个文件夹
# 会看到每个 test_ 函数的结果：PASSED / FAILED
#
# 注意：这个文件里 import pytest 用了两次（顶部和上面）
#       实际项目里放在文件顶部一次即可

# ============================================================
# 六、什么时候写测试？（实用建议）
# ============================================================
# 1. 核心计算函数（剂量/浓度/统计）→ 必须写
# 2. 数据清洗逻辑 → 建议写
# 3. 界面/绘图 → 一般不用写
# 4. 改代码前 → 先跑测试确认没破坏
# 5. 出 bug → 先写一个会失败的测试，再修复（TDD）
#
# 作品集加分项：项目里带测试文件 = 专业工程素养

# ============================================================
# 七、总结
# ============================================================
# 被测模块（纯函数）+ 测试文件（test_开头）
# 正常用例 + 边界用例 + 异常用例
# pytest.approx 处理浮点数比较
# pytest.raises 检查异常
# 真实数据合理性断言（斜率正、R²高）

# ============================================================
# 六、易错点汇总
# ============================================================
# 1. 科学计算测试：不要断言"精确相等"，用 pytest.approx
#    （浮点误差会导致测试不稳定）
# 2. 合理性断言：斜率应为正、R² 应接近 1、浓度应为正
#    ——用业务常识约束结果
# 3. 测试数据要覆盖：正常值、边界值（0、负数）、异常输入
# 4. 测试函数要可复现：别依赖随机数（固定 seed）
# 5. 一个函数一个测试文件，别把全项目塞一个 test
# 6. 测试跑挂别慌：先看是哪一行断言失败

# ============================================================
# 七、自测（40%基础 + 40%中等 + 20%挑战）
# ============================================================
# 【基础】
# 1. 浮点数比较为什么不能用 ==？用什么？
# 2. 合理性断言是什么？举一个科学计算的例子。
# 3. 测试数据要覆盖哪些情况？
#
# 【中等】
# 4. 用 pytest.approx 断言浮点计算结果。
# 5. 给标准曲线拟合写测试：斜率正、R² 高。
# 6. 给函数写边界值测试（0、负数、None）。
#
# 【挑战】
# 7. 给完整的科学计算模块写一套测试（含 pytest.approx）。
# 8. 解释为什么测试用固定 seed 保证可复现。
