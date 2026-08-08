# ============================================================
# 网络请求 ① — requests 基础
# ============================================================
# ⚠️ 需要联网 + 安装：pip install requests
# requests 是 Python 最流行的 HTTP 请求库：
#   访问网页、调用 API（PubChem/UniProt 等科学数据库都有 API！）

import requests

# ============================================================
# 一、GET 请求（获取数据）
# ============================================================
# 基本用法
url = "https://httpbin.org/get"     # 测试用的示例网站
resp = requests.get(url)
print(resp.status_code)             # → 200（成功）
print(resp.url)                     # 实际请求的URL

# 带参数（查询参数）
params = {"q": "aspirin", "limit": 5}
resp = requests.get("https://httpbin.org/get", params=params)
print(resp.url)                     # URL 自动带上 ?q=aspirin&limit=5

# ============================================================
# 二、响应内容
# ============================================================
resp = requests.get("https://httpbin.org/get")

# 文本内容
print(resp.text[:100])              # 原始文本

# JSON 内容（API 通常返回 JSON）
data = resp.json()                  # 自动解析成字典/列表
print(data["url"])                  # 按字典取值

# 响应头
print(resp.headers.get("Content-Type"))

# ============================================================
# 三、POST 请求（提交数据）
# ============================================================
# 提交 JSON 数据
payload = {"name": "样品A", "value": 0.523}
resp = requests.post("https://httpbin.org/post", json=payload)
print(resp.json()["json"])          # 服务器回显的数据

# 提交表单数据
# resp = requests.post(url, data={"key": "value"})

# ============================================================
# 四、请求头与超时
# ============================================================
# 设置请求头（模拟浏览器，有些网站要求）
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "zh-CN",
}
resp = requests.get("https://httpbin.org/headers", headers=headers)

# 超时设置（重要！不设可能一直卡住）
try:
    resp = requests.get("https://httpbin.org/get", timeout=5)  # 5秒超时
except requests.Timeout:
    print("请求超时")

# ============================================================
# 五、错误处理（网络请求必须有）
# ============================================================
def safe_get(url, timeout=10):
    """安全的GET请求：处理各种异常"""
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()       # 状态码非200则抛异常
        return resp
    except requests.ConnectionError:
        print("连接失败（没网/地址错）")
    except requests.Timeout:
        print("请求超时")
    except requests.HTTPError as e:
        print(f"HTTP错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")
    return None

resp = safe_get("https://httpbin.org/get")
if resp:
    print("请求成功！")

# ============================================================
# 六、科学数据库 API 示例（重点！）
# ============================================================
# PubChem API：查化合物信息（纯GET，无需key）
# 示例：查询"阿司匹林"的CID
# 先查名称→CID：
url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/aspirin/cids/JSON"
resp = requests.get(url, timeout=15)
if resp.status_code == 200:
    data = resp.json()
    print("阿司匹林的 PubChem CID：", data["IdentifierList"]["CID"])

# ============================================================
# 七、requests 使用规范
# ============================================================
# 1. 永远设 timeout（防卡死）
# 2. 用 safe_get 模式处理异常
# 3. 尊重网站：控制请求频率（别狂刷）
# 4. 数据量大用流式：resp.iter_content()
# 5. 下载文件：
#    with open("文件.pdf", "wb") as f:
#        f.write(resp.content)

# ============================================================
# 八、总结
# ============================================================
# GET：requests.get(url, params=, headers=, timeout=)
# POST：requests.post(url, json=)
# 解析：resp.text / resp.json() / resp.status_code
# 异常：ConnectionError / Timeout / HTTPError
# 应用：科学数据库 API（PubChem/UniProt）批量取数据！

# ============================================================
# 五、易错点汇总
# ============================================================
# 1. 请求【必须设超时 timeout】，否则网络卡住程序就挂死
# 2. 请求要 try/except 捕获异常（连接失败/超时/404），
#    别让程序崩
# 3. 很多 API 要 headers（User-Agent/API key），
#    不带可能被拒绝
# 4. resp.json() 假设返回 JSON；
#    用 resp.status_code 先确认 200 再解析
# 5. 编码问题：resp.encoding 可能需要设 "utf-8"
# 6. 尊重 API 频率限制（rate limit），别猛刷

# ============================================================
# 六、自测（40%基础 + 40%中等 + 20%挑战）
# ============================================================
# 【基础】
# 1. 请求为什么要设 timeout？
# 2. resp.status_code 怎么用？
# 3. resp.json() 假设响应是什么格式？
#
# 【中等】
# 4. 用 requests.get 请求一个 API 并打印状态码。
# 5. 给请求加 headers（User-Agent）和超时。
# 6. 用 try/except 处理连接异常。
#
# 【挑战】
# 7. 写一个带重试和错误处理的通用请求函数。
# 8. 解释为什么 API 调用要尊重频率限制。
