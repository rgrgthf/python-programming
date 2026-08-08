# ============================================================
# 网络请求 ② — 实战：调用科学数据库 API
# ============================================================
# ⚠️ 需要联网
# 真实场景：批量查询 PubChem（化合物数据库）获取分子信息。
# 这是"药学 + Python"的经典应用，也是作品集好素材。

import requests
import time

# ============================================================
# 一、PubChem 常用 API 一览
# ============================================================
# 名称 → CID：
#   /rest/pug/compound/name/阿司匹林/cids/JSON
# CID → 分子式/分子量：
#   /rest/pug/compound/cid/2244/property/MolecularFormula,MolecularWeight/JSON
# CID → SMILES：
#   /rest/pug/compound/cid/2244/property/CanonicalSMILES/JSON
# CID → 3D结构文件：
#   /rest/pug/compound/cid/2244/record/SDF?record_type=3d

# ============================================================
# 二、查询一个化合物的完整信息
# ============================================================
def query_compound(name):
    """按名称查询化合物的关键信息"""
    # 1. 名称 → CID
    url1 = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/cids/JSON"
    r1 = requests.get(url1, timeout=15)
    if r1.status_code != 200:
        print(f"查不到 {name}")
        return None
    cid = r1.json()["IdentifierList"]["CID"][0]
    print(f"{name} 的 CID: {cid}")

    # 2. CID → 分子式、分子量、SMILES
    url2 = (f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}"
            f"/property/MolecularFormula,MolecularWeight,CanonicalSMILES/JSON")
    r2 = requests.get(url2, timeout=15)
    if r2.status_code != 200:
        print("获取性质失败")
        return None

    prop = r2.json()["PropertyTable"]["Properties"][0]
    return {
        "名称": name,
        "CID": cid,
        "分子式": prop.get("MolecularFormula", ""),
        "分子量": prop.get("MolecularWeight", ""),
        "SMILES": prop.get("CanonicalSMILES", ""),
    }

# 查询阿司匹林（注意：名称要英文，中文会失败）
# info = query_compound("aspirin")
# if info:
#     for k, v in info.items():
#         print(f"  {k}: {v}")

# ============================================================
# 三、批量查询多个化合物（带礼貌延迟）
# ============================================================
def batch_query(names, delay=0.5):
    """批量查询，间隔 delay 秒（尊重服务器）"""
    results = []
    for name in names:
        info = query_compound(name)
        if info:
            results.append(info)
        time.sleep(delay)       # 每次查询之间休息，避免被封
    return results

# 批量查 3 个常见药
drug_names = ["aspirin", "ibuprofen", "paracetamol"]
# drugs = batch_query(drug_names)
# for d in drugs:
#     print(d)

# ============================================================
# 四、把结果整理成表格（pandas）
# ============================================================
import pandas as pd

def to_dataframe(results):
    """查询结果转 DataFrame"""
    return pd.DataFrame(results)

# df = to_dataframe(drugs)
# print(df)
# 可以把 df 存成 Excel：df.to_excel("药物信息.xlsx", index=False)

# ============================================================
# 五、结合 RDKit 做进一步分析（你的专属优势！）
# ============================================================
# 拿到 SMILES 后 → 用 RDKit 计算描述符 → 类药性分析
# 这就是"网络取数 + 本地分析"的完整工作流：
#   1. requests 从 PubChem 拿 SMILES
#   2. RDKit 解析并计算分子描述符
#   3. 做类药五规则筛选
#   4. 存成数据集

# 示意（需 sci 环境 + rdkit）：
"""
from rdkit import Chem
from rdkit.Chem import Descriptors

def analyze_smiles(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    return {
        "MW": Descriptors.MolWt(mol),
        "LogP": Descriptors.MolLogP(mol),
        "HBD": Descriptors.NumHDonors(mol),
        "HBA": Descriptors.NumHAcceptors(mol),
    }
"""

# ============================================================
# 六、API 使用注意事项（礼貌与合规）
# ============================================================
# 1. 控制频率：批量查询加 time.sleep 间隔
# 2. 设置超时：timeout=15 避免卡死
# 3. 检查状态码：!=200 要处理
# 4. 遵守网站使用条款：个人学习用途没问题
# 5. 缓存结果：查过一次存本地，别重复查
#    → 把结果存 Excel/CSV，下次直接用

# ============================================================
# 七、其他药学相关 API（扩展了解）
# ============================================================
# UniProt（蛋白质）：https://rest.uniprot.org/
# ChEMBL（生物活性）：https://www.ebi.ac.uk/chembl/api/data/
# DrugBank（药物）：需要注册申请
# RCSB PDB（蛋白结构）：https://data.rcsb.org/rest/v1/
# NCBI（文献/基因）：https://eutils.ncbi.nlm.nih.gov/entrez/eutils/

# ============================================================
# 八、总结
# ============================================================
# 查询流程：名称→CID→性质
# 批量查询：循环 + time.sleep 间隔
# 结果处理：pandas 整理 + RDKit 分析
# 数据落地：存 Excel 复用（不重复请求）
# 价值：自动建化合物数据库！作品集高质量项目素材

# ============================================================
# 六、易错点汇总
# ============================================================
# 1. API 参数用 params= 字典传，别手拼 URL（易错/易注入）
# 2. 批量请求加【限速】（time.sleep）和异常重试
# 3. 数据量大时分批取，别一次全拉
# 4. 把取到的数据【存下来】（JSON/CSV），别只打印
# 5. 记录 API 的 key/凭证别硬编码在代码里，用环境变量
# 6. 遵守 API 文档的调用规范（频率、字段、引用）

# ============================================================
# 七、自测（40%基础 + 40%中等 + 20%挑战）
# ============================================================
# 【基础】
# 1. 传参用 params= 还是手拼 URL？为什么？
# 2. 批量请求为什么要限速？
# 3. 取到的数据应该怎么处理？
#
# 【中等】
# 4. 用 PubChem API 查询一个化合物的数据。
# 5. 给批量请求加重试和 sleep。
# 6. 把查询结果保存成 JSON/CSV。
#
# 【挑战】
# 7. 批量查询多个化合物并建成一个小数据库文件。
# 8. 解释 API 凭证为什么要用环境变量而不是写死。
