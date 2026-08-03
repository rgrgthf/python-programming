# ============================================================
# 实战：学生成绩管理系统（文件 + 函数 + 数据结构 + 异常处理）
# ============================================================
# 综合运用前六章 + 第七章的知识：
#   函数、列表/字典、文件读写、异常处理、循环菜单
# ============================================================

import os

FILE = "scores.txt"     # 数据文件

# ============================================================
# 一、保存成绩到文件
# ============================================================
def save_scores(scores):
    """把字典 {姓名: 分数} 写入文件"""
    with open(FILE, "w", encoding="utf-8") as f:
        for name, score in scores.items():
            f.write(f"{name},{score}\n")   # 每行：姓名,分数

# ============================================================
# 二、从文件读取成绩
# ============================================================
def load_scores():
    """从文件读取成绩，返回字典；文件不存在返回空字典"""
    scores = {}
    if not os.path.exists(FILE):
        return scores
    with open(FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:                          # 跳过空行
                name, score = line.split(",")  # 按逗号拆分
                scores[name] = int(score)
    return scores

# ============================================================
# 三、主菜单
# ============================================================
def main():
    scores = load_scores()    # 启动时读取已有数据

    while True:
        print("\n===== 成绩管理系统 =====")
        print("1. 添加成绩")
        print("2. 查看所有成绩")
        print("3. 统计平均分/最高分")
        print("4. 退出")
        choice = input("请选择：")

        if choice == "1":
            name = input("姓名：")
            try:
                score = int(input("分数："))
            except ValueError:
                print("分数必须是数字！")
                continue
            scores[name] = score
            save_scores(scores)          # 立即保存
            print(f"已添加 {name}：{score} 分")

        elif choice == "2":
            if not scores:
                print("还没有成绩记录")
            else:
                for name, score in scores.items():
                    print(f"{name}：{score} 分")

        elif choice == "3":
            if not scores:
                print("还没有成绩记录")
            else:
                values = list(scores.values())
                print(f"平均分：{sum(values) / len(values):.1f}")
                best = max(scores, key=scores.get)
                print(f"最高分：{best}，{scores[best]} 分")

        elif choice == "4":
            print("再见！")
            break

        else:
            print("无效选择，请重试")

if __name__ == "__main__":
    main()
# ============================================================
# 运行说明：
# 1. 直接运行这个文件，会出现菜单
# 2. 数据保存在 scores.txt，下次运行还在！
# 3. 这就是一个"最小可用的数据管理系统"
# ============================================================
