# ============================================================
# 深度学习入门 ② — PyTorch 入门
# ============================================================
# ⚠️ 需要安装：pip install torch（CPU版即可学习）
# PyTorch = 最流行的深度学习框架之一。
# 用 PyTorch 训练一个简单神经网络，流程非常清晰：
#   定义网络 → 定义损失和优化器 → 循环训练 → 评估

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# ============================================================
# 一、tensor：PyTorch 的数据结构（类似 numpy 数组）
# ============================================================
x = torch.tensor([1.0, 2.0, 3.0])
print(x)
print(x.shape)          # → torch.Size([3])

# numpy ↔ tensor 互转
arr = np.array([1, 2, 3])
t = torch.from_numpy(arr)
back = t.numpy()
print(back)             # → [1 2 3]

# 张量运算（自动支持GPU加速）
a = torch.randn(3, 3)
b = torch.randn(3, 3)
print((a + b).shape)    # → torch.Size([3, 3])

# ============================================================
# 二、定义神经网络（继承 nn.Module）
# ============================================================
class SimpleNN(nn.Module):
    """一个简单的全连接神经网络：
    输入5个特征 → 隐藏层(64) → 隐藏层(32) → 输出1个值"""
    def __init__(self, input_size=5, hidden1=64, hidden2=32):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, hidden1),   # 全连接层
            nn.ReLU(),                        # 激活
            nn.Linear(hidden1, hidden2),
            nn.ReLU(),
            nn.Linear(hidden2, 1),            # 输出层（回归，无激活）
        )

    def forward(self, x):
        """前向传播（输入→输出）"""
        return self.net(x)

model = SimpleNN()
print(model)
# 会看到层的结构：Linear(5→64), ReLU, Linear(64→32), ...

# ============================================================
# 三、准备数据 + 损失函数 + 优化器
# ============================================================
# 模拟数据：5个特征 → 1个目标值
np.random.seed(42)
n = 500
X = np.random.randn(n, 5).astype(np.float32)
y = (X[:, 0] * 2 + X[:, 1] - X[:, 2] + np.random.randn(n) * 0.1).astype(
    np.float32)

# 转 tensor
X_t = torch.from_numpy(X)
y_t = torch.from_numpy(y).view(-1, 1)   # 变成列向量

# 损失函数：均方误差（回归用）
criterion = nn.MSELoss()
# 优化器：Adam（自动调学习率）
optimizer = optim.Adam(model.parameters(), lr=0.01)

# ============================================================
# 四、训练循环（核心！）
# ============================================================
epochs = 200
for epoch in range(epochs):
    # 1. 前向传播
    predictions = model(X_t)

    # 2. 计算损失
    loss = criterion(predictions, y_t)

    # 3. 反向传播（计算梯度）
    optimizer.zero_grad()     # 清空上次梯度
    loss.backward()           # 反向传播

    # 4. 更新权重
    optimizer.step()

    if (epoch + 1) % 50 == 0:
        print(f"Epoch {epoch+1:>3}: loss = {loss.item():.4f}")

# 损失不断下降 = 模型在学习
# 这个简单问题最终 loss 会降到 0.01 左右（接近噪声水平）

# ============================================================
# 五、评估与预测
# ============================================================
with torch.no_grad():          # 评估模式：不计算梯度（省内存）
    y_pred = model(X_t).numpy().flatten()

# 计算 R²
ss_res = np.sum((y - y_pred) ** 2)
ss_tot = np.sum((y - y.mean()) ** 2)
r2 = 1 - ss_res / ss_tot
print(f"训练集 R² = {r2:.3f}")

# 保存/加载模型
torch.save(model.state_dict(), "simple_nn.pth")
# 加载：
# model = SimpleNN()
# model.load_state_dict(torch.load("simple_nn.pth"))
# model.eval()

# ============================================================
# 六、train/valid/test 划分（规范做法）
# ============================================================
# 上面演示是"全量训练"（教学简化）。
# 真实做法（和 sklearn 一样）：
#   1. 训练集：学权重
#   2. 验证集：选超参数、Early stopping
#   3. 测试集：最后评估（从不参与训练）
# 划分：X_train, X_test = train_test_split(X, y, test_size=0.2)
# （从 sklearn 导 train_test_split 即可）

# ============================================================
# 七、PyTorch 学习路径建议
# ============================================================
# 1. 先会用：改上面这个模板（层数/激活/学习率）
# 2. 再理解：什么是梯度、过拟合、Dropout、Batch
# 3. 然后应用：分子性质预测（下一节）
# 4. 进阶：CNN(图像) / GNN(分子图) / Transformer
#
# 药学相关方向（了解）：
#   - 分子图神经网络（GNN）预测性质
#   - 分子生成（生成新药物分子）
#   - 蛋白结构预测（AlphaFold 类）
#   - 药物-靶点相互作用预测

# ============================================================
# 八、总结
# ============================================================
# tensor：PyTorch的数据（像numpy，支持GPU）
# 网络：nn.Module + nn.Sequential
# 训练：forward → loss → backward → step（四步循环）
# 损失：回归MSE / 分类CrossEntropy
# 优化：Adam（自动调学习率）
# 保存：torch.save(state_dict)

# ============================================================
# 六、易错点汇总
# ============================================================
# 1. 核心对象：Tensor（张量，类似 numpy 数组 + GPU）
# 2. 自动求导：requires_grad=True + 反向传播 backward()；
#    with torch.no_grad() 里不要梯度（推理/评估时用）
# 3. 模型三件套：定义（nn.Module）→ 损失（nn.MSELoss）→
#    优化器（optim.Adam）
# 4. 训练循环：零梯度（zero_grad）→ 前向 → 损失 → backward →
#    optimizer.step()；别忘 zero_grad！
# 5. 数据要转成 tensor 并匹配 dtype（float32）
# 6. 保存模型用 torch.save(model.state_dict())；
#    加载用 load_state_dict

# ============================================================
# 七、自测（40%基础 + 40%中等 + 20%挑战）
# ============================================================
# 【基础】
# 1. Tensor 是什么？和 numpy 数组的关系？
# 2. 模型定义/损失/优化器三件套是什么？
# 3. 训练循环里忘记 zero_grad 会怎样？
#
# 【中等】
# 4. 定义一个小神经网络（nn.Module）。
# 5. 写完整的训练循环（前向/损失/backward/step）。
# 6. 保存和加载模型参数。
#
# 【挑战】
# 7. 训练一个简单的回归网络并评估。
# 8. 解释 with torch.no_grad() 什么时候用、为什么。
