# ============================================================
# Web 开发入门 ② — 实战：药物查询 API + 前端页面
# ============================================================
# ⚠️ 需要安装：pip install flask
# 综合实战：做一个"药物信息查询"小应用——
# 网页输入药物名 → 从 PubChem 拿真实数据 → 网页展示。
# 这是能放进作品集的完整项目！

from flask import Flask, jsonify, request, render_template_string
import requests

app = Flask(__name__)

# ============================================================
# 一、前端页面（HTML模板）
# ============================================================
PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>药物信息查询</title>
    <style>
        body { font-family: 'Microsoft YaHei', sans-serif; max-width: 700px;
               margin: 40px auto; padding: 20px; }
        input, button { padding: 10px; font-size: 16px; }
        input { width: 300px; }
        .card { border: 1px solid #ddd; border-radius: 8px;
                padding: 20px; margin-top: 20px; }
        table { border-collapse: collapse; width: 100%; }
        td, th { border: 1px solid #ddd; padding: 8px; text-align: left; }
        .error { color: red; }
    </style>
</head>
<body>
    <h1>🔬 药物信息查询</h1>
    <form method="GET">
        <input type="text" name="drug" placeholder="输入药物英文名，如 aspirin">
        <button type="submit">查询</button>
    </form>

    {% if drug %}
        {% if info %}
        <div class="card">
            <h2>{{ info['名称'] }}（CID: {{ info['CID'] }}）</h2>
            <table>
                <tr><th>分子式</th><td>{{ info['分子式'] }}</td></tr>
                <tr><th>分子量</th><td>{{ info['分子量'] }}</td></tr>
                <tr><th>SMILES</th><td>{{ info['SMILES'] }}</td></tr>
            </table>
        </div>
        {% else %}
        <p class="error">未找到 "{{ drug }}" 的信息，请检查英文拼写。</p>
        {% endif %}
    {% endif %}
</body>
</html>
"""

# ============================================================
# 二、核心逻辑：调用 PubChem API
# ============================================================
def fetch_pubchem(name):
    """从 PubChem 获取药物信息"""
    # 名称 → CID
    url1 = (f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/"
            f"name/{name}/cids/JSON")
    try:
        r1 = requests.get(url1, timeout=15)
        if r1.status_code != 200:
            return None
        cid = r1.json()["IdentifierList"]["CID"][0]

        # CID → 性质
        url2 = (f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}"
                f"/property/MolecularFormula,MolecularWeight,"
                f"CanonicalSMILES/JSON")
        r2 = requests.get(url2, timeout=15)
        if r2.status_code != 200:
            return None

        prop = r2.json()["PropertyTable"]["Properties"][0]
        return {
            "名称": name.capitalize(),
            "CID": cid,
            "分子式": prop.get("MolecularFormula", ""),
            "分子量": prop.get("MolecularWeight", ""),
            "SMILES": prop.get("CanonicalSMILES", ""),
        }
    except Exception:
        return None

# ============================================================
# 三、两个路由：网页 + JSON API
# ============================================================
# 网页版（给人看）
@app.route("/")
def home():
    drug = request.args.get("drug", "").strip()
    info = fetch_pubchem(drug) if drug else None
    return render_template_string(PAGE, drug=drug, info=info)

# API版（给程序用）
@app.route("/api/drug/<name>")
def api_drug(name):
    info = fetch_pubchem(name)
    if info is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(info)

# ============================================================
# 四、运行与测试
# ============================================================
if __name__ == "__main__":
    print("启动药物查询服务：http://127.0.0.1:5000")
    app.run(debug=True, port=5000)

# 使用方法：
#   1. 运行本文件
#   2. 浏览器打开 http://127.0.0.1:5000
#   3. 输入 aspirin 查询
#   4. API：http://127.0.0.1:5000/api/drug/ibuprofen
#
# 扩展思路：
#   - 接上 SQLite 缓存查询结果（第29章）
#   - 加 RDKit 计算类药性（展示更专业）
#   - 支持批量查询多个药物
#   - 部署到服务器（flask 部署教程）

# ============================================================
# 五、Web 项目的工程化规范
# ============================================================
# 真实项目结构（不是单文件）：
#   project/
#   ├── app.py            # 主程序
#   ├── static/           # CSS/JS/图片
#   ├── templates/        # HTML模板
#   ├── data/             # 数据
#   └── tests/            # 测试（第24章学的）
#
# 部署上线（了解）：
#   - 本地：app.run()
#   - 生产：gunicorn/等待服务器 + nginx
#   - 或者用 Streamlit/Gradio 做数据展示（更省事）

# ============================================================
# 六、总结
# ============================================================
# 完整链路：网页输入 → Flask路由 → 请求PubChem → 渲染展示
# 双接口：网页(render_template) + API(jsonify)
# 作品集：这个项目 = 网络请求 + Web开发 + 药学数据
# 下一步：数据库持久化 → 部署上线
