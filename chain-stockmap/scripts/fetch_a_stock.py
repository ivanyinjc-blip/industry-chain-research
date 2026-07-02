#!/usr/bin/env python3
"""
A股数据获取脚本 v3 - 真实多源接口
数据源:
- 实时行情/估值: 东方财富 push2.eastmoney.com(单股 API,稳定)
- 财务摘要: 东方财富 + AKShare stock_individual_fund_flow(主力资金)
- 技术面: AKShare stock_zh_a_hist(日线) + 自计算均线/MACD/RSI/KDJ
- 资金流向: AKShare stock_individual_fund_flow(主力)

设计参考:harrischen/invest + gushifenxi 三层数据诚实度
"""
import sys
import json
import re
import time
import requests
from datetime import datetime, timedelta

# === 全局 Session + UA ===
SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://quote.eastmoney.com/",
})


def http_get(url, timeout=15, retries=3, encoding="utf-8"):
    """带退避重试的 HTTP GET"""
    last_err = None
    for i in range(retries):
        try:
            r = SESSION.get(url, timeout=timeout)
            r.encoding = encoding
            if r.status_code == 200:
                return r.text
            last_err = f"HTTP {r.status_code}"
        except Exception as e:
            last_err = str(e)
            if i < retries - 1:
                time.sleep(1.0 * (i + 1))
    return None


def safe_float(v, default=None):
    try:
        if v is None or v == "" or v == "-":
            return default
        return float(v)
    except (ValueError, TypeError):
        return default


def get_secid(code):
    """股票代码 → 东财 secid(1=沪市,0=深市)"""
    prefix = 1 if code.startswith(("6", "9", "5")) else 0
    return f"{prefix}.{code}"


# ==================== quote ====================

def fetch_quote(code):
    """东方财富 push2 单股接口 - 实时行情 + 估值"""
    secid = get_secid(code)
    fields = "f43,f44,f45,f46,f47,f48,f57,f58,f60,f50,f51,f52,f117,f168,f167,f59,f292,f191,f192,f292,f173"
    url = f"https://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields={fields}"
    raw = http_get(url, retries=3)
    if not raw:
        return {"status": "error", "message": "东财行情 API 失败"}
    
    try:
        d = json.loads(raw).get("data", {})
    except Exception as e:
        return {"status": "error", "message": f"JSON 解析失败: {e}"}
    
    if not d:
        return {"status": "error", "message": "返回数据为空"}

    # f43=最新价(分),f44=最高,f45=最低,f46=开盘,f47=成交量(手),
    # f48=成交额(元),f50=量比,f51=涨停价,f52=跌停价,
    # f57=代码,f58=名称,f60=昨收,f117=总市值(元),f168=换手率(%),f167=市净率,
    # f292=流通市值(元),f191=市盈率(动),f192=市净率
    price = safe_float(d.get("f43"), 0) / 100
    prev_close = safe_float(d.get("f60"), 0) / 100
    high = safe_float(d.get("f44"), 0) / 100
    low = safe_float(d.get("f45"), 0) / 100
    open_p = safe_float(d.get("f46"), 0) / 100
    change_pct = round((price - prev_close) / prev_close * 100, 2) if prev_close else 0

    return {
        "status": "ok",
        "source": "东方财富 push2(单股)",
        "fetched_at": datetime.now().isoformat(),
        "data": {
            "code": code,
            "name": d.get("f58", ""),
            "price": price,
            "prev_close": prev_close,
            "open": open_p,
            "high": high,
            "low": low,
            "change_pct": change_pct,
            "volume_hand": int(safe_float(d.get("f47"), 0)),
            "amount_yuan": safe_float(d.get("f48"), 0),
            "volume_ratio": safe_float(d.get("f50")),  # 量比
            "turnover_pct": safe_float(d.get("f168")),
            "pe_dynamic": safe_float(d.get("f191"), 0) / 100,  # 东财是 % 形式
            "pb": safe_float(d.get("f167"), 0) / 100,
            "market_cap_yuan": safe_float(d.get("f117"), 0),
            "circulating_cap_yuan": safe_float(d.get("f292"), 0),
            "market_cap_yi": round(safe_float(d.get("f117"), 0) / 1e8, 2),
            "high_limit": safe_float(d.get("f51"), 0) / 100,
            "low_limit": safe_float(d.get("f52"), 0) / 100,
        }
    }


