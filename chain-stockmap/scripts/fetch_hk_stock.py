#!/usr/bin/env python3
"""港股数据获取脚本 - 腾讯 API"""
import sys
import json
import re
from urllib.request import urlopen, Request


def http_get(url, timeout=10):
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("gbk", errors="ignore")
    except Exception as e:
        return None


def fetch_quote(code):
    """腾讯港股: 0700.HK → rt_hk00700"""
    code_clean = code.replace(".HK", "").lstrip("0") or "0"
    code_full = code_clean.zfill(5)
    url = f"https://qt.gtimg.cn/q=hk{code_full}"
    raw = http_get(url)
    if not raw:
        return {"status": "error", "message": "港股 API 失败"}
    
    match = re.search(r'"([^"]+)"', raw)
    if not match:
        return {"status": "error", "message": "解析失败"}
    
    fields = match.group(1).split("~")
    if len(fields) < 40:
        return {"status": "error", "message": f"字段数不足: {len(fields)}"}
    
    return {
        "status": "ok",
        "source": "腾讯港股 API",
        "data": {
            "name": fields[1],
            "code": fields[2],
            "price": float(fields[3] or 0),
            "change_pct": float(fields[32] or 0),
            "high": float(fields[33] or 0),
            "low": float(fields[34] or 0),
            "volume": int(fields[6] or 0),
            "turnover": float(fields[37] or 0),
            "pe": float(fields[39] or 0),
            "market_cap": float(fields[45] or 0),
        }
    }


def fetch_all(code):
    return {"quote": fetch_quote(code)}


def main():
    if len(sys.argv) < 3:
        print(json.dumps({"status": "error", "message": "用法: fetch_hk_stock.py <code> <data_type>"}, ensure_ascii=False))
        sys.exit(1)
    code = sys.argv[1]
    data_type = sys.argv[2]
    
    if data_type == "quote":
        print(json.dumps(fetch_quote(code), ensure_ascii=False, indent=2))
    elif data_type == "all":
        print(json.dumps(fetch_all(code), ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"status": "placeholder", "message": f"{data_type} 建议接 AKShare 港股接口"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
