#!/usr/bin/env python3
"""
发送「格式选择卡」到当前 chat(本 skill 独创 · 末段交付)

CardKit 2.0 schema,两个按钮:
- HTML:单文件 + 内嵌 CSS,适合微信/飞书/邮件转发
- DOCX:pandoc 生成,适合正式投递

按钮回调走 bridge_token,让用户点选后,Claude 在同一会话里继续生成。

用法:
  python3 send_format_card.py <chat_id> <report_md_path> <report_name>

输出:
  - stdout:完整 lark-cli im send-card 命令(可直接复制执行)
"""
import sys
import json
import re
import os
import hmac
import hashlib
import base64
import time
from pathlib import Path


def gen_bridge_token(report_path):
    """
    生成 bridge 回调签名 token(借鉴 lark-channel bridge 设计)

    实际生产中,lark-cli 会有专门的签名接口。
    这里用占位算法,但格式严格对齐 — 调用方需替换为 lark-cli 的真实 token 生成。
    """
    secret = os.environ.get("LARK_CHANNEL_BRIDGE_SECRET", "industry-chain-research-skill-2026")
    timestamp = str(int(time.time()))
    payload = f"{report_path}:{timestamp}"
    sig = hmac.new(
        secret.encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()[:32]
    token = f"{timestamp}.{sig}"
    return token


def build_format_card(chat_id, report_path, report_name):
    """构造 CardKit 2.0 格式选择卡"""
    bridge_token = gen_bridge_token(report_path)

    card = {
        "schema": "2.0",
        "header": {
            "title": {
                "tag": "plain_text",
                "content": f"📄 报告生成 · {report_name}"
            },
            "template": "blue"
        },
        "body": {
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**报告文件**:`{report_path}`\n**报告大小**:{os.path.getsize(report_path) / 1024:.1f} KB\n\n请选择输出格式:"
                    }
                },
                {"tag": "hr"},
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": "📄 生成 HTML(推荐 · 易读可转发)"
                            },
                            "type": "primary",
                            "value": {
                                "__bridge_cb": True,
                                "bridge_token": bridge_token,
                                "format": "html",
                                "report_path": report_path,
                                "report_name": report_name,
                                "chat_id": chat_id,
                                "action": "render_report"
                            }
                        },
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": "📝 生成 Word(DOCX · 适合正式投递)"
                            },
                            "type": "default",
                            "value": {
                                "__bridge_cb": True,
                                "bridge_token": bridge_token,
                                "format": "docx",
                                "report_path": report_path,
                                "report_name": report_name,
                                "chat_id": chat_id,
                                "action": "render_report"
                            }
                        }
                    ]
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "💡 **HTML**:单文件 + 内嵌 CSS,微信/飞书/邮件直接转发\n💡 **DOCX**:pandoc 生成,适合打印或正式邮件附件"
                    }
                }
            ]
        }
    }

    return card


def main():
    if len(sys.argv) < 4:
        print("用法:")
        print("  python3 send_format_card.py <chat_id> <report_md_path> <report_name>")
        print("  例:python3 send_format_card.py oc_xxx report.md '创新药产业链报告'")
        sys.exit(1)

    chat_id = sys.argv[1]
    report_path = sys.argv[2]
    report_name = sys.argv[3]

    if not os.path.exists(report_path):
        print(f"ERROR: 报告文件不存在: {report_path}", file=sys.stderr)
        sys.exit(1)

    card = build_format_card(chat_id, report_path, report_name)

    # 打印 lark-cli 命令(让 Claude 直接复制执行)
    card_json = json.dumps(card, ensure_ascii=False)

    print("=" * 60)
    print("CardKit 2.0 格式选择卡 JSON:")
    print("=" * 60)
    print(json.dumps(card, ensure_ascii=False, indent=2))
    print()
    print("=" * 60)
    print("执行命令(Claude 在工具调用里执行):")
    print("=" * 60)
    # 用 stdin 方式传 JSON,避免转义地狱
    print(f"cat << 'CARDJSON' | lark-cli im send-card --chat-id {chat_id} --card -")
    print(card_json)
    print("CARDJSON")


if __name__ == "__main__":
    main()
