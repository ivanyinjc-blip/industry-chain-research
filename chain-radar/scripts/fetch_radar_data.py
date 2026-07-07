#!/usr/bin/env python3
"""
chain-radar 行业雷达数据采集脚本
==================================

输入:无(从 Tushare DuckDB 直接扫描所有被动指数型 ETF)
输出:radar_raw.json(每只 ETF 的多时间窗口涨幅 + 行业分类)

数据源:
- ETF 基础信息:Tushare DuckDB(fund_basic,本地)
- ETF 日线:Tushare DuckDB(fund_daily,本地)

约束:
- DuckDB 只读连接(duckdb.connect(read_only=True),引擎级别写保护)
- 不依赖 local_api.py 是否打 read_only patch,自带安全连接
- 失败回退东财 push2his(只读,无写风险)

时间窗口:
- 1M = 21 交易日
- 3M = 63 交易日
- 6M = 126 交易日
- 12M = 250 交易日
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime, timedelta

# ============================================================
# A. DuckDB 只读连接(v4.1.1:路径从环境变量读取)
# ============================================================

# 把 _lib 加到 path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "chain-stockmap" / "scripts"))
from _lib.config import get_db_path  # noqa: E402

DB_PATH = get_db_path()  # v4.1.1: 不再硬编码


class _ReadOnlyDuckDB:
    """DuckDB 只读连接 + 操作审计"""
    def __init__(self):
        try:
            import duckdb
            self._conn = duckdb.connect(DB_PATH, read_only=True)
            self._sql_log = []
        except Exception as e:
            raise RuntimeError(f"DuckDB 只读连接失败: {e}")

    def list_sector_etfs(self):
        sql = """
        SELECT ts_code, name, benchmark, list_date
        FROM fund_basic
        WHERE invest_type='被动指数型' AND status='L'
        ORDER BY ts_code
        """
        self._sql_log.append(("SELECT", sql, ()))
        return self._conn.execute(sql).fetchall()

    def fetch_window_return(self, ts_code, days):
        sql = """
        SELECT trade_date, close
        FROM fund_daily
        WHERE ts_code = ?
        ORDER BY trade_date DESC
        LIMIT ?
        """
        params = (ts_code, days)
        self._sql_log.append(("SELECT", sql, params))
        rows = self._conn.execute(sql, params).fetchall()
        if len(rows) < 2:
            return (None, None, None, None)
        last_close = float(rows[0][1])
        last_date = str(rows[0][0])
        first_close = float(rows[-1][1])
        first_date = str(rows[-1][0])
        if first_close == 0:
            return (None, last_close, last_date, first_date)
        ret = round((last_close - first_close) / first_close * 100, 2)
        return (ret, last_close, last_date, first_date)

    def close(self):
        if self._sql_log:
            print(f"[DuckDB-AUDIT] 本次发起 {len(self._sql_log)} 个 SELECT,无可写操作",
                  file=sys.stderr)
        try:
            self._conn.close()
        except Exception:
            pass


# ============================================================
# B. 行业分类(基于 name + benchmark 关键词)
# ============================================================

def classify_sector(name, benchmark):
    """按名称 + 跟踪指数做行业分类"""
    text = (name or "") + " " + (benchmark or "")
    rules = [
        ("光伏",         ["光伏", "太阳能"]),
        ("AI",           ["人工智能", "AI"]),
        ("机器人/智造",  ["机器人", "智能制造", "高端装备"]),
        ("半导体/科技",  ["半导体", "芯片", "集成电路", "存储", "电子",
                         "信息技术", "计算机", "软件", "数字经济", "科技"]),
        ("新能源车",     ["新能源车", "新能源汽车", "锂电池", "动力电池",
                         "智能汽车", "智能驾驶", "车联网", "汽车"]),
        ("储能/碳中和",  ["储能", "碳中和", "低碳", "环保", "ESG"]),
        ("医药生物",     ["医药", "医疗", "生物", "创新药", "疫苗", "中药",
                         "健康", "CXO"]),
        ("军工",         ["军工", "国防", "航空", "航天"]),
        ("消费",         ["消费", "食品", "饮料", "酒", "家电", "商贸",
                         "零售", "必选消费", "可选消费"]),
        ("金融",         ["银行", "证券", "保险", "非银", "金融"]),
        ("地产基建",     ["地产", "房地产", "建材", "基建", "建筑", "工程",
                         "水泥"]),
        ("周期资源",     ["煤炭", "钢铁", "有色", "化工", "石油", "油气",
                         "资源", "黄金", "白银"]),
        ("TMT/传媒",     ["传媒", "游戏", "影视", "互联网", "通信", "5G",
                         "电信", "移动互联网"]),
        ("农业",         ["农业", "畜牧", "农牧", "粮食", "种业", "生猪",
                         "猪", "饲料"]),
        ("港股",         ["恒生", "港股", "H股", "香港"]),
        ("海外",         ["纳斯达克", "标普", "道琼斯", "QDII", "日经",
                         "德国", "印度", "富时", "越南", "韩国", "东南亚"]),
        ("宽基",         ["沪深300", "中证500", "中证1000", "上证50",
                         "科创50", "创业板", "上证指数", "MSCI", "中证A",
                         "红利", "高股息", "央企", "国企", "低波", "质量",
                         "成长", "价值", "基本面"]),
        ("债券",         ["债券", "国债", "城投", "信用", "可转债",
                         "地方债"]),
        ("商品期货",     ["豆粕", "有色金属期货", "能源化工期货",
                         "黄金现货", "原油"]),
    ]
    for label, keywords in rules:
        for kw in keywords:
            if kw in text:
                return label
    return "其它主题"


# ============================================================
# C. 主流程
# ============================================================

def fetch_all(output_path):
    """主入口:扫所有 ETF,算多窗口涨幅,按行业聚合"""
    db = None
    try:
        db = _ReadOnlyDuckDB()
    except Exception as e:
        print(f"[FATAL] DuckDB 只读连接失败,无法扫描: {e}", file=sys.stderr)
        sys.exit(1)

    print("==> 扫描被动指数型 ETF 清单...")
    etfs = db.list_sector_etfs()
    print(f"   找到 {len(etfs)} 只 ETF")

    rows = []
    n = 0
    for ts_code, name, benchmark, list_date in etfs:
        n += 1
        ret_12m, last_close, last_date, first_date_12m = db.fetch_window_return(ts_code, 250)
        ret_6m, _, _, _ = db.fetch_window_return(ts_code, 126)
        ret_3m, _, _, _ = db.fetch_window_return(ts_code, 63)
        ret_1m, _, _, _ = db.fetch_window_return(ts_code, 21)

        sector = classify_sector(name, benchmark)

        rows.append({
            "ts_code": ts_code,
            "name": name,
            "benchmark": benchmark,
            "list_date": list_date,
            "sector": sector,
            "last_date": last_date,
            "last_close": last_close,
            "ret_1m_pct": ret_1m,
            "ret_3m_pct": ret_3m,
            "ret_6m_pct": ret_6m,
            "ret_12m_pct": ret_12m,
        })
        if n % 100 == 0:
            print(f"   已处理 {n}/{len(etfs)} 只")

    db.close()

    out = {
        "meta": {
            "fetched_at": datetime.now().isoformat(),
            "etf_count": len(rows),
            "data_source": "Tushare DuckDB(只读) — fund_basic + fund_daily",
            "windows_days": {"1M": 21, "3M": 63, "6M": 126, "12M": 250},
            "access_mode": "read_only",
        },
        "etfs": rows,
    }

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\n==> 写入 {output_path}({Path(output_path).stat().st_size // 1024} KB)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: fetch_radar_data.py <output.json>")
        sys.exit(1)
    fetch_all(sys.argv[1])
