# ============================================================
# 药物发现实战 ② — DeepChem 入门与药物发现AI
# ============================================================
# DeepChem = 面向药物发现/材料科学的深度学习库（基于TensorFlow/PyTorch）。
# 它封装了大量药物发现常用模型和数据。
# 注意：DeepChem 较重，先在 sci 环境装好再学。

# ============================================================
# 一、安装与验证
# ============================================================
# conda activate sci
# pip install deepchem  (较大，约几百MB，含依赖)
# 或用 conda: conda install -c conda-forge deepchem

# import deepchem as dc
# print(dc.__version__)

# ============================================================
# 二、DeepChem 能做什么
# ============================================================
# 1. 数据集封装：把分子数据集标准化成模型能吃的格式
# 2. 特征化：内置各种分子特征（ECFP、图结构）
# 3. 模型：图神经网络（GCN）、消息传递（MPNN）、Transformer
# 4. 任务：性质预测、虚拟筛选、ADMET、蛋白-配体相互作用
# 5. 数据集：内置 Tox21、HIV、MUV、BACE 等公开基准

# ============================================================
# 三、典型工作流（对比 sklearn 版本）
# ============================================================
# sklearn 版：分子 → 描述符/指纹（人工特征）→ 随机森林
# DeepChem 版：分子 → 图结构（自动学习特征）→ 图神经网络
#
# 区别：
#   sklearn + 指纹：特征人工设计，简单可解释，数据少时好用
#   DeepChem + GNN：特征自动学，需要大数据，效果通常更好
#
# 入门建议：先精通 sklearn+指纹（你已经会），
# 数据量够大（>几千）后再上 DeepChem

# ============================================================
# 四、DeepChem 代码示例（概念）
# ============================================================
# （以下为概念代码，需安装 deepchem 后运行）
#
# import deepchem as dc
# from deepchem.feat import CircularFingerprint
#
# # 1. 数据集
# smiles = ["CC(=O)Oc1ccccc1C(=O)O", "CCO", ...]
# labels = [1, 0, ...]
# featurizer = CircularFingerprint(radius=2, size=2048)
# dataset = dc.data.NumpyDataset(X=featurizer.featurize(smiles), y=labels)
#
# # 2. 拆分
# train, valid, test = dc.splits.RandomSplitter().train_valid_test_split(dataset)
#
# # 3. 模型（多层感知机）
# model = dc.models.MultitaskClassifier(n_tasks=1, n_features=2048,
#                                       layer_sizes=[512, 256])
# model.fit(train, nb_epoch=50)
#
# # 4. 评估
# metric = dc.metrics.Metric(dc.metrics.roc_auc_score)
# print(model.evaluate(test, [metric]))
#
# # 5. 预测新分子
# preds = model.predict(featurizer.featurize(["COc1ccccc1"]))

# ============================================================
# 五、图神经网络（GNN）概念
# ============================================================
# 分子 = 图（原子=节点，键=边）
# GNN 直接把分子图喂给网络，逐层聚合邻居信息
#   比指纹的优势：自动学特征，能捕捉3D/立体信息
#
# 常见架构：
#   GCN（图卷积）
#   MPNN（消息传递网络）—— DeepChem 默认常用
#   AttentiveFP（注意力）
#   Weave（织物网络）
#   GraphConv

# ============================================================
# 六、公开数据集（做项目的资源）
# ============================================================
# MoleculeNet（DeepChem 内置基准）：
#   Tox21: 12种毒性终点（分类）
#   HIV: HIV病毒抑制（分类）
#   BACE: β-分泌酶抑制（回归/分类）
#   ESOL: 水溶性（回归）
#   FreeSolv: 溶剂化自由能（回归）
#   Lipophilicity: LogP（回归）
#
# 加载：
# tasks, datasets, transformers = dc.molnet.load_tox21()
# 或：dc.molnet.load_bace_classification()

# ============================================================
# 七、什么时候学 DeepChem？
# ============================================================
# ✅ 你已经会：sklearn + 指纹 QSAR
# ⏳ 下一步：DeepChem 图神经网络（等数据量需求出现时）
# ⏳ 再往后：Transformer-based 分子模型、蛋白语言模型
#
# 现阶段先把 sklearn + RDKit 的组合吃透（第15章），
# DeepChem 作为"第2梯队"学习，需要时再深入
