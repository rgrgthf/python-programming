# ============================================================
# RDKit 化学信息学 ⑤ — 分子描述符与性质计算
# ============================================================
# 描述符 = 用数字描述分子特征的"向量"。
# QSAR/机器学习里，每个分子变成一个描述符向量 → 喂给模型。
# 这一节掌握最常用的"类药性"描述符。

from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors as desc

mol = Chem.MolFromSmiles("CC(=O)Nc1ccc(O)cc1")   # 对乙酰氨基酚

# ============================================================
# 一、最常用的描述符（背下来）
# ============================================================
print("分子量 MW：", Descriptors.MolWt(mol))           # 151.16
print("LogP（脂水分配系数）：", Descriptors.MolLogP(mol))  # 亲脂性
print("氢键供体 HBD：", Descriptors.NumHDonors(mol))   # 1（酚羟基）
print("氢键受体 HBA：", Descriptors.NumHAcceptors(mol))# 2（酰胺O + 酚O）
print("可旋转键数：", Descriptors.NumRotatableBonds(mol))  # 1
print("拓扑极性表面积 TPSA：", Descriptors.TPSA(mol))   # 49.33
print("芳香环数：", desc.CalcNumAromaticRings(mol))     # 1

# ============================================================
# 二、这些描述符的意义（药学重要！）
# ============================================================
# 类药物五规则（Lipinski's Rule of Five）：
#   一个好药通常满足：
#   - MW < 500
#   - LogP < 5
#   - 氢键供体 ≤ 5
#   - 氢键受体 ≤ 10
#   （不满足4条中2条以上的，口服吸收差）
#
# 这就是描述符的实际用途：先算一遍，初筛"类药性"

def lipinski_check(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return "解析失败"
    mw = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)
    hbd = Descriptors.NumHDonors(mol)
    hba = Descriptors.NumHAcceptors(mol)
    print(f"MW={mw:.1f} LogP={logp:.2f} HBD={hbd} HBA={hba}")
    violations = 0
    if mw > 500: violations += 1
    if logp > 5: violations += 1
    if hbd > 5: violations += 1
    if hba > 10: violations += 1
    print(f"五规则违背数：{violations}/4")
    return "类药 ✓" if violations <= 1 else "偏离类药 ⚠️"

lipinski_check("CC(=O)Nc1ccc(O)cc1")     # 对乙酰氨基酚
lipinski_check("CCO")                    # 乙醇
lipinski_check("CCCCCCCCCCCCCCCCCCCCCCCCCCCC")  # 长链烷烃（太油）

# ============================================================
# 三、更多描述符（全面版）
# ============================================================
# 原子数相关
print("重原子数：", mol.GetNumHeavyAtoms())
print("电荷：", Chem.GetFormalCharge(mol))

# rdMolDescriptors 全家桶
print("精确质量：", desc.CalcExactMolWt(mol))
print("化学式：", desc.CalcMolFormula(mol))
print("环数：", desc.CalcNumRings(mol))
print("饱和环：", desc.CalcNumSaturatedRings(mol))
print("杂环：", desc.CalcNumHeterocycles(mol))
print("芳香环：", desc.CalcNumAromaticRings(mol))

# 分数电荷（部分电荷，用于对接打分）
from rdkit.Chem import rdPartialCharges
# rdPartialCharges.ComputeGasteigerCharges(mol)
# for a in mol.GetAtoms():
#     print(a.GetIdx(), a.GetProp('_GasteigerCharge'))

# ============================================================
# 四、自定义描述符 / 原子级特征
# ============================================================
# 例：计算芳香原子占比
def aromatic_fraction(mol):
    aromatic = sum(1 for a in mol.GetAtoms() if a.GetIsAromatic())
    return aromatic / mol.GetNumAtoms()

print("芳香原子占比：", round(aromatic_fraction(mol), 3))

# 例：找所有碳的杂化类型分布
from collections import Counter
hyb = Counter(str(a.GetHybridization()) for a in mol.GetAtoms())
print("杂化分布：", dict(hyb))

# ============================================================
# 五、批量计算描述符（构建数据集）
# ============================================================
# 把一批分子转成"描述符表格"（QSAR 数据准备的核心）
compounds = {
    "阿司匹林": "CC(=O)Oc1ccccc1C(=O)O",
    "对乙酰氨基酚": "CC(=O)Nc1ccc(O)cc1",
    "布洛芬": "CC(C)Cc1ccc(cc1)C(C)C(=O)O",
    "二甲双胍": "CN(C)C(=N)NC(=N)N",
    "咖啡因": "Cn1cnc2c1c(=O)n(C)c(=O)n2C",
}

print("\n化合物 | MW | LogP | HBD | HBA | TPSA | 环数")
print("-" * 55)
for name, smi in compounds.items():
    m = Chem.MolFromSmiles(smi)
    row = [
        f"{Descriptors.MolWt(m):.1f}",
        f"{Descriptors.MolLogP(m):.2f}",
        f"{Descriptors.NumHDonors(m)}",
        f"{Descriptors.NumHAcceptors(m)}",
        f"{Descriptors.TPSA(m):.1f}",
        f"{desc.CalcNumRings(m)}",
    ]
    print(f"{name}: {' | '.join(row)}")

# 这就是"分子描述符矩阵"——之后机器学习的输入特征！
# 每行 = 一个分子，每列 = 一个性质

# ============================================================
# 六、描述符在 QSAR 中的角色
# ============================================================
# QSAR（定量构效关系）= 分子描述符 → 预测活性/毒性
#   1. 一组已知活性的分子
#   2. 用 RDKit 算描述符 → 特征矩阵
#   3. 活性值（IC50、pIC50等）→ 标签
#   4. sklearn 训练回归/分类模型
#   5. 新分子算描述符 → 预测活性
#
# 你在第21章学的 scipy/第34章将学的 sklearn，就在这里用上