# ==================== finance ====================

def _to_full_code(code):
    """股票代码 → 东财完整代码 (SH600519 / SZ002714)"""
    market, stock_code = get_secid(code).split(".")
    prefix = "SH" if market == "1" else "SZ"
    return f"{prefix}{stock_code}"


def fetch_finance(code):
    """财务摘要 - 东方财富 datacenter(主要财务指标 RPT_F10_FINANCE_MAINFINADATA)"""
    full = _to_full_code(code)  # SH600519 / SZ002714
    sec_postfix = full[:2]     # SH / SZ
    # SECUCODE 字段格式为 "600519.SH" / "002714.SZ"
    secucode = f"{full[2:]}.{sec_postfix}"
    url = (
        "https://datacenter-web.eastmoney.com/api/data/v1/get?"
        "reportName=RPT_F10_FINANCE_MAINFINADATA&columns=ALL&"
        f"filter=(SECUCODE%3D%22{secucode}%22)&"
        "pageNumber=1&pageSize=4&sortTypes=-1&sortColumns=REPORT_DATE"
    )
    raw = http_get(url, retries=3)
    if not raw:
        return {"status": "error", "message": "东财财务 API(datacenter)失败"}

    try:
        result = json.loads(raw).get("result", {})
    except Exception as e:
        return {"status": "error", "message": f"JSON 解析失败: {e}"}

    if not result or not result.get("data"):
        return {"status": "error", "message": "财务数据为空"}

    latest = result["data"][0]

    return {
        "status": "ok",
        "source": "东方财富 datacenter(主要财务指标)",
        "fetched_at": datetime.now().isoformat(),
        "data": {
            "code": code,
            "name": latest.get("SECURITY_NAME_ABBR", ""),
            "report_period": latest.get("REPORT_DATE_NAME", ""),
            "report_type": latest.get("REPORT_TYPE", ""),
            # 每股
            "eps": safe_float(latest.get("EPSJB")),        # 基本每股收益(元)
            "bvps": safe_float(latest.get("BPS")),         # 每股净资产(元)
            # 营收 / 利润(元→亿)
            "revenue_yi": round(safe_float(latest.get("TOTALOPERATEREVE"), 0) / 1e8, 2),
            "net_profit_yi": round(safe_float(latest.get("PARENTNETPROFIT"), 0) / 1e8, 2),
            # 利润率
            "gross_margin": safe_float(latest.get("XSMLL")),   # 销售毛利率 %
            "net_margin": safe_float(latest.get("XSJLL")),     # 销售净利率 %
            "roe": safe_float(latest.get("ROEJQ")),            # 净资产收益率 %
            "roa": safe_float(latest.get("ZZCJLL")),           # 总资产净利率 %
            # 同比
            "yoy_revenue": safe_float(latest.get("TOTALOPERATEREVETZ")),   # 营收同比 %
            "yoy_profit": safe_float(latest.get("PARENTNETPROFITTZ")),    # 净利润同比 %
            # 财务结构
            "debt_ratio": safe_float(latest.get("ZCFZL")),     # 资产负债率 %
            # 历史期数(用于看季度趋势)
            "history_count": len(result["data"]),
        }
    }


# ==================== technical ====================

def calc_ma(series, n):
    return series.rolling(window=n, min_periods=1).mean()


