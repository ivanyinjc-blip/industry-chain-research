#!/usr/bin/env python3
"""
report.md → HTML / DOCX 渲染器(本 skill 独创 · 末段交付)

设计:借鉴 weekly-review-style,提供极简学术主题 CSS
- HTML:单文件 + 内嵌 CSS + 表格美化,适合微信/飞书/邮件转发
- DOCX:pandoc 生成,适合正式投递

用法:
  python3 render_report.py <input.md> <output.html|docx> [format]
  python3 render_report.py report.md report.html html
  python3 render_report.py report.md report.docx docx
"""
import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime


# === 内嵌 CSS 主题(借鉴 weekly-review-style 极简学术风) ===
HTML_CSS = """
:root {
  --primary: #1f4e79;
  --secondary: #2e75b6;
  --bg: #fafbfc;
  --text: #1a1a1a;
  --border: #e1e4e8;
  --code-bg: #f6f8fa;
  --warn-bg: #fff8c5;
  --ok-bg: #dafbe1;
  --err-bg: #ffebe9;
}
* { box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
  line-height: 1.7;
  color: var(--text);
  background: var(--bg);
  max-width: 960px;
  margin: 0 auto;
  padding: 40px 32px 80px;
}
h1, h2, h3, h4 { color: var(--primary); margin-top: 1.8em; }
h1 { font-size: 2em; border-bottom: 3px solid var(--primary); padding-bottom: 12px; }
h2 { font-size: 1.5em; border-bottom: 1px solid var(--border); padding-bottom: 6px; }
h3 { font-size: 1.2em; color: var(--secondary); }
blockquote {
  border-left: 4px solid var(--secondary);
  background: #f0f7ff;
  padding: 12px 16px;
  margin: 16px 0;
  border-radius: 0 4px 4px 0;
  color: #555;
}
table {
  border-collapse: collapse;
  width: 100%;
  margin: 16px 0;
  font-size: 0.92em;
}
th, td {
  border: 1px solid var(--border);
  padding: 8px 12px;
  text-align: left;
}
th { background: var(--primary); color: #fff; font-weight: 600; }
tbody tr:nth-child(even) { background: #f6f8fa; }
tbody tr:hover { background: #eef5fc; }
code {
  background: var(--code-bg);
  padding: 2px 6px;
  border-radius: 3px;
  font-family: "SF Mono", Consolas, monospace;
  font-size: 0.9em;
  color: #d73a49;
}
pre {
  background: var(--code-bg);
  padding: 16px;
  border-radius: 6px;
  overflow-x: auto;
  border: 1px solid var(--border);
}
pre code { background: transparent; padding: 0; color: var(--text); }
ul, ol { padding-left: 24px; }
li { margin: 4px 0; }
hr { border: 0; border-top: 1px solid var(--border); margin: 32px 0; }
img { max-width: 100%; border-radius: 4px; }

/* 数据状态徽章(借鉴 gushifenxi 三层诚实度) */
.badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.8em;
  font-weight: 600;
  margin-left: 4px;
}
.badge-ok { background: var(--ok-bg); color: #1a7f37; }
.badge-estimated { background: var(--warn-bg); color: #9a6700; }
.badge-pending { background: var(--err-bg); color: #cf222e; }

/* 评分星级 */
.rating { color: #f59e0b; font-size: 1.1em; }

/* 报告元信息 */
.meta {
  background: linear-gradient(135deg, #f0f7ff 0%, #e6f2fb 100%);
  border-left: 4px solid var(--primary);
  padding: 16px 20px;
  border-radius: 0 6px 6px 0;
  margin-bottom: 32px;
  font-size: 0.92em;
}
.meta strong { color: var(--primary); }

/* 反证条件框 */
.disproof {
  background: var(--err-bg);
  border-left: 4px solid #cf222e;
  padding: 12px 16px;
  margin: 12px 0;
  border-radius: 0 4px 4px 0;
}
.disproof strong { color: #cf222e; }

/* 跟踪清单框 */
.tracking {
  background: var(--warn-bg);
  border-left: 4px solid #9a6700;
  padding: 12px 16px;
  margin: 12px 0;
  border-radius: 0 4px 4px 0;
}
.tracking strong { color: #9a6700; }

/* 页脚 */
footer {
  margin-top: 64px;
  padding-top: 24px;
  border-top: 2px solid var(--border);
  color: #888;
  font-size: 0.85em;
  text-align: center;
}
"""


