# ============================================================
# RDKit 化学信息学 ④ — 子结构搜索
# ============================================================
# 子结构搜索 = 检查"一个分子里是否包含某个片段"。
# 应用：找含特定药效团的化合物、查某类官能团、虚拟筛选。

from rdkit import Chem

# ============================================================
# 一、基本用法
# ============================================================
# 大分子（母体）
mol = Chem.MolFromSmiles("CC(=O)Nc1ccc(O)cc1")    # 对乙酰氨基酚

# 要搜的子结构（片段）
sub = Chem.MolFromSmiles("c1ccccc1")              # 苯环

# 检查是否包含
print(mol.HasSubstructMatch(sub))    # → True（有苯环）

# 找到所有匹配位置
matches = mol.GetSubstructMatches(sub)
print("匹配次数：", len(matches))     # → 1
print("匹配的原子：", matches)        # → ((3, 4, 5, 6, 7, 8),)（苯环的6个原子）

# ============================================================
# 二、用 SMARTS 搜索"某类官能团"
# ============================================================
# 搜羟基 -OH
oh = Chem.MolFromSmarts("[OX2H]")       # 2价的氧带1个氢
print("羟基个数：", len(mol.GetSubstructMatches(oh)))    # → 1

# 搜羰基 C=O
carbonyl = Chem.MolFromSmarts("[CX3]=[OX1]")
print("羰基个数：", len(mol.GetSubstructMatches(carbonyl)))  # → 1

# 搜酰胺键（肽键核心！）
amide = Chem.MolFromSmarts("C(=O)N")
print("酰胺键：", len(mol.GetSubstructMatches(amide)))   # → 1

# 搜硝基
nitro = Chem.MolFromSmarts("[NX3](=O)=O")
# 搜羧酸
carboxyl = Chem.MolFromSmarts("C(=O)[OH]")

# 常用药效团 SMARTS：
#   羟基       [OX2H]
#   羰基       [CX3]=[OX1]
#   羧酸       C(=O)[OH]
#   氨基       [NX3;H2,H1,H0;!$(NC=O)]
#   苯环       c1ccccc1
#   杂环       [n,s,o]
#   卤素       [F,Cl,Br,I]

# ============================================================
# 三、芳香性搜索的坑（重要！）
# ============================================================
# 苯环的两种 SMILES 写法：
mol = Chem.MolFromSmiles("c1ccccc1")       # 芳香写法（小写c）
mol2 = Chem.MolFromSmiles("C1=CC=CC=C1")   # 凯库勒写法（大写C+双键）

# 两者是同一个分子吗？
print(Chem.MolToSmiles(mol))    # → c1ccccc1
print(Chem.MolToSmiles(mol2))   # → c1ccccc1（RDKit会统一成芳香写法）

# 但用 SMARTS 搜苯环时，写法不同可能匹配不上！
benzene_aromatic = Chem.MolFromSmarts("c1ccccc1")     # 芳香苯
benzene_kekule  = Chem.MolFromSmarts("C1=CC=CC=C1")   # 凯库勒苯
print(mol.HasSubstructMatch(benzene_aromatic))   # → True
print(mol.HasSubstructMatch(benzene_kekule))     # → 可能 False！
# 经验：子结构搜索统一用芳香写法（小写），最稳妥

# ============================================================
# 四、精确匹配 vs 子结构
# ============================================================
mol = Chem.MolFromSmiles("CCO")    # 乙醇

# 子结构匹配：乙醇包含"CC"吗？（包含关系）
print(mol.HasSubstructMatch(Chem.MolFromSmiles("CC")))   # → True

# 精确匹配：完全一样才 True
# 用 isIsomorphic（同构）
mol2 = Chem.MolFromSmiles("OCC")   # 乙醇的另一种写法
print(Chem.MolToSmiles(mol) == Chem.MolToSmiles(mol2))  # → True（规范后一样）

# 判断两个分子是否同一个（同构）
from rdkit.Chem import rdMolDescriptors
# 更严谨：Chem.MolFromSmiles 规范化后比较 SMILES

# ============================================================
# 五、批量搜索（虚拟筛选雏形）
# ============================================================
# 一批化合物，找出所有含苯环+羧基的（有做药的"药味"）
compounds = [
    "c1ccccc1C(=O)O",        # 苯甲酸 ✓
    "CCCC",                  # 丁烷 ✗
    "c1ccccc1N",             # 苯胺（有苯环无羧基）✗
    "COc1ccc(C(=O)O)cc1",    # 对甲氧基苯甲酸 ✓
    "C1CCC1",                # 环丁烷 ✗
]

benzene = Chem.MolFromSmarts("c1ccccc1")
carboxyl = Chem.MolFromSmarts("C(=O)[OH]")

for s in compounds:
    mol = Chem.MolFromSmiles(s)
    has_benzene = mol.HasSubstructMatch(benzene)
    has_carboxyl = mol.HasSubstructMatch(carboxyl)
    mark = "✓" if (has_benzene and has_carboxyl) else "✗"
    print(f"{mark} {s}: 苯环={has_benzene}, 羧基={has_carboxyl}")

# ============================================================
# 六、药效团概念
# ============================================================
# 药效团 = 药物分子中"起作用的关键片段组合"
# 例如：非甾体抗炎药（NSAIDs）几乎都含"羧基 + 芳香环"
# 用 RDKit 搜索"含有某药效团的分子"就是虚拟筛选的第一步：
#   已知活性分子 → 提炼药效团 → 在大数据库里搜含该片段的分子
#
# 典型流程：
#   1. 从已知活性药提炼关键 SMARTS
#   2. 用 RDKit 遍历数据库（几万~几百万分子）
#   3. 找出含目标片段的候选化合物
#   4. 后续用对接/活性测试验证
