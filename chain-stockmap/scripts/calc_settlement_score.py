#!/usr/bin/env python3
"""
chain-settlement 兑现度评分算法
================================

输入:settlement_data.json(由 fetch_settlement_data.py 生成)
输出:settlement_scores.json(每只股票的兑现度评分 + 4 象限 + 关注池排序)

评分公式(P0 已锁定):

承诺兑现度 S = 0.6 × Ps + 0.4 × Pf

其中:
- Ps(股价兑现度,0-10):
  Ps = clip(12M 涨幅 - 行业中位数涨幅, -50pp, +100pp) / 15 + 5
  行业中位数 = 5 分;超额 +100pp = 10;低 -50pp = 0

- Pf(业绩兑现度,0-10):
  Pf = 0.5 × 扣非净利 12M 增速超额 + 0.5 × 经营现金流 12M 增量超额

  扣非净利:
    Np = clip(扣非 12M 增速 - 行业中位数增速, -50pp, +200pp) / 25 + 5
  经营现金流:
    Cp = clip(经营现金流 12M 同比 - 行业中位数同比, -50%, +200%) / 20 + 5

4 象限分类(按 Ps × Pf 二维):
- Q1:Ps>=6 & Pf>=6  同行抢筹(警惕)
- Q2:Ps>=6 & Pf<6   兑现期/终结期(规避)
- Q3:Ps<6 & Pf>=6   价值洼地(关注池 ★)
- Q4:Ps<6 & Pf<6    潜伏/没起来(观察池)

关注池重排:
1. Q3 标的按 S 降序排入关注池
2. Q1 中 S>=8 且 Pf 仍合理的保留作为次要关注
3. Q2 全部入规避池
4. Q4 业绩恶化的入观察池
"""

import sys
import json
from pathlib import Path


def clip(v, lo, hi):
    """数值裁剪到 [lo, hi]"""
    return max(lo, min(hi, v))


def percentile_to_score(delta, lo, hi, base=5):
    """差值 → 0-10 分
    delta: 实际 - 行业中位数(可以是 %, pp, 倍数)
    lo/hi: 差值的最小/最大基准
    base: 0 分和 10 分等价于此 base(行业基准 → 5 分)
    """
    if delta >= hi:
        return 10
    if delta <= lo:
        return 0
    return round((delta - lo) / (hi - lo) * (10 - base) + base, 2)


# ============================================================
# 主算法
# ============================================================

