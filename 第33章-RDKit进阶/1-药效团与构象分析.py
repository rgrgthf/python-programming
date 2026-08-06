# ============================================================
# RDKit 进阶 ① — 药效团、分子对齐与构象分析
# ============================================================
# 虚拟筛选的进阶玩法：药效团模型、分子叠合、构象分析。

from rdkit import Chem
from rdkit.Chem import AllChem, rdMolAlign

# ============================================================
# 一、药效团特征提取
# ============================================================
# 药效团 = 分子中"对活性起关键作用的原子组合"
# 常见药效团特征（feature）：
#   氢键供体（HBD）、氢键受体（HBA）、芳香环、疏水中心、带电基团

from rdkit.Chem.Pharm2D import Generate
from rdkit.Chem import ChemicalFeatures

# 使用 RDKit 内置的特征工厂
from rdkit.Chem import rdMolChemicalFeatures
factory = ChemicalFeatures.BuildFeatureFactory(
    "Data/BaseFeatures.fdef" if False else rdMolChemicalFeatures.BuildFeatureFactory(
        rdMolChemicalFeatures.featureFactoryName  # 简化写法
    ) if False else None
)

# 标准写法：
# from rdkit.Chem import ChemicalFeatures
# factory = ChemicalFeatures.BuildFeatureFactory('BaseFeatures.fdef')
# mol = Chem.MolFromSmiles('CC(=O)Nc1ccc(O)cc1')
# feats = factory.GetFeaturesForMol(mol)
# for f in feats:
#     print(f.GetFamily(), f.GetAtomIds())   # 特征类型 + 涉及的原子

# 特征家族常见：Donor（供体）、Acceptor（受体）、Aromatic（芳香）、Hydrophobe（疏水）

# ============================================================
# 二、分子对齐（叠合）
# ============================================================
# 用途：比较两个分子的3D形状是否相似（形状筛选）
# 需要先有3D构象
def make_3d(smiles):
    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol, randomSeed=42)
    AllChem.MMFFOptimizeMolecule(mol)
    return mol

aspirin = make_3d("CC(=O)Oc1ccccc1C(=O)O")
ibuprofen = make_3d("CC(C)Cc1ccc(cc1)C(C)C(=O)O")

# 形状相似度（shape similarity）
from rdkit.Chem import rdShapeHelpers
from rdkit.Chem.rdMolAlign import CalcShapeTanimoto
# 简化的形状对比：
# sim = rdShapeHelpers.ShapeTanimotoDist(aspirin, ibuprofen)
# 不同方法：

# 基于分子的叠合（对齐两个分子）
# rmsd = rdMolAlign.AlignMol(aspirin, ibuprofen)
# print("RMSD（均方根偏差）：", rmsd)   # 越小越相似
# RMSD < 1.0 Å 通常认为叠合很好

# ============================================================
# 三、构象分析（柔性分子）
# ============================================================
# 同一分子可以有多种3D构象（旋转键的不同扭转）
mol = Chem.MolFromSmiles("CCCCCC")     # 正己烷（可旋转键多）
mol = Chem.AddHs(mol)

# 生成50个构象
cids = AllChem.EmbedMultipleConfs(mol, numConfs=50, randomSeed=42)
print("生成了", len(cids), "个构象")

# 计算每个构象的能量（构象能量排序 → 找低能构象）
energies = []
for cid in cids:
    ff = AllChem.MMFFGetMoleculeForceField(mol, mmffVariant='MMFF94s')
    e = ff.CalcEnergy()
    energies.append(e)

# 按能量排序
sorted_idx = sorted(range(len(energies)), key=lambda i: energies[i])
print("最低能量构象：", sorted_idx[0], "能量", round(energies[sorted_idx[0]], 2))
# 低能构象更可能是分子真实存在的形状（Boltzmann分布）

# 构象间 RMSD（两两对比）
rmsd_matrix = AllChem.GetConformerRMSMatrix(mol)
print("构象差异矩阵形状：", rmsd_matrix.shape)

# ============================================================
# 四、药理应用场景
# ============================================================
# 1. 构象分析：多肽/药物的活性构象搜索
# 2. 药效团筛选：从活性分子提取特征 → 搜数据库
# 3. 形状筛选：以已知活性分子3D形状为模板，找形状相似的新分子
# 4. 分子叠合：比较先导物与候选物
#
# 完整药效团工具推荐（进阶）：Pharmit、PharmMapper（在线服务）

# ============================================================
# 五、RMSD 的意义
# ============================================================
# RMSD = 两个结构对应原子的均方根位移
#   越小 → 结构越接近
#   对接中常用于评估"预测构象 vs 实验构象"的偏差
#   < 2 Å 通常认为对接结果可接受
