# -*- coding: utf-8 -*-
"""从 DeepSeek 导出的 conversations.json 中提取指定标题的对话，保存为 Markdown。

用法：
    python 提取对话.py <json路径> <对话标题> <输出md路径>
"""
import json
import sys
from datetime import datetime


def load_conversations(json_path):
    with open(json_path, encoding="utf-8") as f:
        return json.load(f)


def find_conversation(data, title):
    for conv in data:
        if isinstance(conv, dict) and conv.get("title") == title:
            return conv
    return None


def latest_time(mapping, node_id):
    """返回以 node_id 为根的子树上最新的消息时间戳。"""
    node = mapping[node_id]
    msg = node.get("message") or {}
    best = msg.get("inserted_at") or ""
    for child in node.get("children") or []:
        t = latest_time(mapping, child)
        if t > best:
            best = t
    return best


def pick_child(mapping, node_id):
    """选择要继续的分支：多个 children 时跟随子树时间戳最新的那一个。"""
    children = mapping[node_id].get("children") or []
    if not children:
        return None
    if len(children) == 1:
        return children[0]
    return max(children, key=lambda c: latest_time(mapping, c))


def fragments_of(msg):
    """把消息的 fragments 按类型整理成文本。"""
    think = []
    response = []
    request = []
    for frag in msg.get("fragments") or []:
        t = frag.get("type")
        content = frag.get("content") or ""
        if t == "THINK":
            think.append(content)
        elif t == "RESPONSE":
            response.append(content)
        elif t == "REQUEST":
            request.append(content)
        # SEARCH 片段在导出中 results 为空，直接忽略
    return request, think, response


def extract_to_markdown(conv):
    mapping = conv["mapping"]
    lines = []
    lines.append(f"# {conv['title']}")
    lines.append("")
    lines.append(f"> 对话 ID：`{conv['id']}`")
    lines.append(f"> 创建时间：{conv['inserted_at']}")
    lines.append(f"> 最后更新：{conv['updated_at']}")
    lines.append("")
    lines.append("---")
    lines.append("")

    order = []
    node_id = "root"
    while True:
        nxt = pick_child(mapping, node_id)
        if nxt is None:
            break
        node_id = nxt
        order.append(node_id)

    user_count = 0
    ai_count = 0
    for node_id in order:
        msg = mapping[node_id].get("message")
        if not msg:
            continue
        request, think, response = fragments_of(msg)
        ts = (msg.get("inserted_at") or "")[:16].replace("T", " ")
        if request and not response:
            # 用户消息
            user_count += 1
            lines.append(f"## 🧑 我（第 {user_count} 条）")
            if ts:
                lines.append(f"*{ts}*")
            lines.append("")
            lines.append("\n\n".join(request).strip())
            lines.append("")
            lines.append("---")
            lines.append("")
        elif response:
            ai_count += 1
            if think:
                lines.append(f"## 🤖 DeepSeek 思考（第 {ai_count} 条）")
                if ts:
                    lines.append(f"*{ts}*")
                lines.append("")
                lines.append("<details><summary>展开思考过程</summary>")
                lines.append("")
                lines.append("\n\n".join(think).strip())
                lines.append("")
                lines.append("</details>")
                lines.append("")
            lines.append(f"## ✍️ DeepSeek 回复（第 {ai_count} 条）")
            lines.append("")
            lines.append("\n\n".join(response).strip())
            lines.append("")
            lines.append("---")
            lines.append("")

    lines.append("")
    lines.append(f"*共 {user_count} 条用户消息、{ai_count} 条 AI 回复。*")
    return "\n".join(lines)


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    json_path, title, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    data = load_conversations(json_path)
    conv = find_conversation(data, title)
    if conv is None:
        print(f"未找到标题为「{title}」的对话。现有对话标题：")
        for c in data:
            if isinstance(c, dict):
                print("  -", c.get("title"))
        sys.exit(1)
    md = extract_to_markdown(conv)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"已提取 {len(conv['mapping'])} 个节点 → {out_path}")


if __name__ == "__main__":
    main()
