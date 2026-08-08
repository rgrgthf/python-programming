# ============================================================
# 爬虫实战 ① — BeautifulSoup 网页解析
# ============================================================
# ⚠️ 需要安装：pip install beautifulsoup4 requests
# 爬虫 = 程序自动获取网页数据。
# 流程：requests 拿网页 → BeautifulSoup 解析 → 提取数据。
# 声明：仅学习用途，爬取公开数据，遵守 robots 协议和网站条款。

from bs4 import BeautifulSoup
import requests

# ============================================================
# 一、解析 HTML 的基本方法
# ============================================================
# 示例 HTML（模拟网页内容）
html = """
<html>
<head><title>药学实验报告</title></head>
<body>
  <h1 class="main-title">实验数据总览</h1>
  <div id="content">
    <p class="sample">样品A：浓度 0.5 mg/mL</p>
    <p class="sample">样品B：浓度 1.0 mg/mL</p>
    <p>对照组：无</p>
  </div>
  <table>
    <tr><th>样品</th><th>浓度</th></tr>
    <tr><td>A</td><td>0.5</td></tr>
    <tr><td>B</td><td>1.0</td></tr>
  </table>
</body>
</html>
"""

soup = BeautifulSoup(html, "html.parser")

# ① 找单个元素
print(soup.title.text)                  # → 药学实验报告
print(soup.h1.text)                     # → 实验数据总览
print(soup.find("h1").text)             # 同上方

# ② 按 class 找（CSS选择器）
samples = soup.find_all("p", class_="sample")
for s in samples:
    print(s.text)                       # → 样品A：... / 样品B：...

# ③ 按 id 找
content = soup.find(id="content")
print(content.find_all("p"))            # 找 content 里的所有 p

# ④ CSS 选择器（更强大）
print(soup.select(".sample"))           # class=样
print(soup.select("#content p"))        # id=content 里的 p

# ⑤ 表格解析
rows = soup.select("table tr")
for row in rows[1:]:                    # 跳过表头
    cells = [td.text for td in row.find_all("td")]
    print(cells)                        # → ['A', '0.5'] ...

# ============================================================
# 二、requests + BeautifulSoup 完整流程
# ============================================================
def fetch_and_parse(url):
    """获取网页并解析（示例：只做结构演示）"""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding   # 处理中文编码
        soup = BeautifulSoup(resp.text, "html.parser")
        return soup
    except Exception as e:
        print(f"获取失败: {e}")
        return None

# 真实爬取示例（公共网站）：
# soup = fetch_and_parse("https://example.com")
# 然后 soup.find_all(...) 提取内容

# ============================================================
# 三、提取数据的常用技巧
# ============================================================
# ① 提取所有链接
# for a in soup.find_all("a", href=True):
#     print(a["href"], a.text)

# ② 提取图片
# for img in soup.find_all("img"):
#     print(img.get("src"))

# ③ 提取属性
# print(soup.find("h1")["class"])

# ④ 正则配合（第9章学的！）
import re
# text = soup.get_text()
# emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)

# ============================================================
# 四、爬虫的"三个守则"
# ============================================================
# 1. 守法：只爬公开数据，遵守 robots.txt 和网站条款
# 2. 礼貌：控制频率（time.sleep），别给服务器压力
# 3. 节制：只取需要的，别贪多
#
# 药学场景其实用 API 更多（PubChem 等有正规 API），
# 爬虫主要用于：没有 API 的网站、快速看网页结构。
# 科学数据库优先用 API（第26章），不推荐爬它们。

# ============================================================
# 五、总结
# ============================================================
# 解析：BeautifulSoup(html, "html.parser")
# 查找：find / find_all / select(CSS选择器)
# 文本：元素.text 属性：元素["属性名"]
# 流程：requests 拿 → soup 解析 → 提取 → 存数据
# 守则：守法、礼貌、节制

# ============================================================
# 五、易错点汇总
# ============================================================
# 1. BeautifulSoup 只负责【解析】，抓取还是 requests 干
# 2. 标签用 soup.find / soup.find_all；
#    find 返回第一个，find_all 返回列表
# 3. 取文本用 .text（或 get_text），取属性用 .get("href")
# 4. 网页编码不对会乱码：先看 meta 或设 resp.encoding
# 5. 爬取前检查 robots.txt，遵守网站规矩
# 6. 频率别太高，带 User-Agent，尊重站点

# ============================================================
# 六、自测（40%基础 + 40%中等 + 20%挑战）
# ============================================================
# 【基础】
# 1. 抓取和解析分别由谁负责？
# 2. find 和 find_all 的区别？
# 3. 取标签文本和属性分别用什么？
#
# 【中等】
# 4. 用 requests 抓一个页面，用 BeautifulSoup 提取标题。
# 5. 提取页面上所有链接的 href。
# 6. 处理网页乱码（设置 encoding）。
#
# 【挑战】
# 7. 爬取一个表格页并提取其中的数据行。
# 8. 解释爬虫的"守法、礼貌、节制"三原则具体指什么。
