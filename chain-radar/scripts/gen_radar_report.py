#!/usr/bin/env python3
"""
chain-radar 报告生成器
======================

输入:radar_scores.json
输出:radar.md(行业雷达筛选报告)

报告结构:
0. 一句话结论(Top 3 行业建议)
1. 雷达评分卡(全行业)
2. 三轴定义 + 权重
3. 强烈推荐行业(详细)
4. 推荐行业(详细)
5. 中性 + 规避(列表)
6. 雷达选股建议(对接到 chain-idea)
7. 数据来源 + 不确定性
"""

import sys
import json
from pathlib import Path


def render_table(rows, headers):
    out = "| " + " | ".join(headers) + " |\n"
    out += "| " + " | ".join(["---"] * len(headers)) + " |\n"
    for r in rows:
        out += "| " + " | ".join(str(c) if c is not None else "—" for c in r) + " |\n"
    return out


def render_radar_md(scores):
    out = []
    out.append("# 行业雷达扫描报告")
    out.append("")
    out.append(f"> 扫描时间:{scores['meta']['scored_at']}")
    out.append(f"> 样本:1,561 只被动指数型 ETF(覆盖 14 个重点行业)")
    out.append(f"> 隐含大盘基准(全部 ETF 12M 涨幅中位数):{scores['meta']['benchmark_12m_pct_median']}%")
    out.append(f"> 权重:景气 40% · 趋势 30% · 拥挤反向 30%")
    out.append("")

    # 0. 一句话结论
    sb = scores["buckets"]["strong_buy"]
    b = scores["buckets"]["buy"]
    n = scores["buckets"]["neutral"]
    a = scores["buckets"]["avoid"]

    out.append("## 0. 一句话结论")
    out.append("")
    if sb:
        names = "、".join(s["sector"] for s in sb[:3])
        out.append(f"**强烈推荐研究({len(sb)} 个)**:{names}")
    if b:
        names = "、".join(s["sector"] for s in b[:3])
        out.append(f"**推荐研究({len(b)} 个)**:{names}")
    out.append(f"**中性 / 规避({len(n) + len(a)} 个)**:暂不主动研究,仅在 P0 受益于上下游时跟进")
    out.append("")

    # 1. 雷达评分卡
    out.append("## 1. 行业雷达评分卡")
    out.append("")
    out.append("> 综合分 = 0.4 × 景气 + 0.3 × 趋势 + 0.3 × 拥挤反向")
    out.append("")
    rows = []
    for s in scores["sectors"]:
        rows.append([
            s["sector"],
            s["etf_count"],
            f"{s['median_12m_pct']:+.1f}%",
            f"{s['median_6m_pct']:+.1f}%",
            f"{s['median_3m_pct']:+.1f}%",
            f"{s['median_1m_pct']:+.1f}%",
            f"{s['excess_vs_benchmark_pp']:+.1f}",
            s["score_momentum"],
            s["score_trend"],
            s["score_crowd_inv"],
            s["score_radar"],
            s["rating"],
        ])
    out.append(render_table(rows, [
        "行业", "ETF 数", "12M", "6M", "3M", "1M",
        "超额(pp)", "景气", "趋势", "拥挤反", "雷达分", "评级",
    ]))
    out.append("")

    # 2. 三轴定义
    out.append("## 2. 三轴定义 + 权重")
    out.append("")
    out.append("| 轴 | 定义 | 评分区间 | 含义 |")
    out.append("|---|---|---|---|")
    out.append("| **景气** | 12M 涨幅 | [-25%, +25%] → [0, 10] | 行业过去一年的整体表现 |")
    out.append("| **趋势** | 6M 涨幅 | [-25%, +25%] → [0, 10] | 行业近期半年趋势(不再用比率) |")
    out.append("| **拥挤反向** | 1M 涨幅反向 | ≤-10% → 10 分(超跌), ≥+20% → 0 分(过热) | 短期是否已被充分交易 |")
    out.append("")
    out.append("**评级映射**:")
    out.append("- ★★★★★ 雷达分 ≥ 7.5 且 12M > 5%(强景气 + 趋势 + 短期有空间)")
    out.append("- ★★★★ 雷达分 ≥ 6.5")
    out.append("- ★★★ 雷达分 ≥ 5.0")
    out.append("- ★★ 雷达分 < 5.0 或 12M < -10%(规避)")
    out.append("")

    # 3. 强烈推荐
    out.append("## 3. 强烈推荐行业(★★★★★)")
    out.append("")
    if sb:
        for s in sb:
            out.append(f"### 3.{sb.index(s) + 1} {s['sector']} · 雷达分 {s['score_radar']}")
            out.append("")
            out.append(f"- **12M 涨幅**:{s['median_12m_pct']:+.2f}% (超额 {s['excess_vs_benchmark_pp']:+.2f}pp)")
            out.append(f"- **6M / 3M / 1M**:{s['median_6m_pct']:+.2f}% / {s['median_3m_pct']:+.2f}% / {s['median_1m_pct']:+.2f}%")
            out.append(f"- **三轴分**:景气 {s['score_momentum']} · 趋势 {s['score_trend']} · 拥挤反向 {s['score_crowd_inv']}")
            out.append(f"- **代表 ETF**({s['etf_count']} 只中选 12M 涨幅 Top 3):")
            for etf in s["top_etfs"]:
                out.append(f"  - {etf['name']}({etf['ts_code']}) · 12M {etf['ret_12m_pct']:+.2f}%")
            out.append("")
            # 给行业一个研究方向的提示
            research_hint = {
                "AI":              "算力 / 模型 / 应用三层,关注国产 GPU / 推理芯片 / AI Agent / 端侧 AI",
                "机器人/智造":      "减速器 / 丝杠 / 伺服 / 传感器,关注国产替代 + 商业化兑现",
                "储能/碳中和":      "大储 / 工商业储能 / 户储 + 逆变器 + 电池",
                "光伏":            "钙钛矿 / 0BB / 银包铜 / 贱金属 + 辅材辅料",
                "半导体/科技":      "国产替代(设备 / 材料 / EDA)+ 先进封装 + 存储",
            }.get(s["sector"], "需进一步细分")
            out.append(f"- **研究方向提示**:{research_hint}")
            out.append("")
    else:
        out.append("无强烈推荐行业")
        out.append("")

    # 4. 推荐
    out.append("## 4. 推荐行业(★★★★)")
    out.append("")
    if b:
        for s in b:
            out.append(f"### 4.{b.index(s) + 1} {s['sector']} · 雷达分 {s['score_radar']}")
            out.append("")
            out.append(f"- **12M 涨幅**:{s['median_12m_pct']:+.2f}% (超额 {s['excess_vs_benchmark_pp']:+.2f}pp)")
            out.append(f"- **6M / 3M / 1M**:{s['median_6m_pct']:+.2f}% / {s['median_3m_pct']:+.2f}% / {s['median_1m_pct']:+.2f}%")
            out.append(f"- **代表 ETF**({s['etf_count']} 只中选 12M 涨幅 Top 3):")
            for etf in s["top_etfs"]:
                out.append(f"  - {etf['name']}({etf['ts_code']}) · 12M {etf['ret_12m_pct']:+.2f}%")
            out.append("")
    else:
        out.append("无推荐行业")
        out.append("")

    # 5. 中性 / 规避
    out.append("## 5. 中性 + 规避行业(★★ / ★★★)")
    out.append("")
    rows = []
    for s in n + a:
        rows.append([
            s["sector"], s["rating"],
            f"{s['median_12m_pct']:+.1f}%",
            f"{s['median_1m_pct']:+.1f}%",
            s["score_radar"],
        ])
    out.append(render_table(rows, [
        "行业", "评级", "12M", "1M", "雷达分",
    ]))
    out.append("")
    out.append("**规避行业 ≠ 不研究**:如医药 / 消费虽是规避评级,但若用户提出具体研究问题(政策催化 / 出海 / 新技术),仍可进入 chain-idea 立项")
    out.append("")

    # 6. 雷达 → chain-idea 接入
    out.append("## 6. 雷达选股 → chain-idea 接入")
    out.append("")
    out.append("**用法**:")
    out.append("1. 用户问「研究哪个行业最有价值」,跑本雷达")
    out.append("2. 雷达给出 ★★★★ 及以上行业清单")
    out.append("3. 选定 Top 1-2 行业,进入 `chain-idea`(立项 + 口径)")
    out.append("4. 完成 7 段后,在 `chain-stockmap` 阶段再叠加 `chain-settlement` 做兑现度筛选")
    out.append("")
    out.append("**核心建议(本次扫描结果)**:")
    out.append("")
    out.append("> 优先研究: **AI(★★★) / 机器人 / 智能制造(★★★)**")
    out.append("> - 共同特征:12M 涨幅 +44% 左右 + 6M 仍加速 +30% + 1M 仅 +6-9%(未过热)")
    out.append("> - 研究路径:chain-idea → chain-data → chain-breakdown → chain-cycle(若是产能周期) → chain-analysis → chain-report → chain-stockmap → chain-settlement")
    out.append("")
    out.append("> 次优研究: **光伏 / 储能 / 碳中和(★★★)**")
    out.append("> - 共同特征:12M 强景气但 1M 已超跌(可能反弹拐点)")
    out.append("> - 适合研究产业链拐点 + 周期触发条件")
    out.append("")
    out.append("> 可选研究: **新能源车 / 周期资源 / 军工(★★)**")
    out.append("> - 涨幅中等,需配合个股选择")
    out.append("")

    # 7. 数据来源 + 不确定性
    out.append("## 7. 数据来源 + 不确定性")
    out.append("")
    out.append("**数据源**:")
    out.append("- ETF 基础信息:Tushare DuckDB `fund_basic`(本地,1,561 只 L 状态被动指数型 ETF)")
    out.append("- ETF 日线:Tushare DuckDB `fund_daily`(本地,250 个交易日窗口)")
    out.append("- 行业分类:基于 ETF 名称 + 跟踪指数(benchmark)的关键词匹配")
    out.append("")
    out.append("**不确定性**:")
    out.append("- 行业分类用关键词规则,长尾主题 ETF 归到「其它主题」不进入雷达")
    out.append("- 隐含大盘基准 = 全部 ETF 12M 中位数,这是代理变量;严格应取沪深 300 全收益")
    out.append("- ETF 跟踪误差 + 申赎溢价可能导致行业涨幅与真实行业有偏差")
    out.append("- 6M/1M 短期窗口受市场情绪影响大,雷达分波动性高")
    out.append("")
    out.append("**对齐验收清单**:")
    out.append("- [ ] 三轴评分与文字说明一致")
    out.append("- [ ] 行业评级与雷达分阈值一致")
    out.append("- [ ] 强烈推荐行业的代表 ETF 可在 Tushare 校验到")
    out.append("- [ ] 雷达结果与人工扫读市场主线一致(本次为 AI + 机器人)")
    out.append("")

    return "\n".join(out)


def main():
    if len(sys.argv) < 3:
        print("用法: gen_radar_report.py <radar_scores.json> <radar.md>")
        sys.exit(1)
    scores_path = sys.argv[1]
    out_path = sys.argv[2]
    scores = json.loads(Path(scores_path).read_text(encoding="utf-8"))
    md = render_radar_md(scores)
    Path(out_path).write_text(md, encoding="utf-8")
    print(f"==> 报告写入 {out_path}({len(md)} 字符)")


if __name__ == "__main__":
    main()