def md_to_html(md_path, html_path):
    """markdown → HTML(内嵌 CSS)"""
    import re
    try:
        import markdown
    except ImportError:
        # 降级:用 pandoc
        subprocess.run(
            ["pandoc", md_path, "-o", html_path, "--standalone",
             "--metadata", f"title=研究报告"],
            check=True
        )
        return

    md_text = Path(md_path).read_text(encoding="utf-8")

    # 数据状态徽章替换(借鉴 gushifenxi)
    md_text = re.sub(
        r"\*\*已核验\*\*",
        '<span class="badge badge-ok">✓ 已核验</span>',
        md_text
    )
    md_text = re.sub(
        r"\*\*估算\*\*",
        '<span class="badge badge-estimated">~ 估算</span>',
        md_text
    )
    md_text = re.sub(
        r"\*\*待查证\*\*",
        '<span class="badge badge-pending">? 待查证</span>',
        md_text
    )

    # 评分星级(★★★ → ★★★)
    md_text = re.sub(
        r"(★{2,5})",
        r'<span class="rating">\1</span>',
        md_text
    )

    html_body = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "toc", "nl2br"]
    )

    # 提取第一个 h1 作为 title
    title_match = re.search(r"<h1[^>]*>(.*?)</h1>", html_body)
    title = title_match.group(1) if title_match else "研究报告"

    html_full = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>{HTML_CSS}</style>
</head>
<body>
{html_body}
<footer>
<p>由 <strong>industry-chain-research</strong> skill 自动生成 · {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
<p>格式:HTML(单文件,可直接微信/飞书/邮件转发)</p>
</footer>
</body>
</html>
"""
    Path(html_path).write_text(html_full, encoding="utf-8")


def md_to_docx(md_path, docx_path):
    """markdown → DOCX(用 pandoc)"""
    md_path = Path(md_path).resolve()
    docx_path = Path(docx_path).resolve()

    # 检查 pandoc
    try:
        subprocess.run(["pandoc", "--version"], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("ERROR: pandoc 未安装,请运行: brew install pandoc", file=sys.stderr)
        sys.exit(1)

    subprocess.run([
        "pandoc",
        str(md_path),
        "-o", str(docx_path),
        "--from", "markdown",
        "--to", "docx",
        "--reference-doc=reference.docx",  # 可选,自定义样式
    ], check=True)


def main():
    if len(sys.argv) < 3:
        print("用法:")
        print("  python3 render_report.py <input.md> <output.html> html")
        print("  python3 render_report.py <input.md> <output.docx> docx")
        sys.exit(1)

    md_path = sys.argv[1]
    out_path = sys.argv[2]
    fmt = sys.argv[3] if len(sys.argv) > 3 else out_path.rsplit(".", 1)[-1]

    if not os.path.exists(md_path):
        print(f"ERROR: 输入文件不存在: {md_path}", file=sys.stderr)
        sys.exit(1)

    print(f"[*] 渲染 {md_path} → {out_path} ({fmt})")

    if fmt == "html":
        md_to_html(md_path, out_path)
    elif fmt == "docx":
        md_to_docx(md_path, out_path)
    else:
        print(f"ERROR: 未知格式 {fmt} (支持 html / docx)", file=sys.stderr)
        sys.exit(1)

    size_kb = os.path.getsize(out_path) / 1024
    print(f"[✓] 完成:{out_path} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
