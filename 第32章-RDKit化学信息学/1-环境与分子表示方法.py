# ============================================================
# RDKit 化学信息学 ① — 环境与分子表示方法
# ============================================================
# RDKit = 化学信息学最强大的 Python 库（制药行业标准）。
# 你能用它：读分子结构、算性质、搜索子结构、算相似度、画分子。
# 你的 sci 环境已装好 rdkit 2026.03.4。

# ============================================================
# 一、环境确认
# ============================================================
# 使用前确认用的是 sci 环境（VS Code 右下角切换）
import rdkit
print(rdkit.__version__)   # → 2026.03.4

# 如果没有：
#   conda activate sci
#   conda install rdkit -c conda-forge

# ============================================================
# 二、分子怎么在电脑里表示？（关键概念）
# ============================================================
# 化学家看分子：结构式（球棍/线式）
# 电脑里常用的分子表示方法：

# ① SMILES（最常用）
#    用一串 ASCII 字符描述分子
#    阿司匹林：CC(=O)Oc1ccccc1C(=O)O
#    乙醇：    CCO
#    苯：      c1ccccc1
#
#    规则速记：
#      大写字母 = 原子（C 碳，N 氮，O 氧，S 硫，P 磷）
#      小写 c/n/o = 芳香原子
#      = 双键， # 三键
#      ( ) = 分支
#      数字 = 成环的位置标记
#      [Na+] = 离子
#      * = 任意原子

# ② InChI（国际化学标识，用于数据库/去重）
#    阿司匹林的 InChI 很长，适合计算机存储和比对

# ③ CAS 号（化学文摘社编号）
#    阿司匹林 CAS：50-78-2（一个化合物一个号）

# ④ 分子结构文件（.mol / .sdf）
#    包含完整三维坐标的文件，常用于对接、构象分析

# ============================================================
# 三、为什么学 RDKit？
# ============================================================
# 药学研究的常见任务，RDKit 都能做：
#   1. 解析/生成 SMILES（分子进出计算机的大门）
#   2. 计算分子性质（分子量、LogP、极性表面积）
#   3. 子结构搜索（找含某个药效团的化合物）
#   4. 分子相似度（虚拟筛选：找和先导物相似的分子）
#   5. 分子画图（论文插图）
#   6. 生成描述符 → 喂给机器学习（QSAR）
#
# 这是"药学 + AI"结合的桥梁：RDKit 生成分子特征，ML 做预测。

# ============================================================
# 四、RDKit 的分子对象
# ============================================================
from rdkit import Chem

# SMILES → 分子对象
mol = Chem.MolFromSmiles("CCO")      # 乙醇
print(type(mol))                     # <class 'rdkit.Chem.rdchem.Mol'>

# 分子对象 → SMILES（规范化）
print(Chem.MolToSmiles(mol))         # → CCO
# 注意：SMILES 有无数种写法，RDKit 会输出"规范SMILES"

# 从名称查 SMILES（需要 PubChem 数据库，联网）
# from rdkit import Chem
# from rdkit.Chem import rdMolDescriptors
# 通常配合 pubchempy 或数据库用，先不展开

# ============================================================
# 五、一个分子对象里有什么？
# ============================================================
mol = Chem.MolFromSmiles("CC(=O)Oc1ccccc1C(=O)O")   # 阿司匹林
print("原子数：", mol.GetNumAtoms())        # → 13
print("键数：", mol.GetNumBonds())          # → 13
print("环数：", Chem.rdMolDescriptors.CalcNumRings(mol))  # → 1
print("分子量：", Chem.rdMolDescriptors.CalcExactMolWt(mol))
# → 180.042258745
print("化学式：", Chem.rdMolDescriptors.CalcMolFormula(mol))
# → C9H8O4

# 规范化 SMILES（重要：同一分子不同写法，RDKit 归一）
s1 = Chem.MolFromSmiles("CCO")
s2 = Chem.MolFromSmiles("OCC")
print(Chem.MolToSmiles(s1), Chem.MolToSmiles(s2))  # → CCO CCO（一样！）
# 用途：两个文件里写法不同的同一分子，转规范 SMILES 后能对账去重

# ============================================================
# 六、分子数据文件（SDF）
# ============================================================
# SDF 是药物化学最常用的文件格式（含结构+属性）
# 读取：
#   mols = Chem.SDMolSupplier("data.sdf")
#   for mol in mols:
#       if mol is not None:
#           print(Chem.MolToSmiles(mol))
#
# 写入：
#   with Chem.SDWriter("out.sdf") as w:
#       w.write(mol)
#
# 保存分子：
#   Chem.MolToMolFile(mol, "aspirin.mol")
# 读回：
#   mol2 = Chem.MolFromMolFile("aspirin.mol")
#   print(Chem.MolToSmiles(mol2))   # 一致

# ============================================================
# 七、练手建议
# ============================================================
# 常见的药物 SMILES（试试解析它们）：
#   对乙酰氨基酚（扑热息痛）: CC(=O)Nc1ccc(O)cc1
#   布洛芬:                   CC(C)Cc1ccc(cc1)C(C)C(=O)O
#   阿莫西林:                 CC1(C)S[C@@H]2[C@H](NC(=O)[C@@H](c3ccc(O)cc3)N)C(=O)N2C1C(=O)O
#   二甲双胍:                 CN(C)C(=N)NC(=N)N
#   吗啡:                     CN1CCC23C4C1CC5=C2C(=C(C=C5)O)OC3C(C=C4)O
#   咖啡因:                   Cn1cnc2c1c(=O)n(C)c(=O)n2C
# 每个都用 Chem.MolFromSmiles 试一下，print 出分子量/化学式

# ============================================================
# 六、易错点汇总
# ============================================================
# 1. Chem.MolFromSmiles 解析失败会返回 None（不报错），
#    用前要判空：if mol is not None
# 2. SMILES 大小写/括号/原子价写错就解析失败；
#    芳香环、支链、电荷都要按规则写
# 3. RDKit 在 Windows 用 pip 可能装不上，
#    官方建议用 conda：conda install -c conda-forge rdkit
# 4. 分子量/化学式用 Descriptors / Chem.rdMolDescriptors 计算
# 5. 一个 SMILES 对应一个分子，但同一分子可有多个合法 SMILES
#    （用 CanonicalSMILES 得到唯一规范形式）
# 6. 后续所有章节都建立在"能把 SMILES 转成分子对象"上

# ============================================================
# 七、自测（40%基础 + 40%中等 + 20%挑战）
# ============================================================
# 【基础】
# 1. MolFromSmiles 解析失败返回什么？用前要做什么？
# 2. SMILES 是什么？有什么用途？
# 3. RDKit 官方推荐的安装方式是什么？
#
# 【中等】
# 4. 用 SMILES 创建阿司匹林分子并打印分子量。
# 5. 解析多个 SMILES，处理解析失败的情况。
# 6. 用 CanonicalSMILES 得到规范形式。
#
# 【挑战】
# 7. 写一个函数：输入 SMILES 列表，输出每个分子的分子量/化学式。
# 8. 解释为什么同一分子可以有多个 SMILES。
