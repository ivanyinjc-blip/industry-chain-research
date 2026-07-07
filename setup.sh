#!/usr/bin/env bash
# industry-chain-research v4.1.1 Linux/macOS 一键安装
set -e

echo "=== industry-chain-research v4.1.1 安装 ==="
echo "Python: $(python3 --version)"

# 创建 venv
if [ ! -d "venv" ]; then
    echo "[1/3] 创建 venv..."
    python3 -m venv venv
fi

# 激活
echo "[2/3] 激活 venv..."
source venv/bin/activate

# 安装
echo "[3/3] 安装依赖..."
pip install --upgrade pip
pip install -r requirements.txt
pip install -e ".[dev]"

# 配置 TUSHARE_DB_PATH
echo ""
read -p "请输入 Tushare DuckDB 路径(如 /mnt/e/tushare_db/data/tushare.db),直接回车跳过: " db_path
if [ -n "$db_path" ]; then
    echo "export TUSHARE_DB_PATH=$db_path" >> ~/.bashrc
    export TUSHARE_DB_PATH="$db_path"
    echo "✅ 已写入 ~/.bashrc,请 source ~/.bashrc 或重启终端"
fi

echo ""
echo "=== 安装完成 ==="
echo "下一步:"
echo "  1. pytest tests/"
echo "  2. python chain-radar/scripts/calc_radar_score.py"
