# industry-chain-research v4.1.1 Makefile
# 用法:make <target>

.PHONY: help install test lint run-radar run-stockmap run-report clean

PYTHON ?= python3
PIP ?= pip3

help:  ## 显示帮助
	@echo "可用 target:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## 安装依赖
	$(PIP) install -r requirements.txt
	$(PIP) install -e ".[dev]"

test:  ## 跑测试
	$(PYTHON) -m pytest tests/ -v --cov=chain-stockmap --cov=chain-radar --cov-report=term-missing

lint:  ## 静态检查
	$(PYTHON) -m ruff check .

run-radar:  ## 跑行业雷达
	$(PYTHON) chain-radar/scripts/calc_radar_score.py

run-stockmap:  ## 跑股票地图
	$(PYTHON) chain-stockmap/scripts/calc_settlement_score.py

run-report:  ## 跑报告渲染
	$(PYTHON) chain-report/scripts/render_report.py

clean:  ## 清理临时文件
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null
	rm -f .coverage htmlcov -r
