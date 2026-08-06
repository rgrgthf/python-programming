# ============================================================
# 第十三章 阶段测试 — RDKit 化学信息学
# ============================================================
# 共 10 题：读代码、简答、编程（sci 环境，需 rdkit）
# ============================================================
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors
from rdkit.Chem import rdMolDescriptors as desc
from rdkit.DataStructs import TanimotoSimilarity

# ========== 一、SMILES 与分子创建 ==========

# 1.【读代码】写出输出：
mol = Chem.MolFromSmiles("CCO")
print(Chem.MolToSmiles(mol))
print(mol.GetNumAtoms())
print(Chem.MolToSmiles(Chem.MolFromSmiles("OCC")))
# 你的答案：


# 2.【简答】MolFromSmiles 遇到非法 SMILES 会返回什么？
#     批量处理时为什么要检查它是否为 None？
# 你的答案：


# 3.【读代码】写出输出：
mol = Chem.MolFromSmiles("c1ccccc1O")
print(desc.CalcMolFormula(mol))
print(desc.CalcNumRings(mol))
print(desc.CalcNumAromaticRings(mol))
# 你的答案：


# ========== 二、原子与子结构 ==========

# 4.【编程】分析对乙酰氨基酚 CC(=O)Nc1ccc(O)cc1：
#     打印原子数、化学式、是否有苯环、羟基个数（SMARTS [OX2H]）。
print("第4题（你的代码）：")
# 你的代码：


# 5.【简答】芳香性搜索的坑：为什么搜苯环要用小写 c 的 SMARTS？
# 你的答案：


# ========== 三、描述符 ==========

# 6.【编程】计算布洛芬的 MW、LogP、HBD、HBA、TPSA，
#     判断它是否满足类药五规则（MW<500, LogP<5, HBD≤5, HBA≤10）。
print("第6题（你的代码）：")
# 你的代码：


# ========== 四、指纹与相似度 ==========

# 7.【读代码】写出输出（相似度排序概念）：
benzene = Chem.MolFromSmiles("c1ccccc1")
toluene = Chem.MolFromSmiles("Cc1ccccc1")
hexane = Chem.MolFromSmiles("CCCCCC")
fp1 = AllChem.GetMorganFingerprintAsBitVect(benzene, 2)
fp2 = AllChem.GetMorganFingerprintAsBitVect(toluene, 2)
fp3 = AllChem.GetMorganFingerprintAsBitVect(hexane, 2)
print(round(TanimotoSimilarity(fp1, fp2), 2))
print(round(TanimotoSimilarity(fp1, fp3), 2))
# 你的答案：


# 8.【简答】Tanimoto 相似度 0~1 分别代表什么？虚拟筛选中阈值一般取多少？
# 你的答案：


# ========== 五、综合实战 ==========

# 9.【编程】以阿司匹林为模板，从下面化合物中选出相似度最高的2个：
#    "CC(C)Cc1ccc(cc1)C(C)C(=O)O"  布洛芬
#    "CCCCCCCC"                    辛烷
#    "COc1ccc2cc(ccc2c1)C(C)C(=O)O" 萘普生
#    "Cn1cnc2c1c(=O)n(C)c(=O)n2C"  咖啡因
print("第9题（你的代码）：")
# 你的代码：


# 10.【综合编程】写一个函数 analyze_drug(smiles)：
#    返回该分子的 化学式、分子量、LogP、环数、是否含苯环 的汇总，
#    并打印"该分子是否类药"（五规则）。
#    用阿司匹林测试。
print("第10题（你的代码）：")
# 你的代码：
