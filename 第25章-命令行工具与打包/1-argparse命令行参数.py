# ============================================================
# 命令行工具与打包 ① — argparse 命令行参数
# ============================================================
# 让脚本支持"命令行参数"：
#   终端里：python 脚本.py --input 数据.xlsx --output 结果.xlsx
# 适合做"给实验室同事用的小工具"——不用改代码，参数外面传。

import argparse

# ============================================================
# 一、最简单的命令行参数
# ============================================================
# 常规脚本用 if __name__ == "__main__" 保护
# 这样既能被 import，又能当命令行工具跑

def main():
    parser = argparse.ArgumentParser(description="标准曲线计算工具")
    parser.add_argument("input", help="输入数据文件名")          # 位置参数（必填）
    parser.add_argument("--output", default="result.xlsx",       # 可选参数
                        help="输出文件名（默认result.xlsx）")
    parser.add_argument("--verbose", action="store_true",        # 开关参数
                        help="显示详细信息")

    args = parser.parse_args()

    if args.verbose:
        print(f"输入: {args.input}")
        print(f"输出: {args.output}")

    # 这里是你的处理逻辑
    print(f"正在处理 {args.input} ...")
    print(f"结果保存到 {args.output}")
    return args

if __name__ == "__main__":
    main()

# 使用方法（终端里）：
#   python 1-argparse命令行参数.py 数据.xlsx
#   python 1-argparse命令行参数.py 数据.xlsx --output 结果.xlsx
#   python 1-argparse命令行参数.py 数据.xlsx --verbose
#   python 1-argparse命令行参数.py --help    （自动显示帮助）

# ============================================================
# 二、参数类型（自动转 int/float）
# ============================================================
def main2():
    parser = argparse.ArgumentParser(description="剂量计算")
    parser.add_argument("--weight", type=float, required=True,
                        help="体重(kg)")
    parser.add_argument("--dose", type=float, default=10.0,
                        help="每公斤剂量(mg/kg)，默认10")
    parser.add_argument("--times", type=int, default=1,
                        help="每日次数，默认1")

    args = parser.parse_args()
    daily = args.weight * args.dose * args.times
    print(f"每日剂量: {daily} mg")
    return daily

# if __name__ == "__main__":
#     main2()
# 用法：
#   python 脚本.py --weight 60 --dose 10 --times 3

# ============================================================
# 三、多参数与子命令（进阶）
# ============================================================
# 子命令：一个工具多个操作（像 git add / git commit）
def make_parser():
    parser = argparse.ArgumentParser(description="实验数据处理工具")
    sub = parser.add_subparsers(dest="command", required=True)

    # 子命令：拟合
    p_fit = sub.add_parser("fit", help="标准曲线拟合")
    p_fit.add_argument("--data", required=True, help="数据文件")

    # 子命令：统计
    p_stat = sub.add_parser("stats", help="统计汇总")
    p_stat.add_argument("--data", required=True, help="数据文件")
    p_stat.add_argument("--group", default="组别", help="分组列名")

    return parser

# if __name__ == "__main__":
#     args = make_parser().parse_args()
#     if args.command == "fit":
#         print(f"执行拟合: {args.data}")
#     elif args.command == "stats":
#         print(f"执行统计: {args.data}，按{args.group}分组")
# 用法：
#   python 脚本.py fit --data a.xlsx
#   python 脚本.py stats --data a.xlsx --group 批次

# ============================================================
# 四、完整实战：可用的命令行工具模板
# ============================================================
# 下面这个模板可以直接复制改成自己的工具
import sys

def build_parser():
    parser = argparse.ArgumentParser(
        description="我的实验数据工具",
        epilog="示例: python 工具.py process -i 数据.xlsx -o 结果.xlsx",
    )
    parser.add_argument("action", choices=["process", "report"],
                        help="操作: process=处理, report=生成报告")
    parser.add_argument("-i", "--input", required=True, help="输入文件")
    parser.add_argument("-o", "--output", default="out.xlsx", help="输出文件")
    parser.add_argument("-v", "--verbose", action="store_true", help="详细模式")
    return parser

def process_data(input_file, output_file):
    """处理逻辑占位"""
    print(f"处理 {input_file} → {output_file}")

def make_report(input_file, output_file):
    """报告逻辑占位"""
    print(f"生成报告 {input_file} → {output_file}")

def main3():
    args = build_parser().parse_args()
    try:
        if args.action == "process":
            process_data(args.input, args.output)
        else:
            make_report(args.input, args.output)
    except FileNotFoundError:
        print(f"错误：找不到文件 {args.input}", file=sys.stderr)
        sys.exit(1)

# if __name__ == "__main__":
#     main3()

# ============================================================
# 五、总结
# ============================================================
# 位置参数：parser.add_argument("名字")（必填）
# 可选参数：--参数名，default默认值
# 类型转换：type=int / type=float / type=str
# 开关：action="store_true"
# 帮助：--help 自动生成
# 子命令：add_subparsers
# 配合 if __name__=="__main__"：既可导入又可命令行跑

# ============================================================
# 五、易错点汇总
# ============================================================
# 1. argparse 三步：建 ArgumentParser → add_argument → parse_args
# 2. 参数默认是字符串，要转类型用 type=float/int
# 3. 可选参数用 --xxx；必选位置参数直接写名字
# 4. 参数没传时用 default 给默认值
# 5. 程序入口用 if __name__ == "__main__" 包起来，
#    这样既能命令行跑也能被 import
# 6. 命令行运行：python 文件.py --参数 值

# ============================================================
# 六、自测（40%基础 + 40%中等 + 20%挑战）
# ============================================================
# 【基础】
# 1. argparse 的三个步骤是什么？
# 2. 参数默认是什么类型？怎么转？
# 3. 可选参数和位置参数的区别？
#
# 【中等】
# 4. 写一个命令行脚本：接受 --file 和 --dose 参数。
# 5. 给参数加 type=float 和 default。
# 6. 用 if __name__ 包主逻辑。
#
# 【挑战】
# 7. 把标准曲线计算脚本改造成命令行工具（--数据文件 --输出）。
# 8. 解释为什么既能 import 又能命令行跑很重要。
