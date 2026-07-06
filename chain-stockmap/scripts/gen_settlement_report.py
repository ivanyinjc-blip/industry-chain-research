#!/usr/bin/env python3
"""
chain-settlement 报告生成器
================================

输入:settlement_scores.json + stockmap.md
输出:settlement.md(完整兑现度筛选报告)

报告结构(对应 v4 P0 段产物):
0. 一句话结论
1. 兑现度评分卡(全股票)
2. 4 象限分类 + 关注池
3. 关注池 vs 规避池
4. 兑现度反例(资金信号)
5. 跟踪指标(月度更新)
"""

import sys
import json
from datetime import datetime
from pathlib import Path


def render_table(rows, headers):
    """渲染 Markdown 表格"""
    out = "| " + " | ".join(headers) + " |\n"
    out += "| " + " | ".join(["---"] * len(headers)) + " |\n"
    for r in rows:
        out += "| " + " | ".join(str(c) if c is not None else "—" for c in r) + " |\n"
    return out


def render_settlement_md(scores, stockmap_path=None, case_name="产业链"):
    """主入口:生成 settlement.md"""
    out = []
    out.append(f"# {case_name} · 兑现度筛选报告")
    out.append("")
    out.append(f"> 生成时间:{scores['meta']['scored_at']}")
    out.append(f"> 输入 stockmap:{stockmap_path or '(未提供)'}")
    out.append(f"> 权重:Ps=0.6 · Pf=0.4(扣非 50% + 现金流 50%)")
    out.append(f"> 时间窗口:12M 滚动")
    out.append("")

    # 0. 一句话结论
    focus = scores["pools"]["watch_focus"]
    caution = scores["pools"].get("watch_caution", [])
    avoid = scores["pools"]["watch_avoid"]
    observe = scores["pools"]["watch_observe"]
    backflow = scores["backflow_signals"]
    out.append("## 0. 一句话结论")
    out.append("")
    if focus:
        names = "、".join(s["name"] for s in focus[:3])
        out.append(f"**关注池({len(focus)} 只 · 业绩兑现但股价未涨 = 最佳机会)**:{names}")
    if caution:
        names = "、".join(s["name"] for s in caution[:3])
        out.append(f"**警惕池({len(caution)} 只 · 同行抢筹已充分兑现 = 谨慎追高)**:{names}")
    if avoid:
        names = "、".join(s["name"] for s in avoid[:3])
        out.append(f"**规避池({len(avoid)} 只)**:{names}")
    out.append(f"**兑现度反例({len(backflow)} 个)**:资金已埋伏但股价未动的强信号标的")
    out.append("")

    # 1. 评分卡
    out.append("## 1. 兑现度评分卡")
    out.append("")
    out.append("> 综合分 S = 0.6 × Ps(股价兑现) + 0.4 × Pf(业绩兑现)")
    out.append("> Ps/Pf 中位数为 5 分,7+ 算高兑现,3- 算低兑现")
    out.append("")
    rows = []
    for s in scores["scored"]:
        rows.append([
            s["name"],
            s["code"],
            f"{s['kline_12m_return_pct']:.1f}%" if s.get("kline_12m_return_pct") is not None else "—",
            f"{scores['meta']['benchmark_12m_return_pct']:.1f}%",
            s["Ps_price_settlement"] if s["Ps_price_settlement"] is not None else "—",
            s["Pf_finance_settlement"] if s["Pf_finance_settlement"] is not None else "—",
            s["S_composite"] if s["S_composite"] is not None else "—",
            s["quadrant"] or "—",
            f"{s['fund_flow_60d_yi']:.2f} 亿" if s.get("fund_flow_60d_yi") is not None else "—",
        ])
    out.append(render_table(rows, [
        "公司", "代码", "12M 涨幅", "行业基准",
        "Ps(股价)", "Pf(业绩)", "S(综合)", "象限", "60 日主力净流入",
    ]))
    out.append("")

    # 2. 4 象限分类
    out.append("## 2. 兑现度 4 象限")
    out.append("")
    out.append("| 象限 | 处理 | 含义 |")
    out.append("|---|---|---|")
    out.append("| **Q1 同行抢筹** | ⚠️ 谨慎追高 | Ps高 + Pf高 = 业绩兑现 + 股价兑现 |")
    out.append("| **Q2 兑现期 / 终结期** | ❌ 规避 | Ps高 + Pf低 = 股价兑现但业绩未跟上 = 终结信号 |")
    out.append("| **Q3 价值洼地** | ✅ **关注池** | Ps低 + Pf高 = 业绩已兑现但股价未动 = 最佳机会 |")
    out.append("| **Q4 潜伏 / 没起来** | 🔍 观察池 | Ps低 + Pf低 = 业绩未兑现但市场也未抢筹 |")
    out.append("")

    # 3. 关注池
    out.append("## 3. 关注池(已按 S 降序)")
    out.append("")
    if focus:
        rows = [[
            i + 1,
            s["name"],
            s["code"],
            s["S_composite"],
            s["Ps_price_settlement"],
            s["Pf_finance_settlement"],
            s["kline_12m_return_pct"],
            s["quadrant"],
        ] for i, s in enumerate(focus)]
        out.append(render_table(rows, [
            "#", "公司", "代码", "S", "Ps", "Pf", "12M 涨幅", "象限",
        ]))
    else:
        out.append("**无关注池标的**(全部标的都已兑现或没起来)")
    out.append("")

    # 3.2 警惕池(Q1 同行抢筹已充分兑现)
    out.append("## 3.2 警惕池(Q1 同行抢筹,谨慎追高)")
    out.append("")
    if caution:
        rows = [[
            s["name"], s["code"], s["S_composite"], s["Ps_price_settlement"],
            s["Pf_finance_settlement"], s["kline_12m_return_pct"], s["quadrant"],
        ] for s in caution]
        out.append(render_table(rows, [
            "公司", "代码", "S", "Ps", "Pf", "12M 涨幅", "象限",
        ]))
    else:
        out.append("无警惕标的")
    out.append("")

    # 3.3 规避池
    out.append("## 3.3 规避池")
    out.append("")
    if avoid:
        rows = [[
            s["name"], s["code"], s["S_composite"], s["Ps_price_settlement"],
            s["Pf_finance_settlement"], s["kline_12m_return_pct"], s["quadrant"],
        ] for s in avoid]
        out.append(render_table(rows, [
            "公司", "代码", "S", "Ps", "Pf", "12M 涨幅", "象限",
        ]))
    else:
        out.append("无规避标的")
    out.append("")

    # 3.4 观察池
    out.append("## 3.4 观察池(潜伏 / 待跟进)")
    out.append("")
    if observe:
        rows = [[
            s["name"], s["code"], s["S_composite"], s["quadrant"],
        ] for s in observe]
        out.append(render_table(rows, ["公司", "代码", "S", "象限"]))
    else:
        out.append("无观察标的")
    out.append("")

    # 4. 兑现度反例
    out.append("## 4. 兑现度反例(资金信号)")
    out.append("")
    out.append("> 资金显著净流入 + 12M 涨幅 < 行业基准 + Pf 业绩兑现 → 可能有大兑现未发生,强信号关注")
    out.append("")
    if backflow:
        rows = [[
            b["name"], b["code"],
            f"{b['fund_flow_60d_yi']:.2f} 亿",
            f"{b['return_12m_pct']:.1f}%",
            b["Pf"],
            b["signal"],
        ] for b in backflow]
        out.append(render_table(rows, [
            "公司", "代码", "60 日净流入", "12M 涨幅", "Pf", "信号",
        ]))
    else:
        out.append("无明显资金埋伏信号")
    out.append("")

    # 5. 跟踪指标
    out.append("## 5. 跟踪指标(月度更新)")
    out.append("")
    out.append("| 公司 | 当前象限 | 跟踪要点 | 升级条件 | 降级条件 |")
    out.append("|---|---|---|---|---|")
    for s in scores["scored"]:
        q = s["quadrant"] or "—"
        if q == "Q3价值洼地":
            upgrade = "股价补涨 → 升级到 Q1"
            downgrade = "业绩转负 → 降级到 Q4"
            track = "资金流入 + 价格突破"
        elif q == "Q1同行抢筹":
            upgrade = "—(已充分兑现)"
            downgrade = "业绩跟不上 → Q2(规避)"
            track = "估值是否仍合理"
        elif q == "Q2兑现期":
            upgrade = "—"
            downgrade = "—(已规避)"
            track = "信号反转(业绩兑现 → 重新评估)"
        elif q == "Q4潜伏":
            upgrade = "业绩兑现 → Q3(关注)"
            downgrade = "基本面恶化 → 移除观察"
            track = "基本面拐点"
        else:
            upgrade = "—"
            downgrade = "—"
            track = "—"
        out.append(f"| {s['name']}({s['code']}) | {q} | {track} | {upgrade} | {downgrade} |")
    out.append("")

    # 6. 数据来源 + 不确定性
    out.append("## 6. 数据来源 + 不确定性")
    out.append("")
    out.append("**数据源**:")
    out.append("- K 线:东方财富 push2his.eastmoney.com")
    out.append("- 季报:AKShare stock_profit_sheet + cash_flow(东财底表)")
    out.append("- 行业基准 ETF:Tushare DuckDB(本地数据,local_api.py)")
    out.append("- 资金流:东财 60 日主力净流入")
    out.append("")
    out.append("**不确定性**:")
    out.append("- 业绩增速对比使用最近 4 季度 vs 去年同期 4 季度(滚动 12M)")
    out.append("- 行业 ETF 取中位数作为基准,可能受少数极端值影响")
    out.append("- 资金流「主力净流入」含融资盘,不区分内/外资")
    out.append("")
    out.append("**对齐验收清单**:")
    out.append("- [ ] Ps/Pf 评分算法与文字说明一致")
    out.append("- [ ] 4 象限逻辑与表头定义一致")
    out.append("- [ ] 关注池 vs stockmap 原 P0/P1/P2 评级对比说明")
    out.append("")

    return "\n".join(out)


def main():
    if len(sys.argv) < 3:
        print("用法: gen_settlement_report.py <settlement_scores.json> <settlement.md> [stockmap.md] [case_name]")
        sys.exit(1)

    scores_path = sys.argv[1]
    out_path = sys.argv[2]
    stockmap_path = sys.argv[3] if len(sys.argv) > 3 else None
    case_name = sys.argv[4] if len(sys.argv) > 4 else "产业链"

    scores = json.loads(Path(scores_path).read_text(encoding="utf-8"))
    md = render_settlement_md(scores, stockmap_path, case_name)
    Path(out_path).write_text(md, encoding="utf-8")
    print(f"==> 报告写入 {out_path}({len(md)} 字符)")


if __name__ == "__main__":
    main()
