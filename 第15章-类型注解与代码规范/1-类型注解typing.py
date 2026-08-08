# ============================================================
# 类型注解 ① — typing 类型标注
# ============================================================
# 类型注解 = 给变量/参数/返回值标注类型。
# 好处：
#   1. VS Code 里写代码就有智能提示（补全）
#   2. 提前发现类型错误（不用等运行）
#   3. 代码自文档化（看签名就懂）
# Python 是动态类型，注解是"提示"不是"强制"（除非用 mypy 检查）。

# ============================================================
# 一、基础注解
# ============================================================
# 变量注解
age: int = 20
name: str = "楠木"
height: float = 1.75
is_ok: bool = True

# 函数注解：参数: 类型  和  -> 返回值类型
def add(a: int, b: int) -> int:
    return a + b

print(add(3, 5))   # → 8
# add("x", "y")    # 运行不报错，但 VS Code 会提示类型问题

# ============================================================
# 二、容器类型注解
# ============================================================
from typing import List, Dict, Tuple, Set, Optional, Union

# 列表
def sum_list(nums: List[float]) -> float:
    return sum(nums)

# 字典
def get_value(d: Dict[str, int], key: str) -> Optional[int]:
    return d.get(key)     # Optional = 可能返回 None

# 元组
def stats(data: Tuple[float, float]) -> float:
    return data[0] + data[1]

# 集合
def check_unique(s: Set[int]) -> bool:
    return len(s) == 3

# 新版 Python 3.9+ 可以直接用内置类型
def sum_list_v2(nums: list[float]) -> float:
    return sum(nums)

# ============================================================
# 三、Optional 与 Union（可选/联合类型）
# ============================================================
# Optional[int]  =  int 或 None（常用于"可能没有结果"）
def find_conc(values: list[float], target: float) -> Optional[int]:
    """返回目标值索引，找不到返回 None"""
    for i, v in enumerate(values):
        if v == target:
            return i
    return None

print(find_conc([0.1, 0.5, 1.0], 0.5))   # → 1
print(find_conc([0.1, 0.5, 1.0], 9.9))   # → None

# Union[int, float] = 整数或浮点数
def to_number(s: str) -> Union[int, float]:
    """字符串转数字（整数转 int，否则转 float）"""
    if "." in s:
        return float(s)
    return int(s)

print(to_number("5"))      # → 5
print(to_number("5.5"))    # → 5.5

# ============================================================
# 四、实战：给药剂量计算（带注解的完整函数）
# ============================================================
def calc_dose(weight_kg: float, dose_per_kg: float, unit: str = "mg") -> float:
    """
    计算给药剂量
    参数：
        weight_kg: 体重(kg)
        dose_per_kg: 每公斤剂量
        unit: 单位（默认mg）
    返回：总剂量
    """
    if weight_kg <= 0 or dose_per_kg <= 0:
        raise ValueError("体重和剂量必须为正")
    return weight_kg * dose_per_kg

dose = calc_dose(60.0, 10.0)
print(f"60kg小鼠需给药 {dose} mg")

# ============================================================
# 五、类型别名与自定义类型
# ============================================================
from typing import TypeAlias

# 类型别名（让复杂类型有名字）
Concentration: TypeAlias = float   # 浓度
Dose: TypeAlias = float            # 剂量

def convert_conc(conc: Concentration) -> Dose:
    """浓度转剂量（简化示例）"""
    return conc * 2

# 自定义类作为类型
class Drug:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

def apply_discount(d: Drug, rate: float) -> Drug:
    d.price = d.price * (1 - rate)
    return d

drug = Drug("氯雷他定", 20.0)
apply_discount(drug, 0.1)
print(f"{drug.name} 折后 {drug.price} 元")

# ============================================================
# 六、在 VS Code 里开启类型检查
# ============================================================
# 设置 → 搜索 python.analysis.typeCheckingMode
#   off（默认）    ：不检查
#   basic          ：基础检查（推荐）
#   strict         ：严格检查（强迫症用）
#
# 开启后，类型不对的地方会出现波浪线提示（不用运行就发现 bug）

# ============================================================
# 七、易错点汇总
# ============================================================
# 1. 类型注解是【提示】不是【强制】：类型写错运行不报错，
#    要靠 VS Code 波浪线 / mypy 才能发现——别忘了开检查
# 2. Optional[int] = int 或 None（别理解成"可选参数"）
# 3. Union[int, float] 和 Optional 别混淆：
#    Optional = Union[X, None] 的简写
# 4. Python 3.9+ 用内置 list[int] / dict[str, int]；
#    老版本才需要 from typing import List
# 5. 别过度注解：变量注解适可而止，
#    【函数参数和返回值】的注解最有价值，优先写全
# 6. 自定义类本身就能当类型用（def f(d: Drug)），不用引号

# ============================================================
# 八、自测（40%基础 + 40%中等 + 20%挑战）
# ============================================================
# 【基础】
# 1. 类型注解的三个好处是什么？
# 2. Optional[int] 代表什么？
# 3. 注解是强制的吗？不匹配会怎样？
#
# 【中等】
# 4. 给 calc_dose 函数写完整注解（参数 float，返回 float）。
# 5. 用 Union 写一个函数：接受 int 或 float 都返回 float。
# 6. 说出 list[int] 和 typing.List[int] 的区别（版本）。
#
# 【挑战】
# 7. 定义类型别名 Concentration、Dose，并用在函数签名里。
# 8. 解释为什么函数注解比变量注解更重要？
#    写出一个"没有注解就很容易出错"的函数例子。

# ============================================================
# 七、总结
# ============================================================
# 注解是给人和工具看的，不是强制约束
# 常用：int/str/float/bool、list[T]/dict[K,V]、Optional、Union
# 好处：智能提示 + 提前发现错误 + 自文档化
# 建议：函数签名都写注解（专业习惯）
