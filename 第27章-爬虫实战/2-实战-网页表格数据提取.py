# ============================================================
# 爬虫实战 ② — 实战：提取网页表格数据
# ============================================================
# ⚠️ 需要联网 + beautifulsoup4
# 真实场景：从公开网页抓取表格数据（如药品说明书网站、
# 学术数据表格），解析成结构化数据保存。
# 示例用 Python 官方文档页面（稳定公开，学习用）。

import requests
from bs4 import BeautifulSoup
import pandas as pd

# ============================================================
# 一、抓取 Python 标准库列表页
# ============================================================
def fetch_stdlib_modules():
    """从 Python 官方文档抓取内置模块列表"""
    url = "https://docs.python.org/3/py-modindex.html"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding
    soup = BeautifulSoup(resp.text, "html.parser")

    # 官方文档模块列表在 <code class="xref"> 里
    modules = []
    for code in soup.select("code.xref"):
        name = code.get_text().strip()
        if name and name not in modules:
            modules.append(name)
    return modules

# modules = fetch_stdlib_modules()
# print(f"共找到 {len(modules)} 个模块")
# print(modules[:20])     # 前20个

# ============================================================
# 二、解析表格（最常用的爬虫任务）
# ============================================================
# 示例：本地构造一个 HTML 表格来演示解析（避免依赖外部网站）
html_table = """
<table>
  <thead>
    <tr><th>药品</th><th>规格</th><th>价格(元)</th></tr>
  </thead>
  <tbody>
    <tr><td>阿司匹林</td><td>100mg×30片</td><td>12.5</td></tr>
    <tr><td>布洛芬</td><td>200mg×20粒</td><td>18.0</td></tr>
    <tr><td>氯雷他定</td><td>10mg×6片</td><td>22.8</td></tr>
  </tbody>
</table>
"""
soup = BeautifulSoup(html_table, "html.parser")

# 通用表格解析函数
def parse_table(soup):
    """把网页中的表格解析成列表"""
    headers = [th.get_text(strip=True) for th in soup.select("thead th")]
    rows = []
    for tr in soup.select("tbody tr"):
        cells = [td.get_text(strip=True) for td in tr.find_all("td")]
        rows.append(cells)
    return headers, rows

headers, rows = parse_table(soup)
print("表头:", headers)
print("数据:", rows)

# 转成 pandas DataFrame
df = pd.DataFrame(rows, columns=headers)
df["价格(元)"] = df["价格(元)"].astype(float)    # 转数值
print(df)
print(f"平均价格: {df['价格(元)'].mean():.1f} 元")

# ============================================================
# 三、把抓到的数据存下来
# ============================================================
# 存 CSV / Excel（第23章学的）
# df.to_csv("药品价格.csv", index=False, encoding="utf-8-sig")
# df.to_excel("药品价格.xlsx", index=False)

# ============================================================
# 四、真实网页爬取的套路总结
# ============================================================
# 1. 先看网页结构：浏览器 F12 开发者工具 → Elements
#   找到目标数据的标签和 class
# 2. 用 requests 获取 HTML
# 3. 用 soup.select("选择器") 提取
# 4. 整理成 pandas → 保存
#
# 遇到动态加载的网页（数据是 JS 生成的）：
#   1. 找它的 API 接口（Network 面板看请求）
#   2. 直接请求 API（更干净）
#   3. 或学 Selenium/Playwright（浏览器自动化，进阶）

# ============================================================
# 五、实战建议（老师的话）
# ============================================================
# 药学数据尽量走正规 API（PubChem/ChEMBL 等），
# 爬虫的价值在于：
#   1. 没有 API 的公开数据（新闻、文献列表、药价查询）
#   2. 自动化收集资料（作品集：自动抓取并整理药学资讯）
#   3. 理解 Web 技术（为第28章 Web 开发打基础）
#
# 做爬虫作品注意：
#   - 只爬公开数据
#   - 控制频率
#   - 标注数据来源
#   - 说明用途（学习/科研）

# ============================================================
# 六、总结
# ============================================================
# 表格解析：parse_table 通用函数（thead th + tbody tr td）
# 转结构：pandas DataFrame
# 落盘：to_csv / to_excel
# 复杂网页：F12 分析 → 找 API 或用浏览器自动化
# 守则：守法、礼貌、节制、标来源

# ============================================================
# 六、易错点汇总
# ============================================================
# 1. 表格数据：先定位 <table>，再遍历 <tr> 行、<td> 单元格
# 2. 用 pandas 的 pd.read_html(html) 可以直接读表格（神器！）
# 3. 网页结构常变：爬虫可能"突然失效"，要处理异常
# 4. 数据清洗：提取的文本可能有空格/换行，要 strip()
# 5. 大量数据用 csv/DataFrame 存，别只打印
# 6. 标明数据来源、遵守版权和引用规范

# ============================================================
# 七、自测（40%基础 + 40%中等 + 20%挑战）
# ============================================================
# 【基础】
# 1. 表格由哪三个标签组成？
# 2. pandas 怎么直接读网页表格？
# 3. 提取的文本为什么要 strip()？
#
# 【中等】
# 4. 爬取一个网页表格并提取所有行。
# 5. 用 pd.read_html 读表格转成 DataFrame。
# 6. 给爬虫加异常处理和来源标注。
#
# 【挑战】
# 7. 完整爬取一个药品列表页，存成 CSV 数据库。
# 8. 解释为什么"标来源"是科研爬虫的底线。
