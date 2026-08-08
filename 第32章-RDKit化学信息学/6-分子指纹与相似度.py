# ============================================================
# RDKit 化学信息学 ⑥ — 分子指纹与相似度
# ============================================================
# 分子指纹 = 把分子编码成一串"0/1"或数字，方便比较相似度。
# 相似度是虚拟筛选的核心：
#   "找到和已知活性分子结构相似的化合物"。

from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.DataStructs import TanimotoSimilarity

# ============================================================
# 一、Morgan 指纹（圆形指纹，最常用）
# ============================================================
mol = Chem.MolFromSmiles("c1ccccc1")    # 苯
fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius=2)
# radius=2 表示"看原子周围2个键的范围"（ECFP4）

print(type(fp))               # 位向量
print("指纹位数：", fp.GetNumBits())   # 2048
# 每个分子 → 2048 位的 0/1 串，标记"有哪些局部结构片段"

# 两个分子指纹
benzene = Chem.MolFromSmiles("c1ccccc1")
phenol  = Chem.MolFromSmiles("c1ccccc1O")
toluene = Chem.MolFromSmiles("Cc1ccccc1")
hexane  = Chem.MolFromSmiles("CCCCCC")

fp_benzene = AllChem.GetMorganFingerprintAsBitVect(benzene, 2)
fp_phenol  = AllChem.GetMorganFingerprintAsBitVect(phenol, 2)
fp_toluene = AllChem.GetMorganFingerprintAsBitVect(toluene, 2)
fp_hexane  = AllChem.GetMorganFingerprintAsBitVect(hexane, 2)

# ============================================================
# 二、Tanimoto 相似度（0~1）
# ============================================================
# Tanimoto = 公共片段数 / 总片段数
# 1 = 完全相同，0 = 完全不同
sim_benzene_phenol = TanimotoSimilarity(fp_benzene, fp_phenol)
sim_benzene_toluene = TanimotoSimilarity(fp_benzene, fp_toluene)
sim_benzene_hexane = TanimotoSimilarity(fp_benzene, fp_hexane)

print(f"苯 vs 苯酚:   {sim_benzene_phenol:.3f}")    # ~0.6（有共同苯环）
print(f"苯 vs 甲苯:   {sim_benzene_toluene:.3f}")   # ~0.6
print(f"苯 vs 己烷:   {sim_benzene_hexane:.3f}")    # ~0.1（完全不同）
# 直观验证：苯酚/甲苯和苯相似度高，己烷（烷烃）相似度低

# 相似度经验阈值：
#   > 0.85   很可能有相似活性
#   0.7~0.85 可能相似
#   < 0.4    基本不相似

# ============================================================
# 三、常见指纹类型
# ============================================================
# Morgan/ECFP4：圆形指纹（默认 radius=2），药化最常用
# Morgan radius=3（ECFP6）：范围更大
# MACCS keys：166 位结构键（经典，看有没有特定子结构）
# RDKit fingerprint：路径指纹
# Topological torsion：拓扑扭转指纹

# MACCS 例子：
from rdkit.Chem import MACCSkeys
maccs = MACCSkeys.GenMACCSKeys(mol)
print("MACCS 位数：", maccs.GetNumBits())   # 166

# 不同指纹算出的相似度不同，选哪种看应用场景

# ============================================================
# 四、批量相似度筛选（虚拟筛选雏形）
# ============================================================
# 场景：以"布洛芬"为先导物，从化合物库找相似分子
query_smiles = "CC(C)Cc1ccc(cc1)C(C)C(=O)O"     # 布洛芬
query = Chem.MolFromSmiles(query_smiles)
query_fp = AllChem.GetMorganFingerprintAsBitVect(query, 2)

library = [
    ("阿司匹林", "CC(=O)Oc1ccccc1C(=O)O"),
    ("对乙酰氨基酚", "CC(=O)Nc1ccc(O)cc1"),
    ("萘普生", "COc1ccc2cc(ccc2c1)C(C)C(=O)O"),      # 结构类似！
    ("酮洛芬", "CC(C(=O)O)c1ccccc1C(=O)c1ccccc1"),   # 结构类似！
    ("二甲双胍", "CN(C)C(=N)NC(=N)N"),
    ("咖啡因", "Cn1cnc2c1c(=O)n(C)c(=O)n2C"),
]

print("\n以布洛芬为模板的相似度排序：")
results = []
for name, smi in library:
    m = Chem.MolFromSmiles(smi)
    fp = AllChem.GetMorganFingerprintAsBitVect(m, 2)
    sim = TanimotoSimilarity(query_fp, fp)
    results.append((sim, name))

for sim, name in sorted(results, reverse=True):
    print(f"  {name}: {sim:.3f}")
# 预期：萘普生/酮洛芬（同为NSAIDs）相似度最高
# 这就是"相似结构 → 可能相似活性"的筛选逻辑

# ============================================================
# 五、指纹可视化（理解它在算什么）
# ============================================================
# 指纹本质：把分子"切成局部片段"，看有没有某个片段
# 苯酚的 ECFP4 大致包含：
#   苯环片段、羟基片段、苯环-羟基组合片段
# 己烷只有：各种长度的烷链片段 → 和苯没有共同片段 → 相似度低

# 指纹设置注意事项：
# 1. 指纹位数（2048默认）越大越精确但越慢
# 2. radius 越大看的环境越远（2=ECFP4, 3=ECFP6）
# 3. 同一套筛选要统一参数，否则没可比性

# ============================================================
# 六、完整虚拟筛选流程（概念）
# ============================================================
# 1. 准备：活性分子的 SMILES（模板）
# 2. 计算：模板指纹
# 3. 遍历库：每个化合物算指纹，算 Tanimoto
# 4. 排序：相似度 > 0.7 的进入候选
# 5. 验证：候选做对接/实验
#
# 这是"基于配体的虚拟筛选"（Ligand-Based Virtual Screening）的最简实现，
# 是药化科研的常用起点。

# ============================================================
# 七、练习
# ============================================================
# 1. 用5个你认识的药，两两算 Tanimoto，看哪个最像
# 2. 对比 ECFP4 vs ECFP6 的相似度差异
# 3. 思考：为什么结构相似不一定活性相似？（可能有生物等排体等）

# ============================================================
# 六、易错点汇总
# ============================================================
# 1. 分子指纹 = 把分子结构编码成 0/1 位串，
#    用于相似度比较和机器学习特征
# 2. Morgan 指纹：GetMorganFingerprintAsBitVect；
#    参数 radius（半径）影响精度
# 3. 相似度常用 Tanimoto 系数（0~1，越近 1 越相似）
# 4. 指纹要转成 numpy 数组才能喂给 sklearn
# 5. 结构相似 ≠ 活性相似（等排体、不同结合方式）——
#    相似度只是启发式，不是结论
# 6. 指纹维度高，配合降维/稀疏表示使用

# ============================================================
# 七、自测（40%基础 + 40%中等 + 20%挑战）
# ============================================================
# 【基础】
# 1. 分子指纹是什么？有什么用？
# 2. Tanimoto 相似度的范围？
# 3. 指纹为什么要转成 numpy 数组？
#
# 【中等】
# 4. 计算两个药物的 Morgan 指纹。
# 5. 计算它们的 Tanimoto 相似度。
# 6. 把一批分子算成指纹矩阵。
#
# 【挑战】
# 7. 做相似性检索：找与某药物最相似的化合物。
# 8. 解释为什么结构相似不一定活性相似。
