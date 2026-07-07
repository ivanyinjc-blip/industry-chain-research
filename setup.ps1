# industry-chain-research v4.1.1 Windows 一键安装
# 用法:.\setup.ps1
$ErrorActionPreference = "Stop"

Write-Host "=== industry-chain-research v4.1.1 安装 ===" -ForegroundColor Cyan
Write-Host "Python: $(python --version)"

# 创建 venv
if (-not (Test-Path "venv")) {
    Write-Host "[1/3] 创建 venv..." -ForegroundColor Yellow
    python -m venv venv
}

# 激活 venv
Write-Host "[2/3] 激活 venv..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# 安装依赖
Write-Host "[3/3] 安装依赖..." -ForegroundColor Yellow
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e ".[dev]"

# 配置 TUSHARE_DB_PATH(交互式)
$dbPath = Read-Host "请输入 Tushare DuckDB 路径(如 E:\tushare_db\data\tushare.db),直接回车跳过"
if ($dbPath) {
    [System.Environment]::SetEnvironmentVariable("TUSHARE_DB_PATH", $dbPath, "User")
    Write-Host "✅ TUSHARE_DB_PATH 已设置为: $dbPath" -ForegroundColor Green
}

Write-Host "`n=== 安装完成 ===" -ForegroundColor Cyan
Write-Host "下一步:"
Write-Host "  1. (可选)重启 PowerShell 让环境变量生效"
Write-Host "  2. 跑测试: pytest tests/"
Write-Host "  3. 跑雷达:  python chain-radar/scripts/calc_radar_score.py"
