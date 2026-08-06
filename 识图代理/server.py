# -*- coding: utf-8 -*-
"""
识图代理 MCP Server
====================
给 Copilot Chat 装上"眼睛"：调用免费多模态模型（智谱 GLM-4V-Flash）识图，
把图片内容转成文字描述返回给 Copilot，让纯文本模型也能"看懂"图片。

用法：
  1. 去 https://open.bigmodel.cn 免费注册，创建一个 API Key（GLM-4V-Flash 免费）
  2. 把 key 填进同目录的 config.json
  3. 由 VS Code 的 .vscode/mcp.json 自动启动本服务，无需手动运行

改配置后重启 VS Code（或重载窗口）即可生效。
"""
import os
import json
import base64
import httpx
from mcp.server.mcpserver import MCPServer

# ---------- 配置 ----------
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")


def load_config():
    cfg = {
        "api_key": "",
        "model": "glm-4v-flash",
        "base_url": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
    }
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg.update(json.load(f))
        except Exception as e:
            print(f"[vision-proxy] 读取 config.json 失败: {e}")
    return cfg


mcp = MCPServer("vision-proxy")


# ---------- 工具 ----------
@mcp.tool()
def describe_image(image_path: str, question: str = "请详细描述这张图片的内容。") -> str:
    """识别一张图片并把内容转成文字描述，作为图片的文本表示返回。

    Args:
        image_path: 图片文件的绝对路径（支持 jpg/jpeg/png/webp/gif/bmp）。
        question: 可选，针对图片想问的问题，默认请模型详细描述。
    """
    # 每次调用时实时读取配置（改 key/模型无需重启）
    cfg = load_config()
    if not cfg.get("api_key"):
        return ("错误：识图代理未配置 API Key。"
                "请先在 识图代理/config.json 里填入智谱 API Key"
                "（https://open.bigmodel.cn 免费注册，GLM-4V-Flash 免费使用）。")

    # 1. 检查文件
    if not os.path.isfile(image_path):
        return f"错误：找不到图片文件 {image_path}"
    size = os.path.getsize(image_path)
    if size > 10 * 1024 * 1024:
        return f"错误：图片太大（{size // 1024 // 1024}MB），超过 10MB 限制，请压缩后再试。"

    # 2. 转 base64
    mime = _mime_of(image_path)
    try:
        with open(image_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
    except Exception as e:
        return f"错误：读取图片失败 {e}"

    # 3. 调用多模态模型
    try:
        payload = {
            "model": cfg["model"],
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "image_url",
                     "image_url": {"url": f"data:{mime};base64,{b64}"}},
                    {"type": "text", "text": question},
                ],
            }],
        }
        headers = {"Authorization": f"Bearer {cfg['api_key']}"}
        resp = httpx.post(cfg["base_url"], json=payload,
                          headers=headers, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"错误：调用识图模型失败：{e}"


@mcp.tool()
def list_images(folder: str) -> str:
    """列出某个文件夹里的图片文件，方便找到要识别的图片路径。

    Args:
        folder: 文件夹绝对路径。
    """
    exts = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}
    if not os.path.isdir(folder):
        return f"错误：找不到文件夹 {folder}"
    found = [os.path.join(folder, n) for n in os.listdir(folder)
             if os.path.splitext(n)[1].lower() in exts]
    if not found:
        return f"文件夹 {folder} 里没有找到图片。"
    return "找到图片：\n" + "\n".join(found)


def _mime_of(path):
    ext = os.path.splitext(path)[1].lower()
    return {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".png": "image/png", ".gif": "image/gif",
        ".webp": "image/webp", ".bmp": "image/bmp",
    }.get(ext, "image/jpeg")


if __name__ == "__main__":
    mcp.run()
