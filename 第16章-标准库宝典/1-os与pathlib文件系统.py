# ============================================================
# 标准库宝典 ① — os 与 pathlib（文件系统操作）
# ============================================================
# 处理实验数据的第一步往往是"整理一堆文件"。
# os 和 pathlib 就是干这个的——批量操作文件和文件夹。

import os
from pathlib import Path

# ============================================================
# 一、pathlib（推荐！更现代、更好用）
# ============================================================
# Path 对象 = 路径的"面向对象"表示
p = Path("C:/Users/22239/Python药学学习体系/第18章-pandas数据分析")
print(p.exists())        # 是否存在 → True
print(p.is_dir())        # 是文件夹吗
print(p.name)            # → 第18章-pandas数据分析（最后一部分）
print(p.parent)          # 父路径
print(p.stem)            # 去掉后缀的主名
print(p.suffix)          # 后缀（.py 等）

# 拼接路径（不用管 / 还是 \）
data_file = p / "1-pandas入门-读取数据.py"
print(data_file)         # → ...\1-pandas入门-读取数据.py

# ============================================================
# 二、目录操作
# ============================================================
# 创建目录（mkdir parents=True 连父目录一起建，exist_ok 不报错）
Path("test_dir/sub/a").mkdir(parents=True, exist_ok=True)

# 列出目录内容
for item in Path(".").iterdir():
    print(item.name, "📁" if item.is_dir() else "📄")

# 通配符匹配
py_files = list(Path(".").glob("*.py"))
print(f"当前目录有 {len(py_files)} 个py文件")

# 递归匹配
# all_py = list(Path(".").rglob("*.py"))

# ============================================================
# 三、文件操作
# ============================================================
# 读写文件（Path 自带，比 open 简洁）
f = Path("test.txt")
f.write_text("实验数据：0.523\n", encoding="utf-8")
content = f.read_text(encoding="utf-8")
print(content)

# 删除/重命名
# f.rename("test2.txt")
# f.unlink()          # 删除文件
# Path("test_dir").rmdir()   # 删除空目录

# ============================================================
# 四、os 模块（经典写法，兼容老代码）
# ============================================================
# os.path 是 pathlib 出现前的老方式，读老代码会遇到
print(os.path.exists("test.txt"))          # → True
print(os.path.join("a", "b", "c.py"))      # → a\b\c.py
print(os.path.basename("a/b/c.py"))        # → c.py
print(os.path.dirname("a/b/c.py"))         # → a/b
print(os.path.splitext("data.csv"))        # → ('data', '.csv')

# 环境变量
print(os.environ.get("USERNAME"))          # 当前用户名

# 当前工作目录
print(os.getcwd())

# ============================================================
# 五、shutil：复制/移动/压缩
# ============================================================
import shutil

# 复制文件
# shutil.copy("test.txt", "backup.txt")

# 复制整个目录
# shutil.copytree("test_dir", "test_dir_backup")

# 移动
# shutil.move("backup.txt", "test_dir/backup.txt")

# 压缩打包（备份实验数据神器！）
# shutil.make_archive("data_backup", "zip", "test_dir")

# ============================================================
# 六、实战：批量重命名实验文件
# ============================================================
# 场景：仪器导出的文件叫 result_01.dat ~ result_50.dat
#       想统一改成 样品_日期_编号.dat
# 先创建几个测试文件
for i in range(1, 4):
    Path(f"result_{i:02d}.dat").write_text("data", encoding="utf-8")

# 批量重命名
count = 0
for f in Path(".").glob("result_*.dat"):
    num = f.stem.split("_")[1]          # 取出编号
    new_name = f"样品_20260806_{num}.dat"
    f.rename(Path(f.parent) / new_name)
    count += 1
print(f"重命名了 {count} 个文件")

# 批量移动相同类型文件到文件夹
# Path("归档").mkdir(exist_ok=True)
# for f in Path(".").glob("*.dat"):
#     shutil.move(str(f), "归档/" + f.name)

# ============================================================
# 七、实战：统计文件夹大小/文件数
# ============================================================
def folder_stats(folder):
    """统计文件夹里的文件数和总大小"""
    files = list(Path(folder).rglob("*"))
    total_size = sum(f.stat().st_size for f in files if f.is_file())
    n_files = sum(1 for f in files if f.is_file())
    return n_files, total_size / 1024

n, size_kb = folder_stats("第18章-pandas数据分析")
print(f"该文件夹：{n} 个文件，共 {size_kb:.1f} KB")

# 清理测试文件
for f in Path(".").glob("样品_*.dat"):
    f.unlink()
Path("test.txt").unlink()
shutil.rmtree("test_dir", ignore_errors=True)

# ============================================================
# 总结
# ============================================================
# 日常优先用 pathlib（Path 对象，更现代）
# os.path 读老代码要用；shutil 负责复制/移动/压缩
# 批量处理文件 = glob 匹配 + 循环 + rename/move
