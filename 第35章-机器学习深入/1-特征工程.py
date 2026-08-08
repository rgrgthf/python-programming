# ============================================================
# 机器学习深入 ① — 特征工程
# ============================================================
# ⚠️ 请在 sci 环境运行
# 一句话总结：特征工程 = "让模型更容易学到规律"的预处理。
# 模型效果好不好，特征工程常常比调模型更重要。

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

# ============================================================
# 一、特征缩放（标准化/归一化）
# ============================================================
# 问题：分子量(180)和LogP(2.3)数值范围差太多，
#       模型（如SVM、神经网络）会被大数值特征主导。
# 解决：把所有特征缩放到相近范围。

data = {
    "分子量": [180.16, 206.28, 151.16, 296.36, 344.44],
    "LogP": [1.2, 3.9, 0.5, 4.2, 3.1],
    "活性": [0.8, 0.5, 0.9, 0.3, 0.6],
}
df = pd.DataFrame(data)

# ① 标准化（StandardScaler）：均值0，标准差1
scaler = StandardScaler()
df["分子量_std"] = scaler.fit_transform(df[["分子量"]])
print("标准化后(均值≈0, 标准差≈1):")
print(df["分子量_std"].round(3))

# ② 归一化（MinMaxScaler）：缩放到 0~1
mms = MinMaxScaler()
df["分子量_norm"] = mms.fit_transform(df[["分子量"]])
print("\n归一化后(0~1):")
print(df["分子量_norm"].round(3))

# 注意：fit 用训练集，transform 用训练集+测试集（防数据泄露！）
# 正确做法：
# scaler.fit(X_train)      # 只在训练集上学习
# X_train = scaler.transform(X_train)
# X_test = scaler.transform(X_test)   # 用训练集学的参数转换

# ============================================================
# 二、分类特征编码（类别 → 数字）
# ============================================================
# 问题：模型只认数字，不认"高/中/低"
labels = ["高", "中", "低", "高", "低"]

# ① LabelEncoder：标签编码（有序类别）
le = LabelEncoder()
encoded = le.fit_transform(labels)
print("\nLabelEncoder:", encoded)   # → [2 1 0 2 0]

# ② One-Hot 编码（无序类别，pandas 一行搞定）
df2 = pd.DataFrame({"剂量等级": ["低", "中", "高", "中", "高"]})
one_hot = pd.get_dummies(df2["剂量等级"], prefix="等级")
print("\nOne-Hot编码：")
print(one_hot)
#   等级_低  等级_中  等级_高
# 0    1      0      0
# ...

# ============================================================
# 三、缺失值处理
# ============================================================
df3 = pd.DataFrame({
    "浓度": [0.5, np.nan, 1.0, np.nan, 2.0],
    "活性": [0.8, 0.6, 0.9, 0.7, 0.5],
})

# 方法1：删除含缺失的行（数据多时）
df3_drop = df3.dropna()

# 方法2：用均值/中位数填充
df3_fill = df3.copy()
df3_fill["浓度"] = df3_fill["浓度"].fillna(df3["浓度"].mean())
print("\n均值填充后：")
print(df3_fill)

# ============================================================
# 四、创建新特征（特征组合）
# ============================================================
# 药学场景：单一描述符不够，组合起来更有信息量
df4 = pd.DataFrame({
    "分子量": [180, 206, 151, 296],
    "LogP": [1.2, 3.9, 0.5, 4.2],
    "TPSA": [63, 37, 50, 55],
})

# 常见特征组合
df4["MW_LogP"] = df4["分子量"] / df4["LogP"]      # 比值
df4["MW_TPSA"] = df4["分子量"] * df4["TPSA"]      # 乘积
df4["logMW"] = np.log(df4["分子量"])               # 对数变换
print("\n新特征：")
print(df4)

# ============================================================
# 五、完整流程演示：特征工程 + 建模
# ============================================================
np.random.seed(42)
n = 200
# 模拟：分子量、LogP → 活性（有规律 + 噪声）
X = pd.DataFrame({
    "MW": np.random.uniform(100, 500, n),
    "LogP": np.random.uniform(-2, 5, n),
    "TPSA": np.random.uniform(20, 120, n),
})
y = 0.8 - X["MW"] * 0.0008 + X["LogP"] * 0.1 - X["TPSA"] * 0.002 \
    + np.random.normal(0, 0.05, n)

# 划分训练/测试
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# 缩放（正确：只在训练集 fit）
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 建模 + 评估
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)
r2 = r2_score(y_test, model.predict(X_test_scaled))
print(f"\n特征工程后 R² = {r2:.3f}")

# 特征重要性（看哪个特征最有信息量）
importance = pd.Series(model.feature_importances_, index=X.columns)
print("\n特征重要性：")
print(importance.sort_values(ascending=False))

# ============================================================
# 六、总结
# ============================================================
# 缩放：StandardScaler / MinMaxScaler（只 fit 训练集）
# 编码：LabelEncoder(有序) / One-Hot(无序)
# 缺失：dropna / fillna(均值)
# 新特征：比值/乘积/对数变换
# 心法：特征工程 = 领域知识 + 创造性 + 验证

# ============================================================
# 六、易错点汇总
# ============================================================
# 1. 特征工程 = 从原始数据造出更有用的特征：
#    标准化/缺失处理/组合/编码
# 2. 特征越多越好？不——过多无关特征会拖累模型（维度灾难）
# 3. 编码：类别特征用 OneHot；数值特征标准化
# 4. 特征选择：相关性高/方差接近 0 的特征考虑去掉
# 5. 特征工程要【在训练集上做】并记录变换，
#    测试集用同样的变换（防泄漏）
# 6. 心法：领域知识（药学）+ 创造性 + 验证

# ============================================================
# 七、自测（40%基础 + 40%中等 + 20%挑战）
# ============================================================
# 【基础】
# 1. 特征工程是干什么的？
# 2. 特征是不是越多越好？为什么？
# 3. 类别特征怎么编码？
#
# 【中等】
# 4. 给描述符矩阵做标准化。
# 5. 处理缺失特征值（填充/删除）。
# 6. 做简单的特征选择（去低方差/高相关）。
#
# 【挑战】
# 7. 为 QSAR 数据设计特征工程流水线。
# 8. 解释为什么特征工程要在训练集上做。
