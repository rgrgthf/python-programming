# ============================================================
# 测试与代码质量 ① — pytest 单元测试
# ============================================================
# 为什么要写测试？
#   代码一改就坏、改完不敢确认 → 测试是"安全网"。
#   pytest 是 Python 最流行的测试框架，简单强大。
#   ⚠️ 需要安装：pip install pytest

# ============================================================
# 一、被测试的代码（通常单独放一个模块）
# ============================================================
# 这里用内联函数演示。实际项目里：
#   被测代码 → my_module.py
#   测试代码 → test_my_module.py（pytest 自动发现）

def calc_dose(weight, dose_per_kg):
    """计算给药剂量"""
    if weight <= 0 or dose_per_kg <= 0:
        raise ValueError("体重和剂量必须为正")
    return weight * dose_per_kg


def is_prime(n):
    """判断质数"""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def normalize(data):
    """把数据缩放到 0~1"""
    if not data:
        return []
    min_v, max_v = min(data), max(data)
    if max_v == min_v:
        return [0.5] * len(data)
    return [(x - min_v) / (max_v - min_v) for x in data]

# ============================================================
# 二、pytest 测试的写法
# ============================================================
# pytest 规则：
#   1. 测试文件：test_开头.py（或 _test.py 结尾）
#   2. 测试函数：test_开头
#   3. 用 assert 断言（pytest 自动报告失败详情）
#   4. 运行：终端里 pytest 或 python -m pytest

def test_calc_dose_normal():
    assert calc_dose(60, 10) == 600

def test_calc_dose_float():
    assert calc_dose(55.5, 2.5) == 138.75

def test_calc_dose_invalid():
    # 用 pytest.raises 检查是否抛出异常
    import pytest
    with pytest.raises(ValueError):
        calc_dose(0, 10)
    with pytest.raises(ValueError):
        calc_dose(60, -1)

def test_is_prime():
    assert is_prime(2) == True
    assert is_prime(3) == True
    assert is_prime(4) == False
    assert is_prime(1) == False

def test_normalize():
    assert normalize([1, 2, 3, 4]) == [0, 1/3, 2/3, 1]
    assert normalize([]) == []

def test_normalize_same_values():
    assert normalize([5, 5, 5]) == [0.5, 0.5, 0.5]

# ============================================================
# 三、在 VS Code 里运行测试
# ============================================================
# 方法1：终端运行
#   python -m pytest test_文件.py
#   python -m pytest             # 运行所有测试
#   python -m pytest -v          # 详细模式（显示每个测试名）
#
# 方法2：VS Code 测试面板
#   左侧"测试"图标（烧瓶形状）
#   点击"配置 Python 测试" → 选 pytest
#   之后可以点绿色箭头运行单个测试，失败显示红色

# ============================================================
# 四、参数化测试（多组数据一键测）
# ============================================================
import pytest

@pytest.mark.parametrize("n,expected", [
    (2, True),
    (3, True),
    (4, False),
    (5, True),
    (9, False),
    (17, True),
    (25, False),
])
def test_is_prime_param(n, expected):
    """一组参数跑一次测试，共7次"""
    assert is_prime(n) == expected

# ============================================================
# 五、测试覆盖率（了解）
# ============================================================
# 覆盖率 = 有多少代码被测试到
# 安装：pip install pytest-cov
# 运行：python -m pytest --cov=my_module
# 目标：核心逻辑覆盖率 100%，一般 80% 以上就好

# ============================================================
# 六、测试驱动开发 TDD（进阶理念）
# ============================================================
# TDD 流程：
#   1. 先写测试（描述"应该怎样"）
#   2. 运行测试 → 失败（红）
#   3. 写最简代码让测试通过（绿）
#   4. 重构优化
# 好处：写代码时目标明确，改代码时不怕回归

# ============================================================
# 七、总结
# ============================================================
# pytest 三要素：test_文件、test_函数、assert断言
# 边界测试：空数据/0/负数/极大极小都要测
# 参数化：@pytest.mark.parametrize 批量测
# 异常测试：pytest.raises
# 习惯：改完代码跑一遍测试，确认没弄坏别的
