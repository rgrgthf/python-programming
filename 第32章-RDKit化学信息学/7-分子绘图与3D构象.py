# ============================================================
# RDKit 化学信息学 ⑦ — 分子绘图与3D构象
# ============================================================
# 把分子画出来（论文插图、课件展示）+ 生成3D构象（对接准备）。

from rdkit import Chem
from rdkit.Chem import Draw

# ============================================================
# 一、画单个分子（2D结构式）
# ============================================================
mol = Chem.MolFromSmiles("CC(=O)Oc1ccccc1C(=O)O")   # 阿司匹林

# 生成图片（显示/保存）
img = Draw.MolToImage(mol, size=(400, 300))
# 在 Jupyter 里直接显示；脚本里保存：
img.save("aspirin.png")
# 或在终端脚本用：Draw.MolToFile(mol, "aspirin.png")

# 画网格图（多个分子一起，论文常用）
mols = [Chem.MolFromSmiles(s) for s in [
    "CC(=O)Oc1ccccc1C(=O)O",     # 阿司匹林
    "CC(C)Cc1ccc(cc1)C(C)C(=O)O",# 布洛芬
    "COc1ccc2cc(ccc2c1)C(C)C(=O)O", # 萘普生
    "CN1CCC23C4C1CC5=C2C(=C(C=C5)O)OC3C(C=C4)O", # 吗啡
]]
# 过滤 None
mols = [m for m in mols if m is not None]
img_grid = Draw.MolsToGridImage(mols, molsPerRow=2, subImgSize=(300, 220))
img_grid.save("drugs_grid.png")
print("已保存 drugs_grid.png（2x2 分子网格图）")

# 标注原子序号/属性
img2 = Draw.MolToImage(mol, size=(400, 300), highlightAtoms=[2, 3])
img2.save("aspirin_highlight.png")

# 突出显示子结构匹配（论文常用！）
benzene = Chem.MolFromSmarts("c1ccccc1")
match = mol.GetSubstructMatch(benzene)   # 苯环的原子
img3 = Draw.MolToImage(mol, size=(400, 300), highlightAtoms=match)
img3.save("aspirin_ring.png")
print("苯环已高亮保存")

# ============================================================
# 二、中文显示问题（Windows）
# ============================================================
# RDKit 默认字体可能不支持中文，分子名字建议用英文或不显示
# 或者手动加图例（在网格图下用 subImgSize 控制）
# 一般论文用英文名即可

# ============================================================
# 三、3D 构象生成（对接/构象分析前必做）
# ============================================================
from rdkit.Chem import AllChem

mol3d = Chem.MolFromSmiles("CC(=O)Oc1ccccc1C(=O)O")
mol3d = Chem.AddHs(mol3d)          # 先加氢（3D必须！）

# 生成3D坐标（用ETKDG方法，推荐）
result = AllChem.EmbedMolecule(mol3d, randomSeed=42)
# 返回 0 = 成功
print("3D嵌入结果：", result)

# 优化构象（MMFF力场，让结构合理）
AllChem.MMFFOptimizeMolecule(mol3d)
print("原子数（含H）：", mol3d.GetNumAtoms())

# 保存为 mol 文件（带3D坐标，可导入其他软件）
Chem.MolToMolFile(mol3d, "aspirin_3d.mol")

# 生成多个构象（构象搜索，对接用）
confs = AllChem.EmbedMultipleConfs(mol3d, numConfs=10, randomSeed=42)
print("生成了", len(confs), "个构象")

# ============================================================
# 四、3D 相关计算
# ============================================================
# 3D 描述符（需要先有构象）
from rdkit.Chem import rdMolDescriptors

# 分子体积/表面积（近似）
print("近似表面积(Å²)：", rdMolDescriptors.CalcLabuteASA(mol3d))

# 分子形状（PBF等）后续在对接里更常用

# 计算两分子叠合（形状比较，进阶）：
# 需要 rdShapeAlign / rdMolAlign，后面机器学习章节再展开

# ============================================================
# 五、常见文件格式导出
# ============================================================
# SDF（含属性，药物数据库标准）
from rdkit.Chem import rdMolDescriptors as desc
w = Chem.SDWriter("compounds.sdf")
for m in mols:
    m.SetProp("_Name", Chem.MolToSmiles(m))     # 存名字/ID
    m.SetProp("MW", str(round(desc.CalcExactMolWt(m), 2)))  # 存属性
    w.write(m)
w.close()
print("已保存 compounds.sdf（含分子量属性）")

# SMILES 文件
with open("smiles.txt", "w") as f:
    for m in mols:
        f.write(Chem.MolToSmiles(m) + "\n")

# ============================================================
# 六、3D 对接前的准备工作清单
# ============================================================
# 1. SMILES → 加氢 → EmbedMolecule 生成3D
# 2. MMFF 优化构象
# 3. 保存 .mol/.sdf（带坐标）
# 4. （对接软件：Autodock Vina 等）读入蛋白+配体
# 5. 打分 → 排序候选分子
#
# 这是分子对接（Docking）的标准起点，等你学了对接工具就能衔接

# ============================================================
# 七、练习
# ============================================================
# 1. 选3个药画网格图，突出显示它们的苯环
# 2. 生成咖啡因的3D构象并保存 .mol
# 3. 把一批分子写进 SDF，附加分子量/LogP属性
