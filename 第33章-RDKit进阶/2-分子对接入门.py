# ============================================================
# RDKit 进阶 ② — 分子对接入门
# ============================================================
# 分子对接 = 预测"小分子（配体）如何与蛋白（受体）结合"。
# 这是药物发现的经典手段：评估候选药能否结合到靶点。
# 常用软件：AutoDock Vina（免费开源，命令行）。

# ============================================================
# 一、对接概念
# ============================================================
# 锁钥模型：
#   蛋白 = 锁（受体 receptor），药 = 钥匙（配体 ligand）
# 对接 = 找"钥匙怎么插进锁里最合适"
#
# 输出：结合能（binding affinity），越负代表结合越强
#   结合能 < -7 kcal/mol → 结合较好（初步筛选中可关注）
#   < -9 kcal/mol → 很强

# ============================================================
# 二、对接前的准备（RDKit 负责配体部分）
# ============================================================
from rdkit import Chem
from rdkit.Chem import AllChem

def prepare_ligand(smiles, out_pdbqt="ligand.pdbqt"):
    """配体准备：SMILES → 3D → 优化 → 转PDBQT（对接格式）"""
    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol, randomSeed=42)
    AllChem.MMFFOptimizeMolecule(mol)
    # 旋转键定义（Vina需要知道哪些键可以转）
    AllChem.SetBondTorsionDefinitions? if False else None
    # 实际对接会用 MGLTools / openbabel 转 PDBQT
    print(f"配体准备完成：{smiles}")
    print(f"原子数（含H）：{mol.GetNumAtoms()}")
    return mol

# 例子：准备阿司匹林
prepare_ligand("CC(=O)Oc1ccccc1C(=O)O")

# ============================================================
# 三、AutoDock Vina 工作流程（命令行）
# ============================================================
# ① 安装（Windows 用 conda 最简单）：
#   conda activate sci
#   conda install -c conda-forge autodock-vina

# ② 准备蛋白：
#   从 PDB 数据库下载蛋白结构（如 PDB 1BNA）
#   处理：去水、加氢、转PDBQT（用 ADFRsuite / MGLTools）

# ③ 准备配体：
#   RDKit 生成3D → openbabel 转 PDBQT

# ④ 指定对接盒子（grid box，蛋白上的结合区域）：
#   配置文件 config.txt：
#   receptor = protein.pdbqt
#   ligand   = ligand.pdbqt
#   center_x = 15.0   # 盒子中心坐标
#   center_y = 20.0
#   center_z = 10.0
#   size_x = 20       # 盒子大小
#   size_y = 20
#   size_z = 20
#   exhaustiveness = 8

# ⑤ 运行：
#   vina --config config.txt --out result.pdbqt

# ⑥ 结果：
#   result.pdbqt 里的 VINA RESULT 行给出结合能
#   -8.5 kcal/mol 表示结合较好

# ============================================================
# 四、RDKit 分析对接结果
# ============================================================
# 对接输出的 PDBQT 含多个构象（pose），RDKit 可读取
# 从 PDBQT 读配体（简化示例）：
# from rdkit.Chem import rdMolTransforms
# mol = Chem.MolFromPDBFile("result.pdbqt", removeHs=False)
# print(Chem.MolToSmiles(mol))

# 计算蛋白-配体相互作用（进阶，需要蛋白结构处理）：
#   氢键、疏水接触、π-π堆积 等
# 常用库：PLIP（Protein-Ligand Interaction Profiler）

# ============================================================
# 五、虚拟筛选 + 对接的完整流程
# ============================================================
# 1. 准备靶点蛋白（下载PDB、处理）
# 2. 准备化合物库（RDKit 批量生成3D）
# 3. 逐个对接（Vina 批量跑）
# 4. 按结合能排序，选前N个
# 5. 分析相互作用（PLIP）
# 6. 实验验证
#
# 这是药化/计算机辅助药物设计（CADD）的核心工作流，
# 你在第16章的综合项目里会完整实践

# ============================================================
# 六、对接相关库推荐（后续按需学）
# ============================================================
#   分子准备：RDKit / openbabel / MGLTools
#   对接：AutoDock Vina / AutoDock4 / LeDock
#   分析：PLIP / PyMOL（可视化）
#   高精度：GOLD / Glide / MOE（商业软件，很多课题组用）
#
# 先从免费的 Vina 学起，够用且发表论文认可度高
