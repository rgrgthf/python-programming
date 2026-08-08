# ============================================================
# RDKit 化学信息学 ② — 创建、读取与检查分子
# ============================================================
# 深入 RDKit 的分子对象：从 SMILES/文件创建，检查合法性，
# 处理"坏分子"和立体化学。

from rdkit import Chem

# ============================================================
# 一、从 SMILES 创建分子
# ============================================================
# 合法 SMILES
mol = Chem.MolFromSmiles("c1ccccc1")    # 苯
print("苯：", mol is not None)          # → True

# 非法 SMILES → 返回 None（不报错！）
bad = Chem.MolFromSmiles("CCCCCCCCCCC[C")   # 缺括号
print("坏SMILES：", bad)                # → None

# ⚠️ 常见坑：MolFromSmiles 失败时返回 None 而不是报异常！
# 批量处理时一定要检查是否为 None，否则后面调用会崩溃
mols_list = ["c1ccccc1", "CCO", "invalid!!", "CC(=O)O"]
for s in mols_list:
    m = Chem.MolFromSmiles(s)
    if m is not None:
        print(f"✓ {s} → {Chem.MolToSmiles(m)}")
    else:
        print(f"✗ {s} → 解析失败")

# ============================================================
# 二、分子合法性检查（重要！）
# ============================================================
# 有些 SMILES 能解析，但化学上不合理（价键问题等）
mol = Chem.MolFromSmiles("C")
print(Chem.SanitizeMol(mol))     # → 0 表示合法（原子价正常）
# 返回值：0 = 合法，其他值 = 问题代码

# 更安全的检查方式：
def check_mol(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "SMILES解析失败"
    try:
        Chem.SanitizeMol(mol)     # 化学合理性检查
        return True, "合法"
    except Exception as e:
        return False, str(e)

print(check_mol("c1ccccc1"))   # → (True, '合法')
print(check_mol("C"))          # → (True, '合法')（甲烷）
# 某些"价键怪异"的分子会在这里被拦下

# ============================================================
# 三、分子信息提取
# ============================================================
from rdkit.Chem import rdMolDescriptors as desc

mol = Chem.MolFromSmiles("CC(=O)Nc1ccc(O)cc1")   # 对乙酰氨基酚

# 原子信息
print("原子数：", mol.GetNumAtoms())
print("重原子数（非氢）：", mol.GetNumHeavyAtoms())   # 12
print("键数：", mol.GetNumBonds())
print("环数：", desc.CalcNumRings(mol))
print("芳香环数：", desc.CalcNumAromaticRings(mol))

# 化学式/分子量
print("化学式：", desc.CalcMolFormula(mol))       # C8H9NO2
print("精确质量：", desc.CalcExactMolWt(mol))     # 151.0633
print("平均分子量：", desc.CalcMolWt(mol))        # 151.1626

# ============================================================
# 四、氢原子处理（重要概念）
# ============================================================
mol = Chem.MolFromSmiles("CCO")   # 乙醇

# 默认不含氢（隐式氢）
print("显式原子数：", mol.GetNumAtoms())    # → 3（C C O）

# 加上氢之后
mol_h = Chem.AddHs(mol)
print("加氢后原子数：", mol_h.GetNumAtoms())  # → 9（C2H5OH 共9个原子）

# 反过来
mol2 = Chem.RemoveHs(mol_h)
print("去氢后：", mol2.GetNumAtoms())        # → 3

# 什么时候要加氢？
#   - 3D构象生成前必须加氢
#   - 计算某些描述符需要
#   - 分子对接前
# 什么时候不要？
#   - 子结构搜索（氢会干扰匹配）
#   - 大部分 2D 计算

# ============================================================
# 五、立体化学（手性）
# ============================================================
# @ 和 @@ 表示手性中心的立体构型
mol = Chem.MolFromSmiles("N[C@@H](C)C(=O)O")   # 丙氨酸（L型）

# 检查手性中心
from rdkit.Chem import rdchem
chiral_centers = Chem.FindMolChiralCenters(mol)
print("手性中心：", chiral_centers)
# → [(1, 'S')] 或 [(1, 'R')]（原子1是手性中心，S/R构型）

# 药学意义：对映异构体药理活性可能完全不同！
# 沙利度胺：R型镇静，S型致畸（著名的"反应停"事件）
# 所以药物开发要区分手性

# ============================================================
# 六、从其他格式创建分子
# ============================================================
# 从 InChI
inchi = "InChI=1S/C8H9NO2/c1-6(10)9-7-2-4-8(11)5-3-7/h2-5,11H,1H3,(H,9,10)"
mol = Chem.MolFromInchi(inchi)
print("InChI→SMILES：", Chem.MolToSmiles(mol))

# 从 MolBlock（.mol 文件内容）
molblock = """ethanol
  RDKit          2D

  9  8  0  0  0  0  0  0  0  0999 V2000
...
"""
# mol = Chem.MolFromMolBlock(molblock)

# 从序列（多肽/核酸）
# from rdkit.Chem import rdMolDescriptors
# 多肽：Chem.MolFromSequence("ACDE")（氨基酸单字母）
# 核酸：Chem.MolFromSequence("ATCG", flavor=1)

# ============================================================
# 七、练习
# ============================================================
# 1. 写出你专业里熟悉的药物 SMILES，解析并打印分子量/化学式
# 2. 检查：同一个分子用不同 SMILES 写法，规范后是否一致
# 3. 找一个手性药物，看它的手性中心是 R 还是 S

# ============================================================
# 六、易错点汇总
# ============================================================
# 1. RDKit 的 Mol 对象【不可变】：想改结构要复制或重建，
#    别直接改原子属性
# 2. 用 Chem.MolFromSmiles 创建；
#    检查分子用 mol.GetNumAtoms()/GetNumBonds()
# 3. 手性中心要检查立体化学：mol.GetAtomWithIdx(i).GetChiralTag()
# 4. 原子索引从 0 开始，遍历用 mol.GetAtoms()
# 5. 元素/杂化/形式电荷都从原子对象取
# 6. 大分子（蛋白）用别的工具，RDKit 主要面向小分子药物

# ============================================================
# 七、自测（40%基础 + 40%中等 + 20%挑战）
# ============================================================
# 【基础】
# 1. RDKit 的 Mol 对象可修改吗？
# 2. 怎么统计一个分子的原子数和键数？
# 3. 原子索引从几开始？
#
# 【中等】
# 4. 创建布洛芬分子，打印原子数、分子式。
# 5. 遍历所有原子，打印元素符号。
# 6. 检查某个手性中心是 R 还是 S。
#
# 【挑战】
# 7. 写一个分子分析函数：输入 SMILES，输出原子/键/分子式。
# 8. 解释 RDKit 主要面向哪类分子，为什么。
