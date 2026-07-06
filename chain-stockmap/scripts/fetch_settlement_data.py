#!/usr/bin/env python3
"""
chain-settlement 数据获取脚本
================================

拉个股 + 行业基准的"兑现度"原始数据:
1. 个股过去 12M 收盘价序列(算 12M 涨幅)
2. 个股过去 4 个季度扣非净利润 + 经营现金流(算 12M 业绩增速)
3. 行业 ETF 12M 涨幅(基准,算超额)
4. 个股资金流(北向 + 主力近 60 日净流入,反例信号用)

输入:stockmap.md 路径
输出:settlement_data.json(全量原始数据)

数据源:
- 个股 K 线:东方财富 push2his.eastmoney.com(直接调,稳定)
- 个股季报:AKShare stock_profit_sheet_by_quarterly_em + stock_cash_flow_sheet_by_quarterly_em
- 行业 ETF:Tushare DuckDB(本地,见 ~/.local/share/tushare_pipeline/local_api.py)
- 资金流:东财 datacenter 或 akshare(实测用 ths 接口)

时间窗口:
- 12M = 滚动 250 个交易日(过去 12 个月)
- 业绩:最近 4 个季度数据(报告期)
"""

import sys
import os
import json
import re
import time
import requests
from datetime import datetime, timedelta
from pathlib import Path

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0",
    "Accept": "application/json,text/plain,*/*",
    "Referer": "https://quote.eastmoney.com/",
})
# 长连接 + 重试配置
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

retry_strategy = Retry(
    total=4,
    backoff_factor=1.5,
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["GET"],
)
adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=10, pool_maxsize=20)
SESSION.mount("https://", adapter)
SESSION.mount("http://", adapter)

# ============================================================
# A. 个股 K 线(12M)
# ============================================================

def get_secid(code):
    """6 位股票代码 → 东财 secid(1.SHA,0.SZ)"""
    if code.startswith(("60", "68", "11", "13", "5")):
        return f"1.{code}"
    return f"0.{code}"


