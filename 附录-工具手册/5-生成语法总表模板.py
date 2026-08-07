# -*- coding: utf-8 -*-
# ============================================================
# 生成《Python 语法与函数总表》xlsx 模板
# ============================================================
# 用法：python 5-生成语法总表模板.py
# 作用：生成一个带格式的 Excel 模板，分章节分组，供你填写
#       （这个脚本用到的 openpyxl 就是第23章要学的库！）
# 说明：内容由你自己填，表格骨架老师帮你搭好。
# ============================================================

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from pathlib import Path

# ---- 章节列表（按学习顺序）----
chapters = [
    "第1章 Git 与 GitHub",
    "第2章 输入输出与基础语法",
    "第3章 数据类型与运算符",
    "第4章 流程控制",
    "第5章 数据结构",
    "第6章 函数",
    "第7章 文件与异常处理",
    "第8章 面向对象与模块",
]

ROWS_PER_CHAPTER = 10   # 每章预留的空行数（不够可以自己在Excel里插行）

# ---- 样式定义（VS Code 同款：代码=Consolas，中文=微软雅黑）----
CODE_FONT = "Consolas"              # 英文/代码用（等宽，和 VS Code 代码一样）
CN_FONT = "Microsoft YaHei"         # 中文用（和 VS Code 中文一样，圆润好看）
title_font = Font(bold=True, size=16, name=CN_FONT)
header_font = Font(bold=True, size=12, color="FFFFFF", name=CN_FONT)
header_fill = PatternFill("solid", fgColor="4472C4")     # 表头蓝
chapter_font = Font(bold=True, size=11, color="FFFFFF", name=CN_FONT)
chapter_fill = PatternFill("solid", fgColor="70AD47")    # 章节绿
thin = Side(style="thin", color="BBBBBB")
border = Border(left=thin, right=thin, top=thin, bottom=thin)
center = Alignment(horizontal="center", vertical="center", wrap_text=True)
left = Alignment(horizontal="left", vertical="center", wrap_text=True)

# ---- 建工作簿 ----
wb = Workbook()
ws = wb.active
ws.title = "语法总表"

# 标题行（合并 A1:C1）
ws.merge_cells("A1:C1")
ws["A1"] = "Python 语法与函数总表（第1~8章）"
ws["A1"].font = title_font
ws["A1"].alignment = center
ws.row_dimensions[1].height = 30

# 表头行
headers = ["语法", "作用", "示例"]
for col, h in enumerate(headers, start=1):
    c = ws.cell(row=2, column=col, value=h)
    c.font = header_font
    c.fill = header_fill
    c.alignment = center
    c.border = border
ws.row_dimensions[2].height = 22

# 逐章：章节分组行 + 预留空行
r = 3
for ch in chapters:
    # 章节分组行（合并横跨3列，整行显示章节名）
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
    c = ws.cell(row=r, column=1, value=ch)
    c.font = chapter_font
    c.fill = chapter_fill
    c.alignment = center
    ws.row_dimensions[r].height = 20
    r += 1

    # 预留空行：A/C列(语法/示例)=代码等宽，B列(作用)=中文雅黑
    for _ in range(ROWS_PER_CHAPTER):
        for col in range(1, 4):
            cell = ws.cell(row=r, column=col)
            cell.border = border
            cell.alignment = left
            cell.font = Font(name=CODE_FONT if col != 2 else CN_FONT)
        r += 1

# 列宽（语法 / 作用 / 示例）
ws.column_dimensions["A"].width = 28
ws.column_dimensions["B"].width = 45
ws.column_dimensions["C"].width = 40

# ---- 保存到本脚本同目录 ----
out = Path(__file__).parent / "Python语法总表.xlsx"
wb.save(out)
print(f"✅ 模板已生成：{out}")
print("接下来：用 Excel/WPS 打开，在每章的绿色标题行下面填写")
