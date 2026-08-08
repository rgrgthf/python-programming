# ============================================================
# 调试与日志 ② — logging 日志系统
# ============================================================
# 正式程序不推荐 print 打日志（难管理、难分级、难保存）。
# logging 是专业方案：分级、时间戳、写文件、按级别过滤。

import logging

# ============================================================
# 一、基本用法（先学会这一套）
# ============================================================
logging.basicConfig(
    level=logging.INFO,          # 输出级别：INFO及以上
    format="%(asctime)s [%(levelname)s] %(message)s",   # 格式
    datefmt="%Y-%m-%d %H:%M:%S",
)

logging.debug("调试信息")        # 最详细，一般不显示
logging.info("程序开始运行")
logging.warning("数据缺失，使用默认值")
logging.error("计算失败：除数为零")
# logging.critical("系统崩溃")

# 级别从低到高：
#   DEBUG < INFO < WARNING < ERROR < CRITICAL
# basicConfig 的 level 决定显示哪个级别及以上的

# ============================================================
# 二、把日志写到文件
# ============================================================
# 同时输出到控制台 + 文件
import logging

logger = logging.getLogger("myapp")          # 创建专属 logger
logger.setLevel(logging.DEBUG)

# 控制台 handler
console = logging.StreamHandler()
console.setLevel(logging.INFO)

# 文件 handler
file_handler = logging.FileHandler("app.log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# 统一格式
fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
console.setFormatter(fmt)
file_handler.setFormatter(fmt)

logger.addHandler(console)
logger.addHandler(file_handler)

logger.info("实验数据处理开始")
logger.warning("第3个样品数据异常，已跳过")
logger.error("无法读取文件 data.csv")

# 运行后查看 app.log 文件，会看到完整日志记录

# ============================================================
# 三、实战：实验数据处理脚本的日志设计
# ============================================================
# 场景：批量处理实验数据，每个步骤都要记录，出错要可追溯
def process_experiment(data_path, logger):
    logger.info(f"开始处理 {data_path}")
    try:
        # 模拟读取
        raw = [0.5, 1.2, None, 0.8]
        # 模拟清洗
        cleaned = []
        for i, v in enumerate(raw):
            if v is None:
                logger.warning(f"第{i+1}个数据为空，已跳过")
                continue
            cleaned.append(v)
        logger.info(f"读取 {len(raw)} 条，有效 {len(cleaned)} 条")

        # 模拟计算
        mean = sum(cleaned) / len(cleaned)
        logger.info(f"平均值: {mean:.3f}")
        return mean

    except FileNotFoundError:
        logger.error(f"文件不存在: {data_path}")
        raise
    except Exception as e:
        logger.exception("处理过程发生未知错误")   # 带完整堆栈
        raise

# process_experiment("data/test.csv", logger)

# ============================================================
# 四、logging 的好处（对比 print）
# ============================================================
# 1. 分级：DEBUG 详细调试 / INFO 流程 / WARNING 警告 / ERROR 错误
# 2. 时间戳：每条自动带时间，事后可追溯
# 3. 落盘：日志写文件，程序崩了也能看
# 4. 可配置：生产环境只显示 ERROR，开发显示 DEBUG
# 5. 不污染输出：正式结果用 print，过程用 logging

# ============================================================
# 五、常见误区
# ============================================================
# 误区1：basicConfig 和 getLogger 混用
#   → 要么用 basicConfig 快速配置，要么用 getLogger + handler
# 误区2：日志里拼字符串（性能）
#   → logger.info("值: %s", value)  用 % 格式，懒计算
# 误区3：忘记 encoding
#   → FileHandler(..., encoding="utf-8") 避免中文乱码

# ============================================================
# 六、总结
# ============================================================
# 快速用：logging.basicConfig(level=..., format=...)
# 正式用：getLogger + StreamHandler + FileHandler
# 级别：DEBUG/INFO/WARNING/ERROR/CRITICAL
# 好习惯：程序关键步骤都打 INFO，异常打 ERROR

# ============================================================
# 七、易错点汇总
# ============================================================
# 1. basicConfig 和 getLogger+handler 不要混用（重复输出）
# 2. FileHandler 记得 encoding="utf-8"，否则中文乱码
# 3. 日志字符串用 % 占位符（懒计算）：
#    logger.info("值: %s", v) 比 logger.info(f"值: {v}") 快
#    （f-string 即使不输出也会先拼好字符串）
# 4. 级别搞清顺序：DEBUG < INFO < WARNING < ERROR < CRITICAL
# 5. logger.exception() 要放在 except 里，自带完整堆栈
# 6. 一个 logger 不要重复 addHandler（会打多遍）

# ============================================================
# 八、自测（40%基础 + 40%中等 + 20%挑战）
# ============================================================
# 【基础】
# 1. logging 的五个级别从低到高是什么？
# 2. basicConfig 里 level 是干嘛的？
# 3. logging 相比 print 的三个好处？
#
# 【中等】
# 4. 配置 logging 同时输出到控制台和文件。
# 5. 在实验处理函数里：读取成功打 INFO、
#    空值打 WARNING、文件不存在打 ERROR。
# 6. logger.exception 和 logger.error 的区别？
#
# 【挑战】
# 7. 写一个函数用 try/except + logger.exception 记录完整错误。
# 8. 解释为什么日志用 %s 占位符比 f-string 好（性能角度）。
