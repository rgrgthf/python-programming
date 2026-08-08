# ============================================================
# RDKit 化学信息学 ③ — 原子与键的操作
# ============================================================
# 分子 = 原子 + 键。这一节学会遍历原子、看原子性质、
# 找邻居、分析键的类型和环。

from rdkit import Chem

mol = Chem.MolFromSmiles("CC(=O)Nc1ccccc1")   # 乙酰苯胺

# ============================================================
# 一、遍历原子
# ============================================================
print("原子数：", mol.GetNumAtoms())

# 遍历所有原子
for atom in mol.GetAtoms():
    idx = atom.GetIdx()              # 原子序号
    symbol = atom.GetSymbol()        # 元素符号
    print(f"原子{idx}: {symbol}")

# 原子常用属性
atom = mol.GetAtomWithIdx(0)         # 按序号取原子
print("元素符号：", atom.GetSymbol())      # → C
print("原子序数：", atom.GetAtomicNum())   # → 6
print("形式电荷：", atom.GetFormalCharge())# → 0
print("芳香性：", atom.GetIsAromatic())    # → False
print("手性：", atom.GetChiralTag())       # → CHI_UNSPECIFIED
print("氢个数：", atom.GetTotalNumHs())    # → 3（甲基）

# ============================================================
# 二、原子类型与杂化
# ============================================================
# 判断原子类型（化学环境）
c = mol.GetAtomWithIdx(0)   # 甲基碳
print("杂化：", c.GetHybridization())    # → SP3（甲基是sp3）
print("度数（连接的键数）：", c.GetDegree())  # → 1

# 找芳香原子
print("芳香原子：", [a.GetIdx() for a in mol.GetAtoms() if a.GetIsAromatic()])
# → [4,5,6,7,8,9]（苯环的6个碳）

# 找氧/氮原子
print("氧原子：", [a.GetIdx() for a in mol.GetAtoms() if a.GetSymbol() == "O"])
print("氮原子：", [a.GetIdx() for a in mol.GetAtoms() if a.GetSymbol() == "N"])

# ============================================================
# 三、邻居（键连的原子）
# ============================================================
atom = mol.GetAtomWithIdx(2)   # 羰基碳 C(=O)
print("邻居原子：", [(n.GetIdx(), n.GetSymbol()) for n in atom.GetNeighbors()])
# → [(1, 'C'), (3, 'N'), (0, 'C')] 的某种顺序

# 邻居是化学的核心概念：
#   一个碳连了几个原子？连的什么？决定它的化学环境
# 药效团（pharmacophore）分析就是研究原子间关系

# ============================================================
# 四、键的操作
# ============================================================
print("键数：", mol.GetNumBonds())

for bond in mol.GetBonds():
    a1 = bond.GetBeginAtom().GetIdx()
    a2 = bond.GetEndAtom().GetIdx()
    btype = bond.GetBondType()
    print(f"键 {a1}-{a2}: 类型 {btype}")

# 键类型：
#   SINGLE 单键  DOUBLE 双键  TRIPLE 三键  AROMATIC 芳香键
# 判断：
bond = mol.GetBondBetweenAtoms(2, 3)   # C-N 键
print("C-N 键类型：", bond.GetBondType())
print("是否芳香键：", bond.GetIsAromatic())

# 判断原子间是否有键
print("1和2之间有键？", mol.GetBondBetweenAtoms(1, 2) is not None)
print("0和4之间有键？", mol.GetBondBetweenAtoms(0, 4) is not None)

# ============================================================
# 五、环分析
# ============================================================
from rdkit.Chem import rdMolDescriptors as desc

print("环数：", desc.CalcNumRings(mol))
print("芳香环：", desc.CalcNumAromaticRings(mol))

# 获取所有环（RingInfo）
ri = mol.GetRingInfo()
for ring in ri.AtomRings():
    print("环的原子：", ring)
# → (4, 5, 6, 7, 8, 9)（苯环的6个原子）

# 检查某原子是否在环里
for atom in mol.GetAtoms():
    if atom.IsInRing():
        print(f"原子{atom.GetIdx()}在环里")
    else:
        print(f"原子{atom.GetIdx()}不在环里")

# 环大小（5元环、6元环...）
from rdkit.Chem import rdMolDescriptors
print(desc.CalcNumRings(mol))

# 药物的环结构很重要：
#   阿司匹林含1个苯环，青霉素含β-内酰胺环+噻唑环
# 用 RDKit 能快速分析任意药物的环系

# ============================================================
# 六、SMARTS — 更高级的子结构模式
# ============================================================
# SMARTS = 带模式的SMILES（可描述"某类原子"）
#   [C]        任意碳
#   [O;H1]     有一个氢的氧（羟基氧）
#   [#7]       任意氮
#   c1ccccc1   苯环
#   [N+](=O)[O-] 硝基
# 之后子结构搜索会用到

# 示例：用 SMARTS 找羰基（C=O）
carbonyl = Chem.MolFromSmarts("[CX3]=[OX1]")
print("羰基个数：", len(mol.GetSubstructMatches(carbonyl)))
# → 1（乙酰苯胺有1个羰基）

# ============================================================
# 七、实战：分析一个药物分子的原子组成
# ============================================================
def analyze_molecule(smiles, name):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        print(f"{name}: 解析失败")
        return
    from collections import Counter
    elements = Counter(a.GetSymbol() for a in mol.GetAtoms())
    print(f"\n{name}: {Chem.MolToSmiles(mol)}")
    print(f"  化学式: {desc.CalcMolFormula(mol)}")
    print(f"  元素组成: {dict(elements)}")
    print(f"  环数: {desc.CalcNumRings(mol)}")
    # 药效团常见原子统计
    n = sum(1 for a in mol.GetAtoms() if a.GetSymbol() == "N")
    o = sum(1 for a in mol.GetAtoms() if a.GetSymbol() == "O")
    print(f"  N原子: {n}, O原子: {o}")

analyze_molecule("CC(=O)Nc1ccc(O)cc1", "对乙酰氨基酚")
analyze_molecule("CN1CCC23C4C1CC5=C2C(=C(C=C5)O)OC3C(C=C4)O", "吗啡")

# ============================================================
# 六、易错点汇总
# ============================================================
# 1. 原子/键对象用索引访问：
#    mol.GetAtomWithIdx(i)、mol.GetBondWithIdx(i)
# 2. 键类型（单/双/芳香）用 bond.GetBondType()；
#    原子符号用 atom.GetSymbol()
# 3. 修改分子前先确认是否允许（RDKit 默认不可变）
# 4. 遍历原子看它连了哪些邻居：atom.GetNeighbors()
# 5. 分析复杂分子前先打印原子数/键数确认解析成功
# 6. 手性/杂化信息在原子对象上，别在分子对象上找

# ============================================================
# 七、自测（40%基础 + 40%中等 + 20%挑战）
# ============================================================
# 【基础】
# 1. 怎么取第 i 个原子？
# 2. 键类型用什么方法取？
# 3. 怎么遍历一个原子的邻居？
#
# 【中等】
# 4. 分析阿司匹林：打印每个原子的符号。
# 5. 找出分子中的芳香键。
# 6. 打印某个原子的邻居和键类型。
#
# 【挑战】
# 7. 写一个 analyze_molecule 函数：原子/键/芳香环统计。
# 8. 解释为什么 RDKit 的 Mol 默认不可变，这有什么好处？
