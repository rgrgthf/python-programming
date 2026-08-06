# ============================================================
# RDKit 进阶 ③ — 批量处理化合物数据库
# ============================================================
# 真实科研：几万到几百万个分子，需要批量处理。
# 这一节掌握：读写大文件、过滤、去重、加属性。

from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors as desc

# ============================================================
# 一、从 SDF 批量读分子
# ============================================================
# SDF = 标准药物数据格式（PubChem 可下载）
# 示例：生成几个分子并写入 SDF
mols = [Chem.MolFromSmiles(s) for s in [
    "CC(=O)Oc1ccccc1C(=O)O",
    "CC(C)Cc1ccc(cc1)C(C)C(=O)O",
    "COc1ccc2cc(ccc2c1)C(C)C(=O)O",
    "CC(=O)Nc1ccc(O)cc1",
]]
mols = [m for m in mols if m is not None]

w = Chem.SDWriter("test_library.sdf")
for m in mols:
    w.write(m)
w.close()

# 批量读取
supplier = Chem.SDMolSupplier("test_library.sdf")
print("总分子数：", len(supplier))
for mol in supplier:
    if mol is not None:    # ⚠️ 必须检查 None！
        print(Chem.MolToSmiles(mol))

# ============================================================
# 二、从 CSV/文本读 SMILES（最常见）
# ============================================================
# 药物数据库通常给 CSV：一行一个分子，第一列 SMILES
import csv

# 模拟一个 CSV 化合物库
with open("compound_lib.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["SMILES", "ID", "Name"])
    writer.writerow(["CC(=O)Oc1ccccc1C(=O)O", "C001", "阿司匹林"])
    writer.writerow(["CC(C)Cc1ccc(cc1)C(C)C(=O)O", "C002", "布洛芬"])
    writer.writerow(["CN1CCC23C4C1CC5=C2C(=C(C=C5)O)OC3C(C=C4)O", "C003", "吗啡"])

# 读 CSV → 转分子
compounds = []
with open("compound_lib.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        mol = Chem.MolFromSmiles(row["SMILES"])
        if mol is not None:
            mol.SetProp("_Name", row["Name"])
            mol.SetProp("ID", row["ID"])
            compounds.append(mol)

print(f"成功解析 {len(compounds)} 个分子")

# ============================================================
# 三、批量计算属性并写回
# ============================================================
# 给每个分子计算描述符，附到 SDF 属性里
w = Chem.SDWriter("annotated.sdf")
for mol in compounds:
    mol.SetProp("MW", f"{Descriptors.MolWt(mol):.2f}")
    mol.SetProp("LogP", f"{Descriptors.MolLogP(mol):.2f}")
    mol.SetProp("HBD", str(Descriptors.NumHDonors(mol)))
    mol.SetProp("HBA", str(Descriptors.NumHAcceptors(mol)))
    w.write(mol)
w.close()
print("已保存 annotated.sdf（带MW/LogP/HBD/HBA属性）")

# 读回验证属性
for mol in Chem.SDMolSupplier("annotated.sdf"):
    print(mol.GetProp("_Name"), "MW=", mol.GetProp("MW"))

# ============================================================
# 四、过滤和去重
# ============================================================
# ① 去重：同一分子不同SMILES写法 → 规范SMILES后去重
seen = set()
unique = []
for mol in compounds:
    canon = Chem.MolToSmiles(mol)     # 规范SMILES
    if canon not in seen:
        seen.add(canon)
        unique.append(mol)
print(f"去重后：{len(unique)} 个")

# ② 按属性过滤（类药性初筛）
drug_like = []
for mol in compounds:
    mw = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)
    if mw < 500 and -2 < logp < 5:     # 五规则简化版
        drug_like.append(mol)
print(f"类药性过滤后：{len(drug_like)} 个")

# ③ 排除含特定基团的分子（如排除含硝基）
nitro = Chem.MolFromSmarts("[NX3](=O)=O")
safe = [m for m in compounds if not m.HasSubstructMatch(nitro)]
print(f"排除硝基后：{len(safe)} 个")

# ============================================================
# 五、真实数据库源（了解）
# ============================================================
# PubChem（最大免费库）：pubchem.ncbi.nlm.nih.gov
#   - 可下载 SDF/CSV，几十亿化合物
# ZINC：zinc.docking.org（虚拟筛选专用）
# ChEMBL：www.ebi.ac.uk/chembl（生物活性数据，QSAR常用）
# DrugBank：go.drugbank.com（药物信息）
# 中国药典/药智网：中文化合物数据
#
# 后续做虚拟筛选项目时，从这里下载数据集

# ============================================================
# 六、性能提示（处理大库）
# ============================================================
# 几万分子：直接循环没问题
# 百万分子：
#   1. 用 SMILES 而不是 SDF（解析快）
#   2. 用惰性读取（SDMolSupplier 本来就是惰性的）
#   3. 提前过滤无效 SMILES
#   4. 并行处理（multiprocessing，进阶）
#   5. 描述符预计算并缓存
