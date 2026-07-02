#!/usr/bin/env python3
"""
chain-stockmap 选股数据获取统一入口
借鉴 harrischen/invest run.py 模式

用法:
  python3 fetch_stock.py <market> <code> <data_type>

market: a(A股) / hk(港股) / us(美股)
data_type: quote / finance / technical / fund_flow / valuation / all

示例:
  python3 fetch_stock.py a 600519 quote
  python3 fetch_stock.py hk 00700 all
  python3 fetch_stock.py us NVDA finance
"""
import subprocess
import sys
import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(SCRIPT_DIR, ".venv")
REQUIREMENTS = os.path.join(SCRIPT_DIR, "requirements.txt")


def get_venv_python():
    """获取虚拟环境中的 python 路径"""
    if sys.platform == "win32":
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    return os.path.join(VENV_DIR, "bin", "python3")


def setup_venv():
    """创建虚拟环境并安装依赖(借鉴 invest run.py)"""
    venv_python = get_venv_python()
    if not os.path.exists(venv_python):
        print("首次运行,创建虚拟环境...", file=sys.stderr)
        subprocess.check_call(
            [sys.executable, "-m", "venv", VENV_DIR],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        subprocess.check_call(
            [venv_python, "-m", "pip", "install", "-r", REQUIREMENTS, "-q"],
            stderr=subprocess.DEVNULL,
        )
        print("依赖安装完成。", file=sys.stderr)
    return venv_python


def main():
    if len(sys.argv) < 4:
        print(
            f"""用法: python3 {sys.argv[0]} <market> <code> <data_type>

market: a(A股) / hk(港股) / us(美股)
data_type: quote / finance / technical / fund_flow / valuation / all

示例:
  python3 {sys.argv[0]} a 600519 quote
  python3 {sys.argv[0]} hk 00700 all
  python3 {sys.argv[0]} us NVDA finance

数据源策略(借鉴 invest):
  L1 精确:腾讯/新浪 API(本 skill 已实现)
  L2 近似:WebSearch 补充
  L3 缺失:降级到 N/A + 标注
""",
            file=sys.stderr,
        )
        sys.exit(1)

    market = sys.argv[1].lower()
    code = sys.argv[2]
    data_type = sys.argv[3]

    script_map = {
        "a": "fetch_a_stock.py",
        "hk": "fetch_hk_stock.py",
        "us": "fetch_us_stock.py",
    }

    if market not in script_map:
        print(
            json.dumps({"status": "error", "message": f"不支持的市场: {market},支持: a/hk/us"}, ensure_ascii=False),
            file=sys.stderr,
        )
        sys.exit(1)

    target_script = os.path.join(SCRIPT_DIR, script_map[market])
    if not os.path.exists(target_script):
        print(
            json.dumps({"status": "error", "message": f"市场脚本不存在: {target_script}"}, ensure_ascii=False),
            file=sys.stderr,
        )
        sys.exit(1)

    # 调用市场脚本(用当前 python,因为网络访问已测试过)
    try:
        # 先尝试当前 python(系统已安装依赖)
        result = subprocess.run(
            [sys.executable, target_script, code, data_type],
            capture_output=True, text=True, timeout=30,
        )
        print(result.stdout)
        if result.returncode != 0:
            print(f"[stderr]: {result.stderr}", file=sys.stderr)
    except subprocess.TimeoutExpired:
        print(json.dumps({"status": "error", "message": "API 超时(>30s)"}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"status": "error", "message": f"脚本执行失败: {e}"}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
