# ============================================================
# 药物发现实战 ③ — 综合项目：从靶点到候选分子
# ============================================================
# 把第13~16章所有技能整合成一个完整项目。
# 场景：开发针对某靶点的抑制剂（教学简化版）。
# 流程：数据 → 特征 → 模型 → 虚拟筛选 → 对接 → 输出报告

# 提示：这是一个"项目蓝图"，各环节的完整代码
# 已在前面各章分别实现，这里组装成流水线。

import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors
from rdkit.DataStructs import TanimotoSimilarity

# ============================================================
# 一、项目总览
# ============================================================
# 目标：为某靶点寻找潜在抑制剂
#
# 环节1：收集已知活性数据（ChEMBL下载）
# 环节2：分子特征化（RDKit指纹/描述符）
# 环节3：训练QSAR模型（sklearn）
# 环节4：虚拟筛选（相似度或模型预测）
# 环节5：分子对接打分（Vina）
# 环节6：汇总报告
#
# 本文件演示环节1→4 的组装（简化数据）

# ============================================================
# 二、环节1：数据准备
# ============================================================
# 真实项目：从 ChEMBL 下载某靶点（如 COX-2）的 IC50 数据
# 这里用简化数据演示结构
training_data = [
    # (SMILES, 活性标签 1=有活性)
    ("CC(=O)Oc1ccccc1C(=O)O", 1),
    ("CC(C)Cc1ccc(cc1)C(C)C(=O)O", 1),
    ("COc1ccc2cc(ccc2c1)C(C)C(=O)O", 1),
    ("CC(=O)Nc1ccc(O)cc1", 1),
    ("CCCC", 0),
    ("CCO", 0),
    ("CCN", 0),
    ("C1CCCCC1", 0),
]

# ============================================================
# 三、环节2：特征化
# ============================================================
def fingerprint(smiles, radius=2, nbits=2048):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=nbits)
    arr = np.zeros((nbits,))
    from rdkit.DataStructs import ConvertToNumpyArray
    ConvertToNumpyArray(fp, arr)
    return arr

X, y = [], []
for smi, label in training_data:
    f = fingerprint(smi)
    if f is not None:
        X.append(f)
        y.append(label)
X = np.array(X); y = np.array(y)

# ============================================================
# 四、环节3：训练模型
# ============================================================
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

model = RandomForestClassifier(n_estimators=100, random_state=42)
scores = cross_val_score(model, X, y, cv=4)
print(f"模型交叉验证准确率：{scores.mean():.3f} ± {scores.std():.3f}")
model.fit(X, y)
print("模型训练完成")

# ============================================================
# 五、环节4：虚拟筛选新分子
# ============================================================
screening_library = [
    "COc1ccc2cc(ccc2c1)C(C)C(=O)O",       # 萘普生
    "CC(C(=O)O)c1ccccc1C(=O)c1ccccc1",    # 酮洛芬
    "CC(C)Cc1ccc(cc1)C(O)C(=O)O",         # 氟比洛芬
    "CCCCCCCC",                            # 烷烃（应排除）
    "CCCC",                                # 烷烃（应排除）
]

print("\n===== 虚拟筛选结果 =====")
hits = []
for smi in screening_library:
    f = fingerprint(smi)
    if f is None:
        continue
    proba = model.predict_proba([f])[0, 1]
    pred = model.predict([f])[0]
    status = "✓ 候选" if pred == 1 else "✗ 排除"
    print(f"  {status} | 概率 {proba:.2f} | {smi}")
    if pred == 1:
        hits.append(smi)

# ============================================================
# 六、环节5：候选输出（对接入口）
# ============================================================
print(f"\n候选分子数：{len(hits)}")
for smi in hits:
    mol = Chem.MolFromSmiles(smi)
    print(f"  {smi} | MW={Descriptors.MolWt(mol):.1f} | LogP={Descriptors.MolLogP(mol):.2f}")

# 保存候选 SDF，供 Vina 对接
w = Chem.SDWriter("project_candidates.sdf")
for smi in hits:
    mol = Chem.MolFromSmiles(smi)
    mol.SetProp("_Name", smi)
    w.write(mol)
w.close()
print("候选已保存 project_candidates.sdf")

# ============================================================
# 七、项目报告模板（复试/论文展示）
# ============================================================
# 1. 背景：靶点与疾病的关系
# 2. 方法：数据来源、特征、模型、筛选策略
# 3. 结果：模型AUC、候选分子列表、性质表
# 4. 结论：下一步对接验证方向
#
# 这个流程就是 CADD（计算机辅助药物设计）的入门骨架。
# 复试时可以展示："我用机器学习 + 分子筛选方法，
# 对 XX 靶点进行了虚拟筛选，得到 N 个候选分子"

# ============================================================
# 八、进阶方向（未来）
# ============================================================
# 1. 用真实 ChEMBL 数据（几千分子）替换模拟数据
# 2. 加分子对接（Vina）
# 3. 用 DeepChem 图神经网络提升预测
# 4. 用 PyMOL/PLIP 分析蛋白-配体相互作用
# 5. 如果是毕业课题：结合实验室湿实验验证
