"""
v4.1.1 测试公共 fixture
"""
import sys
import json
from pathlib import Path
import pytest

# 把所有 scripts 目录加到 sys.path
ROOT = Path(__file__).parent.parent
for p in [
    ROOT / "chain-stockmap" / "scripts",
    ROOT / "chain-radar" / "scripts",
    ROOT / "chain-report" / "scripts",
]:
    sys.path.insert(0, str(p))


@pytest.fixture
def sample_a_stock_quote():
    """茅台 600519 模拟 quote 数据"""
    return {
        "f43": "14500",       # 145.00 元
        "f44": "14600",       # 146.00 高
        "f45": "14400",       # 144.00 低
        "f46": "14450",       # 开盘
        "f47": "123456",      # 成交量(手)
        "f48": "1780000000",  # 成交额(元)
        "f57": "600519",
        "f58": "贵州茅台",
        "f60": "14400",       # 昨收
        "f50": "0.85",        # 量比
        "f51": "15840",       # 涨停
        "f52": "12960",       # 跌停
        "f117": "1820000000000",  # 总市值(元)1.82 万亿
        "f168": "0.42",       # 换手率
        "f167": "8.5",        # PB 倍数 (v4.1.1 修复后)
        "f292": "1820000000000",
        "f191": "25.6",       # PE 倍数 (v4.1.1 修复后)
        "f192": "8.5",
        "f173": "32.5",       # ROE %
    }


@pytest.fixture
def sample_loss_stock_quote():
    """亏损股 模拟 quote"""
    return {
        "f43": "500",
        "f58": "测试亏损股",
        "f60": "490",
        "f117": "50000000000",
        "f168": "1.2",
        "f167": "2.1",
        "f292": "50000000000",
        "f191": "-15.5",      # 负 PE(亏损)
        "f192": "2.1",
    }


@pytest.fixture
def fixtures_dir():
    return Path(__file__).parent / "fixtures"
