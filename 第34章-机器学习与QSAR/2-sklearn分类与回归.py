# ============================================================
# 机器学习入门 ② — sklearn 分类与回归
# ============================================================
# 用 sklearn 构建第一个 QSAR 模型：分类（有无活性）+ 回归（预测数值）。
# 场景：从分子描述符预测"是否具有镇痛活性"（教学简化数据）。

import numpy as np
from rdkit import Chem
from rdkit.Chem import Descriptors
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, r2_score, mean_squared_error

# ============================================================
# 一、准备数据（模拟 50 个分子）
# ============================================================
import random
random.seed(42)

def featurize(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    return [Descriptors.MolWt(mol), Descriptors.MolLogP(mol),
            Descriptors.NumHDonors(mol), Descriptors.NumHAcceptors(mol),
            Descriptors.TPSA(mol), Chem.rdMolDescriptors.CalcNumAromaticRings(mol)]

# 模拟：有/无活性分子各25个（用随机SMILES简化，教学用）
base_active = ["CC(=O)c1ccccc1", "CC(C)Cc1ccccc1", "COc1ccccc1",
               "O=C(N)c1ccccc1", "CCOc1ccccc1", "CC(=O)Nc1ccccc1"]
base_inactive = ["CCCC", "CCO", "CCN", "CCCCCC", "CCOC", "CC(=O)OC"]

def make_variants(smiles, n):
    mol = Chem.MolFromSmiles(smiles)
    return [smiles] * n   # 简化：重复（真实场景是真正不同的分子）

X, y = [], []
for s in base_active:
    for _ in range(5):
        f = featurize(s)
        if f: X.append(f); y.append(1)      # 活性=1
for s in base_inactive:
    for _ in range(5):
        f = featurize(s)
        if f: X.append(f); y.append(0)      # 无活性=0

X = np.array(X); y = np.array(y)
print("数据：", X.shape, "活性个数：", sum(y))

# ============================================================
# 二、分类模型：随机森林
# ============================================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("\n===== 分类结果 =====")
print("准确率：", round(accuracy_score(y_test, y_pred), 3))

# 预测概率（药学更常用——排序候选）
proba = model.predict_proba(X_test)[:, 1]   # 预测为活性的概率
print("各测试分子的活性概率：", np.round(proba, 2))

# 特征重要性（哪个描述符最重要！）
importances = model.feature_importances_
feature_names = ["MW", "LogP", "HBD", "HBA", "TPSA", "AromaticRings"]
for name, imp in sorted(zip(feature_names, importances), key=lambda x: -x[1]):
    print(f"  {name}: {imp:.3f}")
# 特征重要性帮助理解"什么性质驱动了活性"

# ============================================================
# 三、交叉验证（防过拟合的可靠评估）
# ============================================================
from sklearn.model_selection import cross_val_score
scores = cross_val_score(RandomForestClassifier(random_state=42),
                         X, y, cv=5, scoring="accuracy")
print("\n5折交叉验证准确率：", np.round(scores, 3))
print("平均：", round(scores.mean(), 3), "±", round(scores.std(), 3))
# 用交叉验证评估比单次 train_test_split 更可靠

# ============================================================
# 四、回归模型：预测数值性质
# ============================================================
# 模拟：预测 LogP（用真实计算的 LogP 作为标签）
from rdkit.Chem import Descriptors

X_r, y_r = [], []
for s in base_active + base_inactive:
    mol = Chem.MolFromSmiles(s)
    if mol:
        X_r.append(featurize(s))
        y_r.append(Descriptors.MolLogP(mol))   # 真实 LogP 作为标签

X_r = np.array(X_r); y_r = np.array(y_r)
X_tr, X_te, y_tr, y_te = train_test_split(X_r, y_r, test_size=0.3, random_state=42)

reg = RandomForestRegressor(n_estimators=100, random_state=42)
reg.fit(X_tr, y_tr)
y_pred_r = reg.predict(X_te)

print("\n===== 回归结果（预测LogP）=====")
print("R² =", round(r2_score(y_te, y_pred_r), 3))
print("RMSE =", round(np.sqrt(mean_squared_error(y_te, y_pred_r)), 3))
for true, pred in list(zip(y_te, y_pred_r))[:5]:
    print(f"  真实 {true:.2f} vs 预测 {pred:.2f}")

# ============================================================
# 五、常见模型对比（了解选哪个）
# ============================================================
# 随机森林 RandomForest：稳健、不需要标准化、特征重要性可解释 ← 入门首选
# 逻辑回归 LogisticRegression：简单、可解释、需要标准化
# SVM：小数据好、需要标准化、可解释性差
# XGBoost/LightGBM：强但容易过拟合、竞赛常用
# 神经网络/DNN：大数据需要、黑盒、后期再学
#
# 药学 QSAR 入门建议：先随机森林 + 逻辑回归，够用且可发表

# ============================================================
# 六、完整 QSAR 流程（记住）
# ============================================================
# 1. 收集数据（活性值 + SMILES，可从 ChEMBL 下载）
# 2. 分子 → 描述符/指纹（RDKit）
# 3. 数据清洗、去重、处理缺失
# 4. 拆分训练/测试
# 5. 训练模型（随机森林起步）
# 6. 交叉验证 + 评价（AUC/R²）
# 7. 外部验证（用没见过的数据测）
# 8. 用模型预测新候选分子
