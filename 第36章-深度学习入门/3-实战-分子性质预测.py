# ============================================================
# 深度学习入门 ③ — 实战：分子性质预测（DNN）
# ============================================================
# ⚠️ 需要：pip install torch；如需RDKit请用 sci 环境
# 综合实战：用深度神经网络预测分子活性。
# 对比第35章的随机森林——同样的任务，两种方法。
# 说明：这里用模拟描述符演示完整流程，换成真实数据即可用。

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score

# ============================================================
# 一、准备数据（模拟 1000 个分子的描述符 → 活性）
# ============================================================
np.random.seed(42)
n = 1000
X = pd.DataFrame({
    "MW": np.random.uniform(100, 500, n),
    "LogP": np.random.uniform(-2, 6, n),
    "HBD": np.random.randint(0, 6, n),
    "HBA": np.random.randint(0, 10, n),
    "TPSA": np.random.uniform(20, 150, n),
    "RotBonds": np.random.randint(0, 12, n),
})
# 活性 = 特征的非线性组合 + 噪声（模拟真实QSAR）
y = (0.9 - X["MW"] * 0.0012 + X["LogP"] * 0.15 - X["TPSA"] * 0.003
     + np.sin(X["HBA"] * 0.5) + np.random.normal(0, 0.08, n))

print(f"数据: {X.shape[0]} 分子, {X.shape[1]} 特征")

# ============================================================
# 二、数据预处理（和 sklearn 流程一致）
# ============================================================
# 划分
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# 标准化
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train).astype(np.float32)
X_test_s = scaler.transform(X_test).astype(np.float32)
y_train = y_train.values.astype(np.float32)
y_test = y_test.values.astype(np.float32)

# 转 tensor
X_train_t = torch.from_numpy(X_train_s)
X_test_t = torch.from_numpy(X_test_s)
y_train_t = torch.from_numpy(y_train).view(-1, 1)
y_test_t = torch.from_numpy(y_test).view(-1, 1)

# ============================================================
# 三、定义网络（6特征 → 隐藏 → 1输出）
# ============================================================
class ActivityNN(nn.Module):
    def __init__(self, input_size=6):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.ReLU(),
            nn.Dropout(0.2),          # 防过拟合（第36章①学的）
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
        )

    def forward(self, x):
        return self.net(x)

model = ActivityNN()
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.005)

# ============================================================
# 四、训练（含验证集 Early Stopping 简化版）
# ============================================================
# 再分一部分当验证集（从训练集里分）
X_tr, X_val, y_tr, y_val = train_test_split(
    X_train_t, y_train_t, test_size=0.15, random_state=42)

best_val = float("inf")
best_state = None
epochs = 300

for epoch in range(epochs):
    # 训练模式
    model.train()
    optimizer.zero_grad()
    pred = model(X_tr)
    loss = criterion(pred, y_tr)
    loss.backward()
    optimizer.step()

    # 每20轮看验证集
    if (epoch + 1) % 20 == 0:
        model.eval()
        with torch.no_grad():
            val_pred = model(X_val)
            val_loss = criterion(val_pred, y_val).item()
        print(f"Epoch {epoch+1:>3}: 训练loss={loss.item():.4f} "
              f"验证loss={val_loss:.4f}")
        # Early stopping：验证集不降了就用最好的
        if val_loss < best_val:
            best_val = val_loss
            best_state = model.state_dict()

# 恢复最佳模型
if best_state:
    model.load_state_dict(best_state)

# ============================================================
# 五、测试集评估
# ============================================================
model.eval()
with torch.no_grad():
    y_pred = model(X_test_t).numpy().flatten()

r2 = r2_score(y_test, y_pred)
print(f"\n测试集 R² = {r2:.3f}")

# 对比：随机森林的效果（第35章学的）
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor(n_estimators=200, random_state=42)
rf.fit(X_train_s, y_train)
rf_r2 = r2_score(y_test, rf.predict(X_test_s))
print(f"随机森林 R² = {rf_r2:.3f}（对比）")

# ============================================================
# 六、保存与预测新分子
# ============================================================
torch.save(model.state_dict(), "activity_nn.pth")
print("模型已保存 activity_nn.pth")

def predict_new(descriptors_dict):
    """预测新分子的活性"""
    model2 = ActivityNN()
    model2.load_state_dict(torch.load("activity_nn.pth"))
    model2.eval()
    # 特征顺序必须和训练一致！
    features = np.array([[descriptors_dict[c] for c in X.columns]],
                        dtype=np.float32)
    features_s = scaler.transform(features)
    with torch.no_grad():
        return model2(torch.from_numpy(features_s)).item()

new_mol = {"MW": 250, "LogP": 3.0, "HBD": 1, "HBA": 4,
           "TPSA": 60, "RotBonds": 5}
print(f"新分子预测活性: {predict_new(new_mol):.3f}")

# ============================================================
# 七、深度学习 vs 传统机器学习（结论）
# ============================================================
# 数据量小（几百~几千）：随机森林 通常更好/更稳/更快
# 数据量大（几万+）：神经网络 能挖出更多模式
# 实操建议：两个都试，用交叉验证比，谁好选谁
# 这本身也是专业做法——不迷信，用数据说话！

# ============================================================
# 八、总结
# ============================================================
# 完整DNN流程：数据→缩放→网络→训练(含验证)→评估→保存→预测
# Dropout 防过拟合
# Early stopping：验证集选最优
# 对比 sklearn：小数据先试传统ML
# 换真实数据：把 X 换成 RDKit 算的描述符（第35章③）
