# ============================================================
# 并发编程 ③ — 异步编程 asyncio
# ============================================================
# 第三种并发方式：异步（async/await）。
# 多线程是"操作系统帮我们切换"，异步是"程序自己切换"。
# 特点：单线程内实现高并发 IO，超省资源，性能怪兽。
# 适用：大量网络请求、API 调用、Web 服务器。

import asyncio
import time

# ============================================================
# 一、async / await 基础
# ============================================================
# async def 定义协程（可暂停的函数）
# await 遇到耗时操作时"让出"，等结果回来继续

async def say_hello():
    print("开始")
    await asyncio.sleep(1)     # 模拟耗时操作（如网络请求）
    print("结束")

# 运行协程
# asyncio.run(say_hello())

# ============================================================
# 二、并发执行多个协程（asyncio 的核心价值）
# ============================================================
async def fetch_data(id_, delay):
    """模拟网络请求"""
    print(f"请求{id_}开始")
    await asyncio.sleep(delay)      # 等待时让出控制权
    print(f"请求{id_}完成")
    return f"数据{id_}"

async def main():
    # gather：同时发起多个请求（并发！）
    results = await asyncio.gather(
        fetch_data("A", 1),
        fetch_data("B", 1),
        fetch_data("C", 1),
    )
    print(results)

start = time.time()
asyncio.run(main())
print(f"总耗时: {time.time()-start:.1f}秒")   # → 约1秒（3个同时跑）

# ============================================================
# 三、批量并发请求（100个任务）
# ============================================================
async def fetch_many(count):
    # 创建 100 个任务
    tasks = [fetch_data(i, 0.1) for i in range(count)]
    results = await asyncio.gather(*tasks)
    return results

async def main2():
    results = await fetch_many(100)
    print(f"完成 {len(results)} 个请求")

# asyncio.run(main2())

# ============================================================
# 四、真实场景：批量调用 API
# ============================================================
# 需要 aiohttp（pip install aiohttp）—— requests 的异步版
import aiohttp

async def fetch_url(session, url):
    async with session.get(url) as resp:
        return await resp.text()

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# urls = ["https://httpbin.org/get"] * 10
# results = asyncio.run(fetch_all(urls))
# 对比 requests 串行，异步版快数倍

# ============================================================
# 五、asyncio vs 多线程
# ============================================================
# asyncio：
#   + 单线程，内存占用极小，可支持上万连接
#   + 切换开销比线程小
#   - 代码要写 async/await，学习成本
#   - 一个阻塞操作（如 time.sleep）会卡住整个循环
#
# 多线程：
#   + 代码不用大改（普通函数）
#   + 线程池用起来简单
#   - 每个线程占内存，几千个就吃力
#
# 判断：
#   简单小批量 → 多线程（ThreadPoolExecutor）
#   海量请求/高性能服务 → asyncio
#   两者都能做时，asyncio 更高效但代码更复杂

# ============================================================
# 六、Web 框架也用异步（了解）
# ============================================================
# 第28章学的 Flask 是同步的
# FastAPI 是异步 Web 框架（性能高，自动生成API文档）
# 以后如果做高性能 API 服务，可以学 FastAPI：
#   from fastapi import FastAPI
#   app = FastAPI()
#   @app.get("/drugs")
#   async def get_drugs(): ...

# ============================================================
# 七、总结
# ============================================================
# async def：定义协程
# await：等待（并让出控制权）
# asyncio.gather：并发执行多个
# asyncio.run：入口
# aiohttp：异步网络库
# 应用：海量API请求、高性能Web服务
# 学习建议：先掌握多线程（够用），asyncio 作为进阶了解
