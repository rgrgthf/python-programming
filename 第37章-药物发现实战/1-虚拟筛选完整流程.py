# ============================================================
# 药物发现实战 ① — 虚拟筛选完整流程
# ============================================================
# 把前面所有技能串起来：从活性先导物 → 化合物库筛选 → 候选分子。
# 这是"基于配体的虚拟筛选"（LBVS）的完整实现。

import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors
from rdkit.DataStructs import TanimotoSimilarity

# ============================================================
# 一、先导化合物（已知活性分子）
# ============================================================
# 以布洛芬为先导物（NSAID），找结构相似的候选物
lead_smiles = "CC(C)Cc1ccc(cc1)C(C)C(=O)O"
lead = Chem.MolFromSmiles(lead_smiles)
lead_fp = AllChem.GetMorganFingerprintAsBitVect(lead, radius=2, nBits=2048)

print("先导物：布洛芬")
print("MW:", round(Descriptors.MolWt(lead), 1))
print("LogP:", round(Descriptors.MolLogP(lead), 2))

# ============================================================
# 二、化合物库（模拟从 ZINC/ChEMBL 下载的分子集）
# ============================================================
library = [
    # 已知NSAIDs（应高相似）
    "COc1ccc2cc(ccc2c1)C(C)C(=O)O",          # 萘普生
    "CC(C(=O)O)c1ccccc1C(=O)c1ccccc1",       # 酮洛芬
    "CC(C)Cc1ccc(cc1)C(O)C(=O)O",            # 氟比洛芬类似
    "O=C(O)Cc1ccc2ccccc2c1",                 # 萘普生异构
    # 无关分子（应低相似）
    "CCCC", "CCO", "CCN", "C1CCCCC1",
    "Cn1cnc2c1c(=O)n(C)c(=O)n2C",            # 咖啡因
    "CN(C)C(=N)NC(=N)N",                     # 二甲双胍
    # 其他候选
    "CC(C)Cc1ccc(cc1)C(=O)CO",
    "COc1ccc(cc1)C(C)C(=O)O",
]

# ============================================================
# 三、逐分子算相似度 + 排序
# ============================================================
results = []
for smi in library:
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        continue
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius=2, nBits=2048)
    sim = TanimotoSimilarity(lead_fp, fp)
    results.append((sim, smi, Descriptors.MolWt(mol)))

# 按相似度降序
results.sort(key=lambda x: -x[0])

print("\n===== 相似度排序 =====")
for sim, smi, mw in results:
    print(f"  相似度 {sim:.3f} | MW {mw:6.1f} | {smi}")

# ============================================================
# 四、筛选出候选（相似度阈值 + 类药性过滤）
# ============================================================
threshold = 0.7
candidates = []
for sim, smi, mw in results:
    if sim >= threshold:
        mol = Chem.MolFromSmiles(smi)
        # 类药性检查
        logp = Descriptors.MolLogP(mol)
        if mw < 500 and -2 < logp < 5:
            candidates.append((sim, smi))

print(f"\n===== 筛选结果（相似度≥{threshold} + 类药性）=====")
for sim, smi in candidates:
    print(f"  {sim:.3f}  {smi}")

# ============================================================
# 五、候选分子输出（后续可做对接）
# ============================================================
# 把候选写入 SDF，供下一步对接
from rdkit.Chem import AllChem
w = Chem.SDWriter("candidates.sdf")
for sim, smi in candidates:
    mol = Chem.MolFromSmiles(smi)
    mol.SetProp("_Name", smi)
    mol.SetProp("Similarity", f"{sim:.3f}")
    w.write(mol)
w.close()
print("\n候选已保存 candidates.sdf，可进入分子对接环节")

# ============================================================
# 六、流程总结（虚拟筛选工作流）
# ============================================================
# 1. 已知活性分子 → 计算指纹（模板）
# 2. 化合物库（数千~数百万）→ 逐个算指纹
# 3. Tanimoto 相似度排序
# 4. 阈值过滤（如 0.7）+ 类药性过滤
# 5. 候选 → 分子对接打分（第14章）
# 6. 结合能排序 → 选前N → 实验验证
#
# 这是完整 LBVS 流程的"最小实现"，
# 真实项目用 ZINC 大库 + 对接，思路完全相同

# ============================================================
# 六、易错点汇总
# ============================================================
# 1. 虚拟筛选流程：目标 → 化合物库 → 描述符/对接 → 打分 → 排序
# 2. 化合物库：ZINC 是免费大库（几百万分子）；
#    教学用小型库，思路相同
# 3. 对接打分是近似，筛选出的是"候选"，不是"结论"
# 4. 筛选要分层：先粗筛（快速性质/药效团）再细筛（对接）
# 5. 结果要人工复核（看结构/结合模式合理性）
# 6. 整个过程可复现：记录库、参数、打分函数

# ============================================================
# 七、自测（40%基础 + 40%中等 + 20%挑战）
# ============================================================
# 【基础】
# 1. 虚拟筛选的完整流程？
# 2. ZINC 是什么？
# 3. 对接打分能当作最终结论吗？
#
# 【中等】
# 4. 描述"粗筛→细筛"的分层策略。
# 5. 筛选结果为什么要人工复核？
# 6. 说明可复现性在虚拟筛选里为什么重要。
#
# 【挑战】
# 7. 设计一个小型虚拟筛选流程（含打分排序）。
# 8. 解释为什么真实项目要用 ZINC 大库。
