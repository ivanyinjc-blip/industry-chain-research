#!/usr/bin/env python3
"""
chain-radar 行业雷达评分算法 v2(2026-07-06 修正趋势定义)
=========================================================

输入:radar_raw.json
输出:radar_scores.json(每个行业的三轴评分 + 综合评级 + Top ETF)

评分体系:「景气 × 趋势 × 拥挤度」三角筛选
------------------------------------------------------
- 景气:12M 涨幅
  [-25%, +25%] → [0, 10];+25% 以上→10;-25% 以下→0
- 趋势:6M 涨幅(绝对值,不再用 6M/12M 比率)
  [-25%, +25%] → [0, 10];+25% 以上→10;-25% 以下→0
- 拥挤度反向:1M 涨幅(短期是否过热,绝对值)
  [0, +30%] → [10, 0];+30% 以上→0;-5% 以下→10(可能超跌反弹)

综合分:Radar = 景气 × 0.4 + 趋势 × 0.3 + 拥挤反向 × 0.3

设计理由(v2 修正):
- v1 用 6M/12M 比率,在 12M 为负时数值反向(医药 -2/-5.85 = 2.84 反而高),违反直觉
- v2 直接看绝对涨幅,语义清晰:"行业过去 6 个月涨多少"

评级:
  ★★★★★ radar ≥ 7.5 且 12M > 5%(强景气 + 强趋势 + 不拥挤)
  ★★★★  radar ≥ 6.5
  ★★★   radar ≥ 5.0
  ★★    radar < 5.0 或 12M < -10%(规避)
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from statistics import median


def clip(v, lo, hi):
    return max(lo, min(hi, v))


def linear_score(value, lo, hi):
    """线性映射到 0-10
    value 在 [lo, hi] 时,score 从 0 升到 10
    """
    if value >= hi:
        return 10.0
    if value <= lo:
        return 0.0
    return round((value - lo) / (hi - lo) * 10.0, 2)


def momentum_score(ret_12m):
    """12M 涨幅 → 景气分(0-10)
    -25% → 0,0% → 5,+25% → 10
    """
    return linear_score(ret_12m, lo=-25, hi=25)


def trend_score(ret_6m):
    """6M 涨幅 → 趋势分(0-10)
    -25% → 0,0% → 5,+25% → 10
    """
    if ret_6m is None:
        return 5.0
    return linear_score(ret_6m, lo=-25, hi=25)


def crowding_inv_score(ret_1m):
    """1M 涨幅 → 拥挤度反向分(0-10)
    短期涨幅越高 = 越拥挤 = 越低分
    短期跌越多 = 越冷 = 越高分(可能反弹)
    """
    if ret_1m is None:
        return 5.0
    # 短期 -10% 以下 → 10 分(超跌机会)
    # 短期 0% → 7 分(冷静)
    # 短期 +5% → 5 分
    # 短期 +10% → 3 分
    # 短期 +20% 以上 → 0 分(过热)
    if ret_1m <= -10:
        return 10.0
    if ret_1m >= 20:
        return 0.0
    # 分段:
    # [-10, 0] → [10, 7]
    # [0, +5] → [7, 5]
    # [+5, +10] → [5, 3]
    # [+10, +20] → [3, 0]
    if ret_1m < 0:
        return round(7 - ret_1m / 10 * 3, 2)  # -10→10, 0→7
    if ret_1m < 5:
        return round(7 - ret_1m / 5 * 2, 2)  # 0→7, 5→5
    if ret_1m < 10:
        return round(5 - (ret_1m - 5) / 5 * 2, 2)  # 5→5, 10→3
    return round(3 - (ret_1m - 10) / 10 * 3, 2)  # 10→3, 20→0


def rating_from_score(radar, ret_12m):
    """综合分 + 12M 涨幅 → 评级"""
    if ret_12m is None:
        return "无数据"
    if ret_12m < -10:
        return "★★ 规避"
    if radar >= 7.5 and ret_12m > 5:
        return "★★★★★ 强烈推荐"
    if radar >= 6.5:
        return "★★★★ 推荐"
    if radar >= 5.0:
        return "★★★ 中性"
    return "★★ 规避"


# 雷达重点行业
RADAR_FOCUS_SECTORS = {
    "AI", "半导体/科技", "机器人/智造", "新能源车", "光伏",
    "储能/碳中和", "医药生物", "军工", "消费", "金融",
    "地产基建", "周期资源", "TMT/传媒", "农业",
}


def calc_scores(radar_raw, etf_count_threshold=3):
    etfs = radar_raw["etfs"]
    sector_etfs = defaultdict(list)
    for e in etfs:
        sector_etfs[e["sector"]].append(e)

    # 隐含大盘基准:全部 ETF 12M 涨幅中位数
    all_12m = [e["ret_12m_pct"] for e in etfs if e["ret_12m_pct"] is not None]
    benchmark_12m = round(median(all_12m), 2)

    sectors = []
    for sector, items in sector_etfs.items():
        if len(items) < etf_count_threshold:
            continue
        if sector not in RADAR_FOCUS_SECTORS:
            continue

        rets_12m = [e["ret_12m_pct"] for e in items if e["ret_12m_pct"] is not None]
        rets_6m = [e["ret_6m_pct"] for e in items if e["ret_6m_pct"] is not None]
        rets_3m = [e["ret_3m_pct"] for e in items if e["ret_3m_pct"] is not None]
        rets_1m = [e["ret_1m_pct"] for e in items if e["ret_1m_pct"] is not None]

        if not rets_12m:
            continue

        med_12m = round(median(rets_12m), 2)
        med_6m = round(median(rets_6m), 2) if rets_6m else None
        med_3m = round(median(rets_3m), 2) if rets_3m else None
        med_1m = round(median(rets_1m), 2) if rets_1m else None

        # 三轴评分
        mom = momentum_score(med_12m)
        trend = trend_score(med_6m)
        crowd_inv = crowding_inv_score(med_1m)

        radar = round(0.4 * mom + 0.3 * trend + 0.3 * crowd_inv, 2)
        rating = rating_from_score(radar, med_12m)

        # Top 3 ETF(按 12M 涨幅)
        top_etfs = sorted(items, key=lambda e: e["ret_12m_pct"] or -999, reverse=True)[:3]
        top_etf_summaries = [{
            "ts_code": e["ts_code"],
            "name": e["name"],
            "ret_12m_pct": e["ret_12m_pct"],
        } for e in top_etfs]

        sectors.append({
            "sector": sector,
            "etf_count": len(items),
            "median_1m_pct": med_1m,
            "median_3m_pct": med_3m,
            "median_6m_pct": med_6m,
            "median_12m_pct": med_12m,
            "excess_vs_benchmark_pp": round(med_12m - benchmark_12m, 2),
            "score_momentum": mom,
            "score_trend": trend,
            "score_crowd_inv": crowd_inv,
            "score_radar": radar,
            "rating": rating,
            "top_etfs": top_etf_summaries,
        })

    sectors.sort(key=lambda x: x["score_radar"], reverse=True)

    buckets = {
        "strong_buy": [],
        "buy": [],
        "neutral": [],
        "avoid": [],
    }
    for s in sectors:
        if "★★★★★" in s["rating"]:
            buckets["strong_buy"].append(s)
        elif "★★★★" in s["rating"]:
            buckets["buy"].append(s)
        elif "★★★" in s["rating"]:
            buckets["neutral"].append(s)
        else:
            buckets["avoid"].append(s)

    return {
        "meta": {
            "scored_at": datetime.now().isoformat(),
            "benchmark_12m_pct_median": benchmark_12m,
            "benchmark_note": "隐含大盘基准 = 全部 ETF 12M 涨幅中位数",
            "weights": {"momentum": 0.4, "trend": 0.3, "crowd_inv": 0.3},
            "scoring_rules": {
                "momentum": "12M 涨幅,[-25%, +25%] → [0, 10]",
                "trend": "6M 涨幅,[-25%, +25%] → [0, 10](v2 改:不再用比率)",
                "crowd_inv": "1M 涨幅反向,≤-10%→10(超跌),≥+20%→0(过热)",
            },
            "etf_count_threshold": etf_count_threshold,
            "radar_focus_sectors": sorted(RADAR_FOCUS_SECTORS),
        },
        "sectors": sectors,
        "buckets": buckets,
        "all_sector_count": len(sectors),
        "strong_buy_count": len(buckets["strong_buy"]),
        "buy_count": len(buckets["buy"]),
    }


def main():
    if len(sys.argv) < 3:
        print("用法: calc_radar_score.py <radar_raw.json> <radar_scores.json>")
        sys.exit(1)
    inp = sys.argv[1]
    outp = sys.argv[2]
    raw = json.loads(Path(inp).read_text(encoding="utf-8"))
    scores = calc_scores(raw)
    Path(outp).write_text(json.dumps(scores, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"==> 评分完成 {len(scores['sectors'])} 个行业")
    print(f"   强烈推荐: {scores['strong_buy_count']} 个")
    print(f"   推荐: {scores['buy_count']} 个")
    print(f"\n--- Top 5 行业 ---")
    for s in scores["sectors"][:5]:
        print(f"  {s['sector']:10s} 雷达分={s['score_radar']:5.2f}  "
              f"12M={s['median_12m_pct']:+6.2f}%  6M={s['median_6m_pct']:+6.2f}%  "
              f"1M={s['median_1m_pct']:+6.2f}%  评级={s['rating']}")


if __name__ == "__main__":
    main()
