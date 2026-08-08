# ============================================================
# 机器学习深入 ② — 模型调优与交叉验证
# ============================================================
# ⚠️ 请在 sci 环境运行
# 模型效果不好怎么办？→ 调超参数 + 更可靠的评估。
# 这一节：交叉验证、GridSearchCV 自动调参、学习曲线。

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import (cross_val_score, GridSearchCV,
                                     train_test_split)
from sklearn.metrics import accuracy_score

# ============================================================
# 一、为什么单次划分不可靠？
# ============================================================
# 数据划分一次 → 结果取决于"运气"（哪部分当测试集）
# 交叉验证：划分多次，每次换测试集，结果取平均 → 更可信

# ============================================================
# 二、交叉验证（cross_val_score）
# ============================================================
# 生成模拟分类数据（如：分子有活性/无活性）
X, y = make_classification(n_samples=500, n_features=10,
                           n_informative=6, random_state=42)

model = RandomForestClassifier(n_estimators=50, random_state=42)

# 5折交叉验证：数据分5份，轮流1份测试4份训练
scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")
print("5折交叉验证准确率：", scores.round(3))
print(f"平均: {scores.mean():.3f} ± {scores.std():.3f}")

# 对比单次划分（碰运气，可能偏高或偏低）
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)
print(f"单次划分准确率: {accuracy_score(y_test, model.predict(X_test)):.3f}")

# ============================================================
# 三、GridSearchCV：自动搜索最佳超参数
# ============================================================
# 随机森林有很多参数（n_estimators、max_depth...）
# GridSearchCV = 穷举所有组合，交叉验证选出最好的

param_grid = {
    "n_estimators": [50, 100],       # 树的数量
    "max_depth": [None, 5, 10],      # 树的最大深度
    "min_samples_split": [2, 5],     # 分裂最少样本数
}

grid = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=3,                    # 3折交叉验证
    scoring="accuracy",
    n_jobs=-1,               # 用所有CPU核心
)

grid.fit(X, y)
print(f"\n最佳参数: {grid.best_params_}")
print(f"最佳分数: {grid.best_score_:.3f}")

# 用最佳模型预测
best_model = grid.best_estimator_

# ============================================================
# 四、不同模型的对比（选模型的方法）
# ============================================================
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

models = {
    "逻辑回归": LogisticRegression(max_iter=1000),
    "KNN": KNeighborsClassifier(),
    "SVM": SVC(),
    "随机森林": RandomForestClassifier(n_estimators=50, random_state=42),
}

print("\n各模型交叉验证对比：")
results = {}
for name, model in models.items():
    scores = cross_val_score(model, X, y, cv=5)
    results[name] = scores.mean()
    print(f"  {name}: {scores.mean():.3f}")

best_name = max(results, key=results.get)
print(f"\n🏆 效果最好: {best_name}")

# ============================================================
# 五、过拟合与欠拟合
# ============================================================
# 欠拟合：训练和测试都差 → 模型太简单，加复杂度
# 过拟合：训练很好、测试差 → 模型死记硬背，要正则化/简化
#
# 判断方法：对比训练集和测试集分数
#   训练0.99 / 测试0.60 → 过拟合！
#   训练0.62 / 测试0.60 → 正常
#   训练0.55 / 测试0.52 → 欠拟合

# 解决过拟合：
#   - 减少模型复杂度（max_depth调小、减少特征）
#   - 增加数据量
#   - 正则化（正则化参数C/alpha调小）

# ============================================================
# 六、类别不平衡（药学常见！）
# ============================================================
# 场景：1000个化合物，只有50个有活性 → 正类太少
# 模型会"偷懒"全预测负类（准确率95%但毫无用）
# 解决：
#   1. class_weight="balanced"（sklearn 内置）
#   2. 过采样/欠采样（imblearn 库）
#   3. 换评估指标：用 F1 / AUC，别只看准确率

from sklearn.metrics import f1_score, roc_auc_score

# 模拟不平衡数据
X_u, y_u = make_classification(
    n_samples=1000, n_features=10, weights=[0.95, 0.05], random_state=42)

model_bal = RandomForestClassifier(class_weight="balanced", random_state=42)
scores_f1 = cross_val_score(model_bal, X_u, y_u, cv=5, scoring="f1")
print(f"\n不平衡数据 F1 = {scores_f1.mean():.3f}（class_weight=balanced）")

# ============================================================
# 七、总结
# ============================================================
# 交叉验证：cross_val_score（评估更可靠）
# 自动调参：GridSearchCV（找最佳超参数）
# 模型对比：多个模型交叉验证取平均
# 过拟合：训练好测试差 → 简化/正则化
# 不平衡：class_weight="balanced" + 用F1/AUC

# ============================================================
# 六、易错点汇总
# ============================================================
# 1. 交叉验证（CV）：把数据切 K 份，轮流做验证——
#    比单次划分更可靠
# 2. GridSearchCV 调参：给参数网格，自动找最优；
#    参数太多会非常慢
# 3. 类别不平衡（活性分子远少于非活性）：
#    class_weight="balanced" 或用 F1/AUC 评估
# 4. 不平衡数据别只看准确率（全猜多数类也有高准确率）
# 5. 调参要在训练/验证集上，测试集只能最后用一次
# 6. 先默认参数跑通，再调参

# ============================================================
# 七、自测（40%基础 + 40%中等 + 20%挑战）
# ============================================================
# 【基础】
# 1. 交叉验证是什么？比单次划分好在哪？
# 2. GridSearchCV 干什么？
# 3. 类别不平衡时用什么评估指标？
#
# 【中等】
# 4. 用 cross_val_score 做 5 折交叉验证。
# 5. 用 GridSearchCV 调一个模型的参数。
# 6. 处理类别不平衡（class_weight）。
#
# 【挑战】
# 7. 给 QSAR 模型做交叉验证 + 调参。
# 8. 解释为什么测试集只能最后用一次。