def calc_macd(series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    dif = ema_fast - ema_slow
    dea = dif.ewm(span=signal, adjust=False).mean()
    macd = (dif - dea) * 2
    return dif, dea, macd


def calc_rsi(series, n=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(window=n, min_periods=1).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=n, min_periods=1).mean()
    rs = gain / loss.replace(0, 1e-9)
    return 100 - (100 / (1 + rs))


def calc_kdj(df, n=9):
    low_n = df["low"].rolling(window=n, min_periods=1).min()
    high_n = df["high"].rolling(window=n, min_periods=1).max()
    rsv = (df["close"] - low_n) / (high_n - low_n).replace(0, 1e-9) * 100
    k = rsv.ewm(alpha=1/3, adjust=False).mean()
    d = k.ewm(alpha=1/3, adjust=False).mean()
    j = 3 * k - 2 * d
    return k, d, j


def fetch_technical(code, days=180):
    """技术面 - AKShare 日线 + 自计算"""
    try:
        import akshare as ak
        ak.requests = SESSION
    except ImportError:
        return {"status": "error", "message": "akshare 未安装"}

    # 先取行情来获取股票名称
    quote_cached = fetch_quote(code).get("data", {})

    end = datetime.now().strftime("%Y%m%d")
    start = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")
    
    last_err = None
    for attempt in range(3):
        try:
            df = ak.stock_zh_a_hist(
                symbol=code, period="daily",
                start_date=start, end_date=end, adjust="qfq"
            )
            if df is None or df.empty:
                last_err = "日线数据为空"
                time.sleep(1)
                continue

            col_map = {"日期": "date", "开盘": "open", "收盘": "close",
                       "最高": "high", "最低": "low", "成交量": "volume",
                       "成交额": "amount", "涨跌幅": "pct_change", "换手率": "turnover"}
            df = df.rename(columns=col_map)
            if "date" not in df.columns:
                df["date"] = df.index.astype(str)
            df["date"] = df["date"].astype(str)
            df = df.sort_values("date").reset_index(drop=True)

            close = df["close"].astype(float)
            current = float(close.iloc[-1])

            ma5 = float(calc_ma(close, 5).iloc[-1])
            ma10 = float(calc_ma(close, 10).iloc[-1])
            ma20 = float(calc_ma(close, 20).iloc[-1])
            ma60 = float(calc_ma(close, 60).iloc[-1]) if len(close) >= 60 else None

            dif, dea, macd_hist = calc_macd(close)
            rsi14 = float(calc_rsi(close, 14).iloc[-1])
            k, d, j = calc_kdj(df)
            k_val, d_val, j_val = float(k.iloc[-1]), float(d.iloc[-1]), float(j.iloc[-1])

            # 多因子评分(借鉴 invest)
            trend_score = 0
            if current > ma5: trend_score += 1
            if current > ma10: trend_score += 1
            if current > ma20: trend_score += 1
            if ma60 and current > ma60: trend_score += 1
            if dif.iloc[-1] > dea.iloc[-1]: trend_score += 1
            trend = trend_score / 5 * 5

            if 50 <= rsi14 <= 70:
                cycle = 4
            elif 40 <= rsi14 < 50 or 70 < rsi14 <= 80:
                cycle = 3
            elif rsi14 < 30:
                cycle = 4.5
            else:
                cycle = 2

            if trend >= 4:
                stage = "强势上行"
            elif trend >= 3:
                stage = "健康上行"
            elif trend >= 2:
                stage = "震荡整理"
            else:
                stage = "弱势下行"

            bias_ma20 = round((current - ma20) / ma20 * 100, 2)
            window = min(60, len(df))
            high_60d = float(df["high"].tail(window).max())
            low_60d = float(df["low"].tail(window).min())

            return {
                "status": "ok",
                "source": f"AKShare 日线 + 自计算({len(df)} 个交易日)",
                "fetched_at": datetime.now().isoformat(),
                "data": {
                    "code": code,
                    "name": quote_cached["name"] if quote_cached else "",
                    "latest_date": str(df["date"].iloc[-1]),
                    "current_price": round(current, 2),
                    "ma5": round(ma5, 2),
                    "ma10": round(ma10, 2),
                    "ma20": round(ma20, 2),
                    "ma60": round(ma60, 2) if ma60 else None,
                    "macd_dif": round(float(dif.iloc[-1]), 4),
                    "macd_dea": round(float(dea.iloc[-1]), 4),
                    "macd_hist": round(float(macd_hist.iloc[-1]), 4),
                    "rsi_14": round(rsi14, 2),
                    "kdj_k": round(k_val, 2),
                    "kdj_d": round(d_val, 2),
                    "kdj_j": round(j_val, 2),
                    "bias_ma20": bias_ma20,
                    "high_60d": round(high_60d, 2),
                    "low_60d": round(low_60d, 2),
                    "trend_score": round(trend, 2),
                    "cycle_score": cycle,
                    "trend_stage": stage,
                    "support_ma20": round(ma20, 2),
                    "resistance_60d_high": round(high_60d, 2),
                }
            }
        except Exception as e:
            last_err = str(e)
            time.sleep(1.5 * (attempt + 1))
    
    return {"status": "error", "message": f"技术面 3 次重试后失败: {last_err}"}


# ==================== fund_flow ====================

def fetch_fund_flow(code):
    """资金流向 - AKShare stock_individual_fund_flow(必须带 market)"""
    try:
        import akshare as ak
        ak.requests = SESSION
    except ImportError:
        return {"status": "error", "message": "akshare 未安装"}

    # market 参数必须传(否则东财接口返回空)
    market = "sh" if code.startswith(("6", "9", "5")) else "sz"

    # 预取名称
    name_cached = fetch_quote(code).get("data", {}).get("name", "")

    last_err = None
    for attempt in range(3):
        try:
            df = ak.stock_individual_fund_flow(stock=code, market=market)
            if df is None or df.empty:
                last_err = f"资金流向返回为空(market={market})"
                time.sleep(2)
                continue

            latest = df.iloc[-1]
            recent = df.tail(10)

            def pick(row, *candidates):
                for c in candidates:
                    if c in row.index:
                        return row[c]
                return None

            main_net_today = safe_float(pick(latest, "主力净流入-净额", "主力净流入"))
            super_net_today = safe_float(pick(latest, "超大单净流入-净额", "超大单净流入"))
            big_net_today = safe_float(pick(latest, "大单净流入-净额", "大单净流入"))
            mid_net_today = safe_float(pick(latest, "中单净流入-净额", "中单净流入"))
            small_net_today = safe_float(pick(latest, "小单净流入-净额", "小单净流入"))
            latest_date = str(pick(latest, "日期", "date") or latest.name)

            main_col = None
            for c in ("主力净流入-净额", "主力净流入"):
                if c in recent.columns:
                    main_col = c
                    break
            main_10d = float(recent[main_col].sum()) if main_col else 0.0

            return {
                "status": "ok",
                "source": "AKShare stock_individual_fund_flow",
                "fetched_at": datetime.now().isoformat(),
                "data": {
                    "code": code,
                    "name": name_cached,
                    "market": market,
                    "latest_date": latest_date,
                    "main_net_today": main_net_today,
                    "super_net_today": super_net_today,
                    "big_net_today": big_net_today,
                    "mid_net_today": mid_net_today,
                    "small_net_today": small_net_today,
                    "main_net_10d_sum": round(main_10d, 2),
                    "trend": "净流入" if main_10d > 0 else "净流出",
                }
            }
        except Exception as e:
            last_err = str(e)
            time.sleep(2 * (attempt + 1))

    return {"status": "error", "message": f"资金流向 3 次重试后失败: {last_err}"}


# ==================== valuation ====================

def fetch_valuation(code):
    """估值(基于 quote 的 PE/PB + 52 周分位)"""
    quote = fetch_quote(code)
    if quote["status"] != "ok":
        return quote
    d = quote["data"]
    return {
        "status": "ok",
        "source": "东方财富 push2(估值)",
        "fetched_at": datetime.now().isoformat(),
        "data": {
            "code": code,
            "name": d["name"],
            "price": d["price"],
            "pe_dynamic": d["pe_dynamic"],
            "pb": d["pb"],
            "market_cap_yi": d["market_cap_yi"],
            "high_limit": d["high_limit"],
            "low_limit": d["low_limit"],
            "change_pct": d["change_pct"],
        }
    }


def fetch_all(code):
    """一键获取全部"""
    return {
        "quote": fetch_quote(code),
        "valuation": fetch_valuation(code),
        "finance": fetch_finance(code),
        "technical": fetch_technical(code),
        "fund_flow": fetch_fund_flow(code),
    }


def main():
    if len(sys.argv) < 3:
        print(json.dumps({"status": "error", "message": "用法: fetch_a_stock.py <code> <data_type>"}, ensure_ascii=False))
        sys.exit(1)
    
    code = sys.argv[1]
    data_type = sys.argv[2] if len(sys.argv) > 2 else "quote"
    
    handler_map = {
        "quote": fetch_quote,
        "finance": fetch_finance,
        "technical": fetch_technical,
        "fund_flow": fetch_fund_flow,
        "valuation": fetch_valuation,
        "all": fetch_all,
    }
    
    handler = handler_map.get(data_type)
    if not handler:
        print(json.dumps({"status": "error", "message": f"未知数据类型: {data_type}"}, ensure_ascii=False))
        sys.exit(1)
    
    result = handler(code)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
