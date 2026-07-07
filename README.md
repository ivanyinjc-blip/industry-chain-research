# Industry Chain Research Skill

> **v4.1** · 9 段对齐流水线 · 面向 A 股 / 港股 / 美股的产业链深度投研 skill
> 升级时间:2026-07-06 · 在 8+1 之前加入 **chain-radar(行业雷达)**第 0 段
> 适配场景:Claude Code / OpenAI Codex CLI 等 agent CLI

---

## 🎯 这个 Skill 解决什么

产业链研究的 6 个常见痛点,以及本 skill 的解法:

| 痛点 | 现状 | 本 skill 解法 |
|---|---|---|
| 想法飘忽 | "研究一下 AI 芯片" → 没有边界 | chain-idea 口径拆分 + 三问法 |
| 数据散乱 | 微信群/研报/招股书各说各话 | chain-data 三端拆解 + 11 词 + 数据状态 |
| 环节说不清 | 上中下游概念混淆 | chain-breakdown 三类缺口 + 周期位置 |
| 缺周期判断 | 不区分周期顶部 / 底部 | **chain-cycle(强周期行业必跑)** |
| 缺反证 | 单向看好,缺乏证伪 | chain-verify + 全程反证前置 |
| 结论不稳定 | 同样的研究换个时间出不同结论 | **「周期 × 缺口 × 政策」三角定位法** |
| **不知道研究哪个行业**(v4.1) | 用户上来就"研究点啥好" | **chain-radar 三轴评分扫 1,561 只 ETF** |
| **选出 10 只但不知哪只已兑现**(v4.0) | stockmap 全给"看多",无兑现度区分 | **chain-settlement 4 象限分类** |

---

## 📐 9 段对齐架构(v4.1)

```
     ┌──────────────────┐
     │  chain-radar     │ 0 行业雷达:从 1,561 只 ETF 筛出 Top 行业
     │  (v4.1 新增)     │   「景气 × 趋势 × 拥挤度」三轴评分
     └──────┬───────────┘
            ▼
     ┌─────────────────┐
     │  chain-idea     │ ① 待研究问题 + 口径 + 周期/政策前置
     └──────┬──────────┘
            ▼
     ┌──────────────────┐
     │  chain-data      │ ② 上中下游 + 三端 + 周期性数据
     └──────┬───────────┘
            ▼
     ┌────────────────────┐
     │ chain-chip-design  │ ②.5 工艺路线 + 衬底设备 + 良率爬升(可选)
     │ (半导体/光芯片必跑) │ ★ 产业链图生成
     └──────┬─────────────┘
            ▼
     ┌────────────────────┐
     │ chain-breakdown    │ ③ 4 维评分 + 三类缺口 + 周期位置
     └──────┬─────────────┘
            ▼
     ┌────────────────────┐
     │ chain-cycle        │ ④ 周期类型 + 周期阶段 + 拐点预测(可选)
     │ (强周期行业必跑)    │
     └──────┬─────────────┘
            ▼
     ┌──────────────────────┐
     │ chain-analysis       │ ⑤ 三层价值量 + 微笑曲线 + 利润转移 + 周期影响
     └──────┬───────────────┘
            ▼
     ┌──────────────────────┐
     │ chain-report         │ ⑥ 研报骨架 + 数据状态分层
     └──────┬───────────────┘
            ▼
     ┌──────────────────────┐
     │ chain-settlement     │ ⑦ P0 兑现度筛选(4 象限分类)
     │ (v4.0 新增)          │
     └──────┬───────────────┘
            ▼
     ┌──────────────────────┐
     │ chain-stockmap       │ ⑧ 价值量 × 财务 × 估值 × 技术 × 周期 → 选股清单
     └──────────────────────┘

     每段输出后,chain-verify 做反证 + 核销 + 周期触发矩阵
```

**可选段**:chain-chip-design 半导体/光芯片必跑;chain-cycle 强周期行业必跑(农业/化工/钢铁/煤炭/航运/半导体)。

---

## 🧩 9 个核心模块

| # | 模块 | 产物 | 输入 | 核心方法论 | 必跑 |
|---|---|---|---|---|---|
| 0 | **总纲** `SKILL.md` | 调度指令 | 用户提问 | 哪一段被激活 | - |
| 0.5 | **chain-radar** (v4.1) | `radar.md` | 用户问"研究哪个行业" | ETF 三轴扫描(景气 40% / 趋势 30% / 拥挤反向 30%) | ⚠️ 仅"选赛道"时跑 |
| 1 | **chain-idea** | `idea.md` | 用户模糊问题 | 三问法 + 口径拆分 + 周期/政策前置 | ✅ |
| 2 | **chain-data** | `data.md` | idea.md | 上中下游 + 材料/设备/工艺三端 | ✅ |
| 2.5 | **chain-chip-design**(可选) | chip-design.md + 产业链图 HTML | data.md | device physics 工艺路线 + 良率爬升 + mermaid 图 | ⚠️ 半导体/光芯片 |
| 3 | **chain-breakdown** | `breakdown.md` | data.md | 4 维评分 + 三类缺口 + 周期位置 | ✅ |
| 4 | **chain-cycle**(可选) | `cycle.md` | breakdown.md | 6 类周期指标 + 拐点预测 | ⚠️ 强周期 |
| 5 | **chain-analysis** | `analysis.md` | breakdown + cycle | 三层价值量 + 微笑曲线 + 利润转移 | ✅ |
| 6 | **chain-report** | `report.md` | analysis.md | 5 段叙事 + 11 词强制覆盖 + 数据状态分层 | ✅ |
| 6.5 | **chain-settlement**(P0) | `settlement.md` | stockmap 候选清单 | S = 0.6×Ps + 0.4×Pf,4 象限分类 | ✅(stockmap 前) |
| 7 | **chain-verify** | `verify.md` | report.md | 5 类核销 + 周期触发矩阵 | ✅ |
| 8 | **chain-stockmap** | `stockmap.md` | report + settlement | 价值量 × 财务 × 估值 × 技术 × 周期 | ✅ |

