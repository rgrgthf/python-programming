# ============================================================
# 并发编程 ① — 多线程 threading
# ============================================================
# 场景：程序里有大量"等待"（等网络、等文件、等IO），
# 多线程 = 等待的同时干别的事，大幅提速。
# 典型应用：批量下载、批量请求 API、批量读文件。

import threading
import time

# ============================================================
# 一、创建线程的两种方式
# ============================================================
# 方式1：直接传函数
def work(name, seconds):
    print(f"线程{name}开始，需要{seconds}秒")
    time.sleep(seconds)
    print(f"线程{name}完成")

# 创建线程
t1 = threading.Thread(target=work, args=("A", 2))
t2 = threading.Thread(target=work, args=("B", 2))

start = time.time()
t1.start()      # 启动
t2.start()      # 两个线程同时跑
t1.join()       # 等线程结束
t2.join()
print(f"多线程总耗时: {time.time()-start:.1f}秒")   # → 约2秒（并行）

# 对比：串行要4秒
start = time.time()
work("串1", 2)
work("串2", 2)
print(f"串行总耗时: {time.time()-start:.1f}秒")     # → 约4秒

# ============================================================
# 二、线程池（推荐！不用手动管理线程）
# ============================================================
from concurrent.futures import ThreadPoolExecutor

def fetch_one(id_):
    """模拟网络请求"""
    time.sleep(1)
    return f"数据{id_}"

# 线程池：自动分配线程
with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(fetch_one, range(8)))
print(results)   # → 8个任务，4线程并行，约2秒完成

# ============================================================
# 三、线程安全：共享数据要加锁
# ============================================================
# ⚠️ 坑：多个线程同时改一个变量会出问题
counter = 0

def bad_increment():
    global counter
    for _ in range(100000):
        counter += 1        # 不是原子操作！可能丢更新

threads = [threading.Thread(target=bad_increment) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()
print(f"不加锁: {counter}")    # → 可能不是 400000（丢数据！）

# 加锁解决
lock = threading.Lock()
counter = 0

def good_increment():
    global counter
    for _ in range(100000):
        with lock:           # 拿锁，保证原子性
            counter += 1

threads = [threading.Thread(target=good_increment) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()
print(f"加锁后: {counter}")    # → 400000（正确）

# ============================================================
# 四、实战：批量下载/请求（科学数据）
# ============================================================
# 场景：批量请求 API（如 PubChem 查多个化合物）
def query_drug(cid):
    """模拟查询一个化合物的API"""
    time.sleep(0.5)      # 模拟网络延迟
    return f"CID {cid} 查询完成"

cids = list(range(1, 11))    # 10个化合物

# 串行：5秒
start = time.time()
results = [query_drug(c) for c in cids]
print(f"串行: {time.time()-start:.1f}秒")

# 线程池：约1.5秒（4线程）
start = time.time()
with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(query_drug, cids))
print(f"线程池: {time.time()-start:.1f}秒")
print(results[0])

# ============================================================
# 五、什么时候用多线程？
# ============================================================
# ✅ 适合（IO密集型）：网络请求、文件读写、数据库
#    等待时释放 CPU，别的线程干活 → 快很多
#
# ❌ 不适合（CPU密集型）：大量纯计算
#    受 GIL 限制，多线程并不能同时用多核
#    CPU 密集要用多进程（下一节）
#
# GIL（全局解释器锁）：Python 同一时刻只有一个线程执行字节码
#   所以纯计算多线程反而慢（线程切换开销）
#   但 IO 等待时 GIL 会释放，所以 IO 密集多线程有效

# ============================================================
# 六、总结
# ============================================================
# 创建线程：threading.Thread(target=函数, args=())
# 线程池：ThreadPoolExecutor（推荐）
# 共享数据：加锁 threading.Lock（with lock）
# 适用：IO密集（网络/文件/数据库）
# 不适用：CPU密集（用多进程）