def calc_scores(settlement_data):
    """对每只股票算兑现度评分 + 象限"""
    meta = settlement_data["meta"]
    benchmark_12m = meta.get("industry_etf_12m_return_median_pct", 0)

    # 业绩预热:取出所有股票的 12M 同比,算行业中位数
    deduct_yoy_list = []
    cash_yoy_list = []
    for s in settlement_data["stocks"]:
        sum12 = s.get("finance_12m_summary") or {}
        dy = sum12.get("deduct_yoy_pct")
        cy = sum12.get("cashflow_yoy_pct")
        if dy is not None:
            deduct_yoy_list.append(dy)
        if cy is not None:
            cash_yoy_list.append(cy)

    def median(lst):
        if not lst:
            return 0
        s = sorted(lst)
        n = len(s)
        return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2

    deduct_industry_median = median(deduct_yoy_list)
    cash_industry_median = median(cash_yoy_list)

    scored = []
    for s in settlement_data["stocks"]:
        code = s["code"]
        name = s["name"]
        sum12 = s.get("finance_12m_summary") or {}

        # Ps(股价兑现度)
        ret12 = s.get("kline_12m_return_pct")
        if ret12 is None:
            ps = None
        else:
            delta = ret12 - benchmark_12m
            ps = percentile_to_score(delta, lo=-50, hi=100, base=5)

        # Pf(业绩兑现度)
        deduct_yoy = sum12.get("deduct_yoy_pct")
        cash_yoy = sum12.get("cashflow_yoy_pct")
        if deduct_yoy is None and cash_yoy is None:
            pf = None
        else:
            np_score = None
            cp_score = None
            if deduct_yoy is not None:
                np_score = percentile_to_score(deduct_yoy - deduct_industry_median, -50, 200, base=5)
            if cash_yoy is not None:
                cp_score = percentile_to_score(cash_yoy - cash_industry_median, -100, 200, base=5)

            if np_score is not None and cp_score is not None:
                pf = round(0.5 * np_score + 0.5 * cp_score, 2)
            elif np_score is not None:
                pf = np_score
            else:
                pf = cp_score

        # S 综合
        if ps is None or pf is None:
            S = None
        else:
            S = round(0.6 * ps + 0.4 * pf, 2)

        # 象限
        quadrant = None
        if ps is not None and pf is not None:
            if ps >= 6 and pf >= 6:
                quadrant = "Q1同行抢筹"
            elif ps >= 6 and pf < 6:
                quadrant = "Q2兑现期"
            elif ps < 6 and pf >= 6:
                quadrant = "Q3价值洼地"
            else:
                quadrant = "Q4潜伏"

        scored.append({
            "name": name,
            "code": code,
            "kline_12m_return_pct": ret12,
            "benchmark_12m_return_pct": benchmark_12m,
            "Ps_price_settlement": ps,
            "Pf_finance_settlement": pf,
            "S_composite": S,
            "quadrant": quadrant,
            "fund_flow_60d_yi": s.get("fund_flow_60d_yi"),
            "deduct_yoy_pct": sum12.get("deduct_yoy_pct"),
            "cashflow_yoy_pct": sum12.get("cashflow_yoy_pct"),
            "deduct_12m_yi": sum12.get("deduct_netprofit_yi"),
            "cash_12m_yi": sum12.get("operate_cashflow_yi"),
        })

    # 关注池分类(关注池只看 Q3 业绩兑现但股价还没跟上 = 最佳机会)
    pools = {
        "watch_focus": [],   # Q3 价值洼地(主要)
        "watch_caution": [], # Q1 同行抢筹(警惕追高)
        "watch_avoid": [],   # Q2 兑现期(规避)
        "watch_observe": [], # Q4 潜伏(观察)
    }
    for x in scored:
        if x["S_composite"] is None:
            continue
        q = x["quadrant"]
        if q == "Q3价值洼地":
            pools["watch_focus"].append(x)
        elif q == "Q1同行抢筹":
            pools["watch_caution"].append(x)
        elif q == "Q2兑现期":
            pools["watch_avoid"].append(x)
        elif q == "Q4潜伏":
            pools["watch_observe"].append(x)

    # 按 S 降序排
    for k in pools:
        pools[k].sort(key=lambda x: x.get("S_composite") or 0, reverse=True)

    # 兑现度反例
    backflow_signals = []
    for x in scored:
        if (x["fund_flow_60d_yi"] is not None
                and x["fund_flow_60d_yi"] > 1.0
                and x["kline_12m_return_pct"] is not None
                and x["kline_12m_return_pct"] < benchmark_12m
                and x["Pf_finance_settlement"] is not None
                and x["Pf_finance_settlement"] >= 6):
            backflow_signals.append({
                "name": x["name"],
                "code": x["code"],
                "signal": "资金显著流入但股价未涨,业绩已现 — 大兑现信号",
                "fund_flow_60d_yi": x["fund_flow_60d_yi"],
                "return_12m_pct": x["kline_12m_return_pct"],
                "Pf": x["Pf_finance_settlement"],
            })

    return {
        "meta": {
            "scored_at": datetime_now(),
            "benchmark_12m_return_pct": benchmark_12m,
            "weights": {"Ps_60": 0.6, "Pf_40": 0.4, "Pf_split_Np_50_Cp_50": True},
            "thresholds": {
                "Ps": {"Q1Q2": 6, "lo_clip": -50, "hi_clip": 100},
                "Pf": {"Q1Q3": 6, "lo_clip": -50, "hi_clip": 200},
                "S_focus_min": 8,
            },
        },
        "scored": scored,
        "pools": pools,
        "backflow_signals": backflow_signals,
    }


def datetime_now():
    from datetime import datetime
    return datetime.now().isoformat()


def main():
    if len(sys.argv) < 3:
        print("用法: calc_settlement_score.py <settlement_data.json> <settlement_scores.json>")
        sys.exit(1)

    inp = sys.argv[1]
    outp = sys.argv[2]

    data = json.loads(Path(inp).read_text(encoding="utf-8"))
    scores = calc_scores(data)
    Path(outp).write_text(json.dumps(scores, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"==> 评分完成 {len(scores['scored'])} 只,写入 {outp}")
    # 打印关注池
    print(f"\n--- 关注池 ({len(scores['pools']['watch_focus'])} 只) ---")
    for x in scores["pools"]["watch_focus"]:
        print(f"  {x['name']}({x['code']}) S={x['S_composite']} {x['quadrant']}")
    print(f"\n--- 规避池 ({len(scores['pools']['watch_avoid'])} 只) ---")
    for x in scores["pools"]["watch_avoid"]:
        print(f"  {x['name']}({x['code']}) S={x['S_composite']} {x['quadrant']}")
    print(f"\n--- 兑现度反例 ({len(scores['backflow_signals'])} 个) ---")
    for b in scores["backflow_signals"]:
        print(f"  {b['name']}({b['code']}) {b['signal']}")


if __name__ == "__main__":
    main()
