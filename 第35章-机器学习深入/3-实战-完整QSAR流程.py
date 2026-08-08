# ============================================================
# 机器学习深入 ③ — 实战：完整 QSAR 建模流程
# ============================================================
# ⚠️ 请在 sci 环境运行（需要 rdkit + sklearn）
# 把前面学的串成一条完整的流水线：
#   SMILES → 描述符 → 特征工程 → 调参 → 评估 → 保存 → 预测
# 这是你作品集的"标准模板"！

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error
import joblib

# ============================================================
# 一、准备数据（模拟：SMILES + 活性值）
# ============================================================
# 真实场景从文件读：pd.read_csv("qsar_data.csv")
np.random.seed(42)
n = 300
smiles_list = [f"mol{i}" for i in range(n)]    # 真实是SMILES串
activity = np.random.uniform(0.1, 10.0, n)     # 真实是IC50等

# ============================================================
# 二、计算描述符（RDKit 版，需 sci 环境）
# ============================================================
def calc_descriptors(smiles_list):
    """从 SMILES 计算描述符（用RDKit）"""
    # 真实代码（第13/32章学的）：
    # from rdkit import Chem
    # from rdkit.Chem import Descriptors
    # features = []
    # for s in smiles_list:
    #     mol = Chem.MolFromSmiles(s)
    #     if mol is None:
    #         continue
    #     features.append({
    #         "MW": Descriptors.MolWt(mol),
    #         "LogP": Descriptors.MolLogP(mol),
    #         "HBD": Descriptors.NumHDonors(mol),
    #         "HBA": Descriptors.NumHAcceptors(mol),
    #         "TPSA": Descriptors.TPSA(mol),
    #     })
    # return pd.DataFrame(features)

    # 这里用模拟数据演示流程
    return pd.DataFrame({
        "MW": np.random.uniform(100, 500, len(smiles_list)),
        "LogP": np.random.uniform(-2, 5, len(smiles_list)),
        "HBD": np.random.randint(0, 5, len(smiles_list)),
        "HBA": np.random.randint(0, 8, len(smiles_list)),
        "TPSA": np.random.uniform(20, 120, len(smiles_list)),
    })

X = calc_descriptors(smiles_list)
y = activity
print("特征矩阵：", X.shape)
print(X.head())

# ============================================================
# 三、数据划分（stratify 保持分布）
# ============================================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# ============================================================
# 四、特征缩放 + 建模 + 调参
# ============================================================
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

# 调参
param_grid = {
    "n_estimators": [100, 200],
    "max_depth": [None, 10],
    "min_samples_split": [2, 5],
}
grid = GridSearchCV(
    RandomForestRegressor(random_state=42),
    param_grid, cv=5, n_jobs=-1,
)
grid.fit(X_train_s, y_train)
print(f"最佳参数: {grid.best_params_}")

# ============================================================
# 五、评估
# ============================================================
model = grid.best_estimator_
y_pred = model.predict(X_test_s)

r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
print(f"测试集 R² = {r2:.3f}")
print(f"测试集 MAE = {mae:.3f}")

# 特征重要性
importance = pd.Series(model.feature_importances_, index=X.columns)
print("\n特征重要性排序：")
print(importance.sort_values(ascending=False))

# ============================================================
# 六、保存模型（joblib）—— 学过的！现在用上
# ============================================================
joblib.dump(model, "qsar_model.pkl")
joblib.dump(scaler, "qsar_scaler.pkl")
print("\n✅ 模型和缩放器已保存")

# ============================================================
# 七、加载模型做预测（新化合物）
# ============================================================
def predict_activity(descriptors_dict):
    """给新化合物预测活性"""
    loaded_model = joblib.load("qsar_model.pkl")
    loaded_scaler = joblib.load("qsar_scaler.pkl")
    # 输入必须是训练时同样的特征顺序
    features = pd.DataFrame([descriptors_dict], columns=X.columns)
    features_s = loaded_scaler.transform(features)
    return loaded_model.predict(features_s)[0]

# 预测一个新分子
new_mol = {"MW": 220.5, "LogP": 2.1, "HBD": 2, "HBA": 5, "TPSA": 70}
pred = predict_activity(new_mol)
print(f"\n新分子预测活性: {pred:.2f}")

# ============================================================
# 八、把这个流程变成你的模板
# ============================================================
# 换成真实数据的步骤：
#   1. 读数据：pd.read_excel("活性数据.xlsx")（第23章）
#   2. 算描述符：RDKit（第32章）
#   3. 特征工程（第35章①）
#   4. 调参评估（第35章②）
#   5. 保存模型 + 写个预测脚本（第25章打包成exe！）
#   6. 配测试（第24章）
#   7. 写说明文档放作品集
# 这就是一个完整的 QSAR 工具项目！

# ============================================================
# 九、总结
# ============================================================
# 完整流程：数据→特征→划分→缩放→调参→评估→保存→预测
# 关键点：scaler/模型一起保存、特征顺序一致
# joblib：保存/加载模型（第15/34章复习）
# 这个流程 = 作品集核心项目骨架

# ============================================================
# 六、易错点汇总
# ============================================================
# 1. 完整 QSAR：数据 → 描述符 → 特征工程 → 划分 →
#    CV 调参 → 最终模型 → 测试集评估 → 新分子预测
# 2. 每一步都记下来（预处理参数），保证可复现
# 3. 最终评估只用一次测试集，别反复调
# 4. 结果写进报告：模型、参数、CV 分数、测试集分数
# 5. 保存模型（joblib/pickle），方便复用
# 6. 这个流程能跑通 = 一个完整科研作品

# ============================================================
# 七、自测（40%基础 + 40%中等 + 20%挑战）
# ============================================================
# 【基础】
# 1. 完整 QSAR 流程的步骤顺序？
# 2. 为什么要记录每一步的预处理参数？
# 3. 模型保存用什么？
#
# 【中等】
# 4. 搭建完整 QSAR 流程并评估。
# 5. 保存模型并用新分子预测。
# 6. 写一份简单的模型报告。
#
# 【挑战】
# 7. 把完整 QSAR 流程整理成作品集项目（含说明）。
# 8. 解释"测试集只用一次"为什么是科研红线。
