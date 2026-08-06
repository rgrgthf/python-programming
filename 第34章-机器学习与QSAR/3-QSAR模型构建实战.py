# ============================================================
# 机器学习入门 ③ — QSAR 模型构建实战
# ============================================================
# 用更真实的流程：指纹特征 + 多种模型对比 + 模型保存与复用。
# 场景：基于分子指纹预测"化合物是否对某靶点有活性"。

import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.DataStructs import ConvertToNumpyArray
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix

# ============================================================
# 一、用 ECFP4 指纹做特征（比描述符更全面）
# ============================================================
def fp_featurize(smiles):
    """SMILES → Morgan指纹（2048位）"""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius=2, nBits=2048)
    arr = np.zeros((2048,))
    ConvertToNumpyArray(fp, arr)
    return arr

# 模拟数据（活性/非活性）
data = [
    # (SMILES, label)
    ("CC(=O)Oc1ccccc1C(=O)O", 1),
    ("CC(C)Cc1ccc(cc1)C(C)C(=O)O", 1),
    ("COc1ccc2cc(ccc2c1)C(C)C(=O)O", 1),
    ("CC(=O)Nc1ccc(O)cc1", 1),
    ("CN1CCC23C4C1CC5=C2C(=C(C=C5)O)OC3C(C=C4)O", 1),
    ("CC(=O)c1ccc(O)cc1", 1),
    ("CCOc1ccc(cc1)C(C)C(=O)O", 1),
    ("CCCC", 0),
    ("CCO", 0),
    ("CCN", 0),
    ("CCCCCCCC", 0),
    ("CCOC", 0),
    ("CC(=O)OC", 0),
    ("CCCCCCCCCC", 0),
]

X, y = [], []
for smi, label in data:
    f = fp_featurize(smi)
    if f is not None:
        X.append(f)
        y.append(label)
X = np.array(X); y = np.array(y)
print("特征矩阵：", X.shape)   # → (14, 2048)

# ============================================================
# 二、两种模型对比
# ============================================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y)

models = {
    "随机森林": RandomForestClassifier(n_estimators=100, random_state=42),
    "逻辑回归": LogisticRegression(max_iter=1000, random_state=42),
}

for name, model in models.items():
    # 交叉验证
    cv_scores = cross_val_score(model, X, y, cv=5, scoring="roc_auc")
    # 训练+测试
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    proba = model.predict_proba(X_test)[:, 1]
    acc = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, proba)
    print(f"\n{name}:")
    print(f"  5折交叉验证AUC: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
    print(f"  测试集准确率: {acc:.3f}")
    print(f"  测试集AUC: {auc:.3f}")

# ============================================================
# 三、查看混淆矩阵（分类的细节）
# ============================================================
model = models["随机森林"]
y_pred = model.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
print("\n混淆矩阵（[[真阴, 假阳], [假阴, 真阳]]）：")
print(cm)
# 注意假阴（假阴性）：活性分子被漏掉 → 药学里最该避免！
# 宁可多几个假阳（多做几次验证），不能漏掉潜在活性物

# ============================================================
# 四、模型保存与加载（部署/复用）
# ============================================================
import joblib

# 保存模型
joblib.dump(model, "qsar_model.pkl")
print("\n模型已保存：qsar_model.pkl")

# 加载模型
loaded_model = joblib.load("qsar_model.pkl")

# 用加载的模型预测新分子
new_molecules = [
    "COc1ccc2cc(ccc2c1)C(C)C(=O)O",   # 萘普生（应该预测活性）
    "CCCCCC",                          # 己烷（应该预测无活性）
]
for smi in new_molecules:
    fp = fp_featurize(smi)
    proba = loaded_model.predict_proba([fp])[0, 1]
    pred = loaded_model.predict([fp])[0]
    print(f"{smi}: 预测={'活性' if pred==1 else '无活性'} (概率{proba:.2f})")

# ============================================================
# 五、ADMET 预测概念（药物发现关键）
# ============================================================
# QSAR 不止预测活性，还预测 ADMET 性质：
#   A 吸收（Absorption）、D 分布（Distribution）
#   M 代谢（Metabolism）、E 排泄（Excretion）
#   T 毒性（Toxicity）
# 一个分子活性再强，吸收差/毒性大也成不了药
#
# 开源工具（了解）：
#   ADMETlab：在线ADMET预测
#   SwissADME：在线工具
#   DeepChem 的 ADMET 模块：代码化
# 这就是"药物发现 = 活性 + 安全性 + 成药性"的综合

# ============================================================
# 六、真实数据来源（做正式项目时用）
# ============================================================
# ChEMBL：www.ebi.ac.uk/chembl —— 生物活性数据（免费，QSAR标配）
#   - 可按靶点/疾病下载 IC50/EC50 数据
#   - 下载 CSV → SMILES + 活性值 → 你的第一个真实 QSAR 项目
#
# 建议的正式项目路线：
#   1. 从 ChEMBL 下载某个靶点的活性数据（如 COX-2）
#   2. 清洗（去重复、去无效、转 pIC50）
#   3. 指纹特征 → 随机森林 → 交叉验证
#   4. 报告：AUC、特征重要性、预测新化合物
#   5. 这就是复试能展示的"真实科研作品"
