"""
共享配置加载 v4.1.1
- TUSHARE_DB_PATH 从环境变量读取
- 没设时给清晰错误
- 兼容 Windows / Linux / macOS 路径
"""
import os
import sys
from pathlib import Path
from typing import Optional


def get_db_path(var_name: str = "TUSHARE_DB_PATH") -> str:
    """
    读取 DuckDB 路径,失败时给清晰错误

    Returns:
        str: 数据库绝对路径

    Raises:
        FileNotFoundError: 未配置或路径不存在
    """
    db_path = os.environ.get(var_name, "").strip()
    if not db_path:
        print("=" * 60, file=sys.stderr)
        print(f"❌ 环境变量 {var_name} 未设置", file=sys.stderr)
        print("", file=sys.stderr)
        print("请先配置 Tushare DuckDB 路径:", file=sys.stderr)
        print("  Linux/macOS:", file=sys.stderr)
        print(f'    export {var_name}="/path/to/tushare.db"', file=sys.stderr)
        print("  Windows PowerShell:", file=sys.stderr)
        print(f'    $env:{var_name}="E:\\path\\to\\tushare.db"', file=sys.stderr)
        print("  Windows CMD:", file=sys.stderr)
        print(f"    set {var_name}=E:\\path\\to\\tushare.db", file=sys.stderr)
        print("", file=sys.stderr)
        print("或者运行一键安装脚本:", file=sys.stderr)
        print("  bash setup.sh    # Linux/macOS", file=sys.stderr)
        print("  .\\setup.ps1      # Windows", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        raise FileNotFoundError(f"{var_name} 未设置")

    p = Path(db_path)
    if not p.exists():
        print(f"❌ {var_name}={db_path} 不存在", file=sys.stderr)
        print(f"   请检查路径或参考 docs/setup.md", file=sys.stderr)
        raise FileNotFoundError(f"DB 不存在: {db_path}")

    return str(p)


def get_akshare_token() -> Optional[str]:
    """AKShare 不需要 token,保留此函数为后续扩展"""
    return os.environ.get("AKSHARE_TOKEN", None)


def get_tushare_token() -> Optional[str]:
    """Tushare Pro token(用于高级接口)"""
    return os.environ.get("TUSHARE_TOKEN", None)