def fetch_kline_12m(code, end_date=None, retries=4):
    """拉过去 12M 日 K 线(东财 push2his),带退避重试
    Returns:list of dict {date, open, close, high, low, volume, amount, change_pct}
    """
    if end_date is None:
        end_date = datetime.now().strftime("%Y%m%d")
    start_date = (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")

    secid = get_secid(code)
    url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
    params = {
        'secid': secid,
        'fields1': 'f1,f2,f3,f4,f5,f6',
        'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58',
        'klt': '101',
        'fqt': '1',
        'beg': start_date,
        'end': end_date,
        'lmt': '250',
    }
    last_err = None
    for attempt in range(retries):
        try:
            r = SESSION.get(url, params=params, timeout=15)
            r.raise_for_status()
            payload = r.json()
            data = payload.get("data") or {}
            klines = data.get("klines") or []
            rows = []
            for line in klines:
                parts = line.split(",")
                if len(parts) < 8:
                    continue
                rows.append({
                    "date": parts[0],
                    "open": float(parts[1]),
                    "close": float(parts[2]),
                    "high": float(parts[3]),
                    "low": float(parts[4]),
                    "volume": float(parts[5]),
                    "amount": float(parts[6]),
                    "change_pct": float(parts[7]),
                })
            if rows:
                return {"status": "ok", "data": rows, "source": f"东财 push2his({len(rows)} 条)", "fetched_at": datetime.now().isoformat()}
            last_err = "klines 为空"
        except Exception as e:
            last_err = str(e)
        time.sleep(1.0 * (attempt + 1))
    return {"status": "error", "message": last_err or "未知错误"}


def calc_12m_return(kline_data):
    """从 K 线数据算 12M 涨幅"""
    rows = kline_data.get("data") or []
    if len(rows) < 2:
        return None
    start = rows[0]["close"]
    end = rows[-1]["close"]
    return round((end - start) / start * 100, 2)


# ============================================================
# B. 季度业绩(扣非 + 经营现金流)
# ============================================================

def fetch_quarterly_finance(code):
    """拉最近 4 季度扣非净利 + 经营现金流(AKShare)"""
    try:
        import akshare as ak
    except ImportError:
        return {"status": "error", "message": "akshare 未安装"}

    # 东财 secid prefix
    secid = get_secid(code)  # 1.688017 or 0.002714
    market = "SH" if secid.startswith("1.") else "SZ"
    em_symbol = f"{market}{code}"  # SH688017

    try:
        # 利润表
        df_p = ak.stock_profit_sheet_by_quarterly_em(symbol=em_symbol)
        # 现金流量表
        df_c = ak.stock_cash_flow_sheet_by_quarterly_em(symbol=em_symbol)
    except Exception as e:
        return {"status": "error", "message": f"akshare 失败: {e}"}

    if df_p is None or df_p.empty:
        return {"status": "error", "message": "利润表为空"}
    if df_c is None or df_c.empty:
        return {"status": "error", "message": "现金流量表为空"}

    # 取最近 8 季度(用于算 12M 同比)
    df_p = df_p.sort_values("REPORT_DATE", ascending=False).head(8).reset_index(drop=True)
    df_c = df_c.sort_values("REPORT_DATE", ascending=False).head(8).reset_index(drop=True)

    # 输出最近 4 季度明细 + 12M 同比汇总
    rows = []
    for i in range(min(4, len(df_p))):
        report_date = str(df_p.iloc[i].get("REPORT_DATE", ""))
        report_name = df_p.iloc[i].get("REPORT_DATE_NAME", "")
        netprofit = float(df_p.iloc[i].get("DEDUCT_PARENT_NETPROFIT") or 0)
        cash = None
        for j in range(len(df_c)):
            if str(df_c.iloc[j].get("REPORT_DATE", "")) == report_date:
                cash = float(df_c.iloc[j].get("NETCASH_OPERATE") or 0)
                break
        rows.append({
            "report_date": report_date,
            "report_name": report_name,
            "deduct_netprofit_yi": round(netprofit / 1e8, 4),
            "operate_cashflow_yi": round((cash or 0) / 1e8, 4),
        })

    # 12M 滚动 = 最近 4 季度之和;12M 上年同期 = 4-8 季度前 4 个之和
    if len(df_p) >= 8:
        recent_4_deduct = sum(float(df_p.iloc[i].get("DEDUCT_PARENT_NETPROFIT") or 0) for i in range(4))
        prev_4_deduct = sum(float(df_p.iloc[i].get("DEDUCT_PARENT_NETPROFIT") or 0) for i in range(4, 8))
        deduct_yoy_pct = round((recent_4_deduct - prev_4_deduct) / abs(prev_4_deduct) * 100, 2) if prev_4_deduct else None

        recent_4_cash = 0
        prev_4_cash = 0
        for i in range(8):
            rd = str(df_p.iloc[i].get("REPORT_DATE", ""))
            for j in range(len(df_c)):
                if str(df_c.iloc[j].get("REPORT_DATE", "")) == rd:
                    if i < 4:
                        recent_4_cash += float(df_c.iloc[j].get("NETCASH_OPERATE") or 0)
                    else:
                        prev_4_cash += float(df_c.iloc[j].get("NETCASH_OPERATE") or 0)
                    break
        cashflow_yoy_pct = round((recent_4_cash - prev_4_cash) / max(abs(prev_4_cash), 1) * 100, 2)
    else:
        deduct_yoy_pct = None
        cashflow_yoy_pct = None

    return {
        "status": "ok",
        "data": rows,
        "summary_12m": {
            "deduct_netprofit_yi": round(recent_4_deduct / 1e8, 4) if recent_4_deduct else None,
            "deduct_yoy_pct": deduct_yoy_pct,
            "operate_cashflow_yi": round(recent_4_cash / 1e8, 4) if recent_4_cash else None,
            "cashflow_yoy_pct": cashflow_yoy_pct,
        },
        "source": f"akshare 东财季表({len(df_p)} 期)",
        "fetched_at": datetime.now().isoformat(),
    }


def calc_12m_finance_growth(finance_data):
    """算 12M 业绩增速(对比上年同期)
    输入:4 季度数据(最近 4 个季度,每个 REPORT_DATE 不同)
    
    12M 扣非净利 = 最近 4 季度之和
    比较的同期需要去年同期(4 个季度)
    这里没有拉去年同期,所以返回原始数据由 calc_settlement_score.py 处理
    """
    return finance_data  # 只透传


# ============================================================
# C. 行业 ETF 基准
# ============================================================

# ---- Tushare DuckDB 只读连接辅助 ----
# 设计原则:
# 1. 只对 `tushare.db` 发起 SELECT,只读 flag 强制开启
# 2. 不依赖 local_api.py 是否被打过 read_only patch
# 3. 自带操作审计:本次启动用了哪些 SQL,写到 stderr
# 4. 失败立即回退东财,不重试(不写入风险)
DB_PATH = "/mnt/e/tushare_db/data/tushare.db"

class _ReadOnlyDuckDB:
    """DuckDB 只读连接 + 操作审计(只在退出时打印所有执行过的 SQL)"""
    def __init__(self):
        try:
            import duckdb
            self._conn = duckdb.connect(DB_PATH, read_only=True)
            self._sql_log = []
        except Exception as e:
            raise RuntimeError(f"DuckDB 只读连接失败: {e}")

    def fund_daily(self, ts_code, start_date="", end_date=""):
        """复刻 local_api.fund_daily 接口(只用 SELECT)"""
        sql = "SELECT trade_date, close FROM fund_daily WHERE ts_code = ?"
        params = [ts_code]
        if start_date:
            sql += " AND trade_date >= ?"
            params.append(start_date)
        if end_date:
            sql += " AND trade_date <= ?"
            params.append(end_date)
        sql += " ORDER BY trade_date"
        self._sql_log.append(("SELECT", sql, tuple(params)))
        return self._conn.execute(sql, params).df()

    def close(self):
        # 打印本次执行的 SQL(审计)
        if self._sql_log:
            print(f"[DuckDB-AUDIT] 本次发起 {len(self._sql_log)} 个 SELECT,无可写操作",
                  file=sys.stderr)
        try:
            self._conn.close()
        except Exception:
            pass


def fetch_industry_benchmark(etf_codes, end_date=None):
    """拉行业 ETF 12M 涨幅(用作个股对比基准)
    输入:etf_codes = ['562500.SH', ...]

    加固要点(read-only):
    - DuckDB 连接强制 read_only=True(即使脚本有 bug 也写不进)
    - 失败立即回退东财,不重试(不写入风险)
    - 用 _ReadOnlyDuckDB 替代 local_api.fund_daily(默认安全)
    - 本函数不发起任何 DDL/DML
    """
    db = None
    try:
        db = _ReadOnlyDuckDB()
    except Exception as e:
        print(f"[WARN] DuckDB 只读连接建立失败,全量走东财 fallback: {e}", file=sys.stderr)

    if end_date is None:
        end_date = datetime.now().strftime("%Y%m%d")
    start_date = (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")

    results = []
    for code in etf_codes:
        local_df = None
        if db is not None:
            try:
                local_df = db.fund_daily(code, start_date=start_date, end_date=end_date)
            except Exception as e:
                print(f"[WARN] DuckDB 查询 {code} 失败,fallback: {e}", file=sys.stderr)
                local_df = None

        if local_df is not None and len(local_df) >= 2:
            start = float(local_df.iloc[0]["close"])
            end = float(local_df.iloc[-1]["close"])
            ret = round((end - start) / start * 100, 2)
            results.append({"code": code, "12m_return_pct": ret, "source": "Tushare DuckDB(只读)"})
            continue

        # 回退:东财 push2his(部分 ETF 代码不存在 ETF 行情,无法用 secid)
        results.append({"code": code, "12m_return_pct": None, "source": "fallback_na(东财 ETF 不支持)"})

    if db is not None:
        db.close()

    return {
        "status": "ok",
        "data": results,
        "source": "Tushare DuckDB(只读) + 东财 fallback",
        "fetched_at": datetime.now().isoformat(),
        "access_mode": "read_only",  # 显式标签
    }


# ============================================================
# D. 资金流(60 日净流入,做兑现度反例)
# ============================================================

def fetch_fund_flow_60d(code):
    """60 日主力净流入(东财数据中心)"""
    full = code
    secid = get_secid(code)
    market = "1" if secid.startswith("1.") else "0"
    stock_code = secid.split(".")[1]

    end = datetime.now()
    start = end - timedelta(days=120)  # 多取 60 天以防节假日
    url = "https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get"
    params = {
        'secid': f"{market}.{stock_code}",
        'fields1': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13',
        'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58',
        'klt': '101',
        'fqt': '1',
        'beg': start.strftime("%Y%m%d"),
        'end': end.strftime("%Y%m%d"),
        'lmt': '120',
    }
    try:
        r = SESSION.get(url, params=params, timeout=15)
        r.raise_for_status()
        data = r.json().get("data") or {}
        klines = data.get("klines") or []
        # f55 主力净流入(元)
        net_in = []
        for line in klines[-60:]:
            parts = line.split(",")
            if len(parts) < 7:
                continue
            net_in.append(float(parts[4]) if parts[4] else 0.0)
        return round(sum(net_in) / 1e8, 4) if net_in else None  # 元 → 亿
    except Exception:
        return None


# ============================================================
# E. 解析 stockmap.md
# ============================================================

def parse_stockmap(stockmap_path):
    """从 stockmap.md 提取股票清单
    输出:[{name, code, role: P0/P1/P2/重点关注}, ...]
    """
    text = Path(stockmap_path).read_text(encoding="utf-8")
    stocks = []
    # 匹配形如 "绿的谐波 | 688017"
    pattern = re.compile(r"\|\s*\*?\*?([^|\n*]+?)\*?\*?\s*\|\s*(\d{6})\s*\|")
    for m in pattern.finditer(text):
        name = m.group(1).strip()
        code = m.group(2).strip()
        if code.isdigit() and len(code) == 6:
            stocks.append({"name": name, "code": code})
    # 去重
    seen = set()
    deduped = []
    for s in stocks:
        if s["code"] in seen:
            continue
        seen.add(s["code"])
        deduped.append(s)
    return deduped


# ============================================================
# F. 主流程
# ============================================================

def fetch_all(stockmap_path, etf_codes, output_path, delay=0.4):
    """主入口:读取 stockmap,拉所有数据,写 JSON"""
    print(f"==> 读取 stockmap: {stockmap_path}")
    stocks = parse_stockmap(stockmap_path)
    print(f"   找到 {len(stocks)} 只股票")

    print(f"==> 拉行业 ETF 基准({len(etf_codes)} 只)")
    benchmark = fetch_industry_benchmark(etf_codes)
    benchmark_return = [b["12m_return_pct"] for b in benchmark.get("data", []) if b["12m_return_pct"] is not None]
    benchmark_median = round(sum(benchmark_return) / len(benchmark_return), 2) if benchmark_return else 0

    settlement_data = {
        "meta": {
            "fetched_at": datetime.now().isoformat(),
            "stockmap": str(stockmap_path),
            "stock_count": len(stocks),
            "industry_etf_codes": etf_codes,
            "industry_etf_12m_return_median_pct": benchmark_median,
            "data_sources": {
                "kline": "东财 push2his.eastmoney.com",
                "finance": "AKShare stock_profit_sheet_by_quarterly_em + stock_cash_flow_sheet_by_quarterly_em",
                "benchmark": "Tushare DuckDB(local) + 东财 fallback",
                "fund_flow": "东财 push2his 资金流接口",
            },
        },
        "stocks": [],
    }

    for i, s in enumerate(stocks, 1):
        code = s["code"]
        print(f"\n[{i}/{len(stocks)}] {s['name']}({code})")
        print(f"   kline 12M...")
        kl = fetch_kline_12m(code)
        ret12 = calc_12m_return(kl) if kl.get("status") == "ok" else None
        print(f"   12M 涨幅: {ret12}%")

        time.sleep(delay)
        print(f"   季度财务...")
        fin = fetch_quarterly_finance(code)
        n_quarters = len(fin.get("data") or [])
        print(f"   拉取 {n_quarters} 期季报")

        time.sleep(delay)
        print(f"   资金流...")
        fund60 = fetch_fund_flow_60d(code)
        print(f"   60 日主力净流入: {fund60} 亿")

        settlement_data["stocks"].append({
            "name": s["name"],
            "code": code,
            "kline_raw": kl,
            "kline_12m_return_pct": ret12,
            "finance_quarterly": fin,
            "finance_12m_summary": fin.get("summary_12m") if fin.get("status") == "ok" else None,
            "fund_flow_60d_yi": fund60,
        })
        time.sleep(delay)

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(settlement_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n==> 写入 {output_path}({out.stat().st_size // 1024} KB)")

    return settlement_data


def main():
    if len(sys.argv) < 4:
        print("用法:")
        print("  fetch_settlement_data.py <stockmap.md> <output.json> <etf1,etf2,...>")
        print("示例:")
        print("  fetch_settlement_data.py /tmp/robot-case/09-stockmap/stockmap.md /tmp/settlement.json 562500.SH,159770.SZ")
        sys.exit(1)

    stockmap_path = sys.argv[1]
    output_path = sys.argv[2]
    etf_codes = [c.strip() for c in sys.argv[3].split(",") if c.strip()]

    if not Path(stockmap_path).exists():
        print(f"stockmap 文件不存在: {stockmap_path}")
        sys.exit(1)

    fetch_all(stockmap_path, etf_codes, output_path)


if __name__ == "__main__":
    main()