---

## 🌟 差异化方法论:「周期 × 缺口 × 政策」三角定位法

传统产业链研究:产业链 → 环节 → 公司(单维线性)

本 skill 升级版:**产业链 → 周期定位 × 缺口识别 × 政策环境 → 公司(三维交叉)**

### 16 种组合矩阵评级表

| 周期位置 | 缺口类型 | 政策环境 | 评级 | 典型案例 |
|---|---|---|---|---|
| 底部 | 国产替代 | 支持 | **★★★★★ 最佳** | 猪肉种猪育种 |
| 底部 | 增量 | 中性 | ★★★★ 良好 | - |
| 底部 | 瓶颈 | 支持 | ★★★★ 良好 | - |
| 上升 | 国产替代 | 支持 | ★★★★ 良好 | 氟化工电子 HF |
| 上升 | 新需求 | 支持 | ★★★★ 良好 | 氟化工 PVDF |
| 上升 | 增量 | 中性 | ★★★ 中等 | - |
| 顶部 | 任何 | 任何 | **★★ 规避** | - |
| 下降 | 任何 | 任何 | **★★ 规避** | - |
| ... 其余 8 种组合 | | | ★★★ 中等 | |

### chain-radar 三轴评分(v4.1)

| 轴 | 定义 | 评分区间 | 含义 |
|---|---|---|---|
| **景气** | 12M 涨幅 | [-25%, +25%] → [0, 10] | 行业过去一年整体表现 |
| **趋势** | 6M 涨幅(绝对值) | [-25%, +25%] → [0, 10] | 行业近期半年趋势 |
| **拥挤反向** | 1M 涨幅反向 | ≤-10% → 10 分(超跌),≥+20% → 0 分(过热) | 短期是否已被充分交易 |

**综合公式**:`R = 0.4 × 景气 + 0.3 × 趋势 + 0.3 × 拥挤反向`

### chain-settlement 4 象限分类(v4.0)

| 象限 | 含义 | 处理 |
|---|---|---|
| **Q1 同行抢筹** | Ps ≥ 6 + Pf ≥ 6 | ⚠️ 警惕追高 |
| **Q2 兑现期** | Ps ≥ 6 + Pf < 6 | ❌ 规避 |
| **Q3 价值洼地** ★ | Ps < 6 + Pf ≥ 6 | ✅ **关注池** |
| **Q4 潜伏** | Ps < 6 + Pf < 6 | 🔍 观察池 |

---

## 🚀 快速开始

### 安装

```bash
# 作为 Claude skill 放在 ~/.claude/skills/industry-chain-research
# 或作为 Codex skill 放在 ~/.codex/skills/industry-chain-research
cp -r industry-chain-research ~/.claude/skills/
```

### 用法

```text
# 1) 不知道研究哪个行业
> 跑一下 chain-radar
→ 出 radar.md,挑 Top 1-2 行业

# 2) 已知要研究哪个行业
> 用 industry-chain-research 跑 AI 产业链 9 段
→ 出 idea.md → data.md → breakdown.md → analysis.md
   → report.md → settlement.md → stockmap.md
   → verify.md(全程反证核销)

# 3) 强周期行业
> 用 industry-chain-research 跑猪肉 9 段
→ 强制加跑 chain-cycle 段
```

### 已跑通的实战案例

| 案例 | 雷达分 | 关注池 Q3 | 样本路径 |
|---|---|---|---|
| 光伏 v4.1 | 8.71(第 1) | 爱旭股份 + 大全能源 | `chain-radar/examples/radar-2026-07-06/` |
| AI v4.1 | 8.30(第 2) | (待补) | `examples/ai-hbm-chain/` |
| 机器人 v4.0 | 7.96 | 鸣志电器 + 汇川技术 | `chain-stockmap/examples/robot-case/` |
| 氟化工 v1 | - | - | `examples/fluorine-case/` |
| 猪肉 v2(强周期) | - | - | `examples/pig-case/` |
| 创新药 v2(政策 + 出海) | - | - | `examples/innovative-drug-case/` |

---

## 🛠 技术栈与依赖

