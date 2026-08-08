# ============================================================
# Web 开发入门 ① — Flask 基础
# ============================================================
# ⚠️ 需要安装：pip install flask
# 你已经会 Python 了，Web 开发其实不难：
# Flask = 用 Python 写"网页后端"的最简框架。
# 学了它，可以做出"药物查询网站/API"这样的作品。

from flask import Flask, jsonify, request

# 创建应用
app = Flask(__name__)

# ============================================================
# 一、第一个路由（网页）
# ============================================================
@app.route("/")
def home():
    return "<h1>欢迎来到我的药物数据库</h1><p>这是一个 Flask 应用</p>"

# 带参数的 URL
@app.route("/drug/<name>")
def drug_page(name):
    return f"<h1>{name}</h1><p>这是 {name} 的详情页</p>"

# 运行方式：python 1-Flask基础.py
# 浏览器访问 http://127.0.0.1:5000/
#           http://127.0.0.1:5000/drug/阿司匹林

# ============================================================
# 二、JSON API（给程序用，不是给人看）
# ============================================================
# 模拟药物数据库（实际会用 SQLite，第29章）
DRUGS = {
    "aspirin": {"名称": "阿司匹林", "CID": 2244, "分子量": 180.16},
    "ibuprofen": {"名称": "布洛芬", "CID": 3672, "分子量": 206.28},
    "paracetamol": {"名称": "对乙酰氨基酚", "CID": 1983, "分子量": 151.16},
}

# GET /api/drugs → 返回所有药物
@app.route("/api/drugs")
def list_drugs():
    return jsonify(DRUGS)

# GET /api/drugs/<name> → 返回单个药物
@app.route("/api/drugs/<name>")
def get_drug(name):
    drug = DRUGS.get(name)
    if drug is None:
        return jsonify({"error": "未找到该药物"}), 404
    return jsonify(drug)

# POST /api/drugs → 添加药物（用 request.json 拿数据）
@app.route("/api/drugs", methods=["POST"])
def add_drug():
    data = request.json
    if not data or "name" not in data:
        return jsonify({"error": "缺少name字段"}), 400
    DRUGS[data["name"]] = data
    return jsonify({"message": "添加成功", "drug": data}), 201

# ============================================================
# 三、查询参数（?keyword=xxx）
# ============================================================
@app.route("/api/search")
def search():
    keyword = request.args.get("keyword", "")
    # 模糊匹配
    results = {k: v for k, v in DRUGS.items() if keyword in v["名称"]}
    return jsonify(results)

# ============================================================
# 四、测试这个 API（先运行再测试）
# ============================================================
# 运行本文件后，用浏览器或 requests 测试：
#   GET  http://127.0.0.1:5000/api/drugs
#   GET  http://127.0.0.1:5000/api/drugs/aspirin
#   GET  http://127.0.0.1:5000/api/search?keyword=布
#   POST http://127.0.0.1:5000/api/drugs
#         {"name": "loratadine", "名称": "氯雷他定", "CID": 3957}

# 用 requests 测试（第26章学的）：
# import requests
# resp = requests.get("http://127.0.0.1:5000/api/drugs")
# print(resp.json())

# ============================================================
# 五、启动方式与调试模式
# ============================================================
if __name__ == "__main__":
    app.run(debug=True, port=5000)
    # debug=True：改代码自动重启 + 出错显示详情
    # 生产环境不要用 debug=True！

# ============================================================
# 六、Web 开发概念扫盲
# ============================================================
# 前端：用户看到的（HTML/CSS/JS）—— 网页长得什么样
# 后端：处理数据的（Flask/FastAPI）—— 逻辑和数据库
# API：后端给程序用的接口（返回 JSON）
# 路由：URL 和函数的对应关系（@app.route）
# 请求方法：GET(拿数据) / POST(提交数据) / PUT(改) / DELETE(删)

# ============================================================
# 七、总结
# ============================================================
# @app.route("/路径") 定义路由
# 返回 HTML：return "<h1>..."
# 返回 JSON：jsonify(字典)
# 取参数：URL变量/<name>、request.args、request.json
# 启动：app.run(debug=True)
# 下一步：连数据库（第29章）→ 做完整药物查询网站

# ============================================================
# 五、易错点汇总
# ============================================================
# 1. 路由用 @app.route("/路径")，函数返回的是响应内容
# 2. 动态参数用 <name>：@app.route("/drug/<id>")
# 3. app.run(debug=True) 改代码自动重启，但生产环境要关掉 debug
# 4. 返回 JSON 用 jsonify()，返回网页用 render_template()
# 5. 改完代码要重启服务器才生效（debug 模式除外）
# 6. 端口默认 5000，被占用要改 app.run(port=xxx)

# ============================================================
# 六、自测（40%基础 + 40%中等 + 20%挑战）
# ============================================================
# 【基础】
# 1. 路由和视图函数的关系？
# 2. 动态路径参数怎么定义？
# 3. debug=True 的作用？
#
# 【中等】
# 4. 创建一个 Flask 应用，根路径返回"Hello"。
# 5. 加一个 /drug/<id> 路由返回药品信息 JSON。
# 6. 修改端口启动服务。
#
# 【挑战】
# 7. 做一个简单的药物查询页面（路由+返回信息）。
# 8. 解释为什么生产环境要关 debug。