| 数据源 | 用途 | 访问方式 |
|---|---|---|
| **Tushare DuckDB** | ETF 基础信息 + 日线 + 财务 | **只读**(`duckdb.connect(DB_PATH, read_only=True)`) |
| **AKShare** | 季度利润表/现金流量表 | `stock_profit_sheet_by_quarterly_em` |
| **东方财富 push2his** | K 线 + 60 日主力净流入 | HTTPS 直接调,带 retry |
| **腾讯/新浪 API** | A 股/港股/美股实时行情 | `fetch_a_stock.py` / `fetch_hk_stock.py` / `fetch_us_stock.py` |

依赖:`httpx`、`pandas`、`akshare`、`duckdb`(Tushare 自带)

每个 segment 的 `scripts/requirements.txt` 列出细分依赖。

---

## 🔒 数据访问约束(2026-07-06 加固)

**所有访问 Tushare DuckDB 的脚本必须**:

1. **引擎层只读**: `duckdb.connect(DB_PATH, read_only=True)`
2. **审计日志**: 每次 exit 打印 `[DuckDB-AUDIT] 本次发起 N 个 SELECT,无可写操作`
3. **失败 fallback 立即走东财**,不重试(避免无意中写入)
4. **零依赖 local_api.py 是否被改**:自己建立只读连接

被拒绝的操作:`INSERT` / `UPDATE` / `CREATE` / `DELETE` / `ATTACH`(全部 `InvalidInputException`)。

---

## 🎓 3 大核心原则

1. **对齐优先于完美** — 每段产物必须是「上段可消化、本段可执行」的形态
2. **永远问"反证条件是什么"** — chain-verify 显式列出"什么情况下我会错"
3. **核销清单 = 纪律** — verify.md 的对齐验收清单,逐条核销到 ✅

---

## 🚫 红线

- ❌ 跳过 chain-idea 直接列数据
- ❌ 单向看好无反证
- ❌ chain-verify 没核销 ✅ 就算"完成"
- ❌ 硬塞投资建议(本 skill 只做产业链研究)
- ❌ 使用未公开数据
- ❌ 省略数据状态(已核验/估算/预期/待查证)
- ❌ 强周期行业不跑 chain-cycle
- ❌ **chain-radar 后直接跳到 chain-stockmap,跳过 1-6 段**(❌ 雷达只是入口,不是研究)

---

## 📚 借鉴来源 + 本 skill 扩展

| 来源 | 借鉴内容 | 类型 |
|---|---|---|
| 微信公众号「爱 AI 的大刘」《齐码.SKILL》(2026-06) | 6 段对齐架构 | 借鉴 |
| [harrischen/invest](https://github.com/harrischen/invest) | 三类缺口分类 + 多因子评分 + 微笑曲线 | 借鉴 |
| [zhangmusinb/gushifenxi-skill](https://github.com/zhangmusinb-dotcom/gushifenxi-skill) | 口径拆分 + 三端拆解 + 数据状态分层 | 借鉴 |
| **本 skill 扩展** | 「周期 × 缺口 × 政策」三角定位法 | **独创** |
| **本 skill 扩展** | chain-cycle 周期段(强周期行业必跑) | **独创** |
| **本 skill 扩展** | 16 种组合矩阵评级表 | **独创** |
| **本 skill 扩展** | chain-radar ETF 三轴扫描(v4.1) | **独创** |
| **本 skill 扩展** | chain-settlement 4 象限兑现度筛选(v4.0) | **独创** |
| **本 skill 扩展** | chain-chip-design 工艺路线子段 + 良率爬升 | **独创** |

---

## 🆕 演进路线

- **v1 (2026-07-01)** — 6 段对齐架构 + 借鉴基础
- **v2 (2026-07-02)** — 7 段(新增 chain-stockmap)+ 氟化工案例
- **v3 (2026-07-02)** — 8 段(新增 chain-cycle)+ 三角定位法 + 猪肉 + 创新药案例
- **v3.1 (2026-07-02)** — ★ 新增「格式选择卡」末段交付
- **v3.2 (2026-07-02)** — ★ 新增「chain-chip-design」工艺路线子段 + 光模块 + EML 双案例
- **v3.3 (2026-07-03)** — 产业链图升级为 PIL + cairosvg 高保真版 + 18 SVG 图标库
- **v3.4 (2026-07-03)** — Bootstrap Icons v1.x 实心版(19 个图标)+ 径向彩色光圈
- **v4.0 (2026-07-06)** — ★ 新增 chain-settlement(兑现度筛选)7.5 段
- **v4.1 (2026-07-06)** — ★ 新增 chain-radar(行业雷达)第 0 段,基于 1,561 只 ETF 三轴筛选
- **v4 后续预研** — 港股 18A API / LLM-driven 周期拐点 / 多产业链横向对比 / 飞书 webhook 自动跟踪 / PDF 输出

详细变更见 [CHANGELOG.md](CHANGELOG.md)。

---

## 📄 License

内部使用,未经作者许可不得商业发布。

---

*改编自「齐码.SKILL」by 爱 AI 的大刘 · Apply to Research Domain · 2026-07-02*
