---
name: industry-chain-research
description: 产业链深度研究 8 段对齐 skill。借鉴「齐码.SKILL」Design-by-Contract 思想 + harrischen/invest 多因子评分 + zhangmusinb/gushifenxi 深度研究方法,形成「周期 × 缺口 × 政策」三角定位法的独特方法论。每段输入=上段产物,实现"结论=证据"的全链路对齐。包含三层价值量(成本/利润/瓶颈)、三类缺口(瓶颈/增量/国产替代/新需求)、反证条件、跟踪指标。聚焦 A 股 + 港股 + 美股产业链投研。
---

# 产业链深度研究 Skill · 8+1 段对齐(2026-07-02 v3.2 升级)

> 灵感来源:
> 1. 微信公众号「爱AI的大刘」《齐码.SKILL》(2026-06)— 6 段对齐架构
> 2. [harrischen/invest](https://github.com/harrischen/invest) — 多因子评分 + 选股落地
> 3. [zhangmusinb-dotcom/gushifenxi-skill](https://github.com/zhangmusinb-dotcom/gushifenxi-skill) — 口径拆分 + 三层价值量 + 数据状态
> 
> 作者改编:Claude(阿超投资助理) · 2026-07-02
> 适用:A 股 / 港股 / 美股产业链投研(二级市场视角)

## 🎯 这个 skill 解决什么

产业链研究常见的 6 个痛点:

| 痛点 | 现状 | 本 skill 解法 |
|---|---|---|
| 想法飘忽 | "研究一下 AI 芯片" → 没有边界 | chain-idea 口径拆分 + 三问法 |
| 数据散乱 | 微信群/研报/招股书各说各话 | chain-data 三端拆解 + 11 词 + 数据状态 |
| 环节说不清 | 上中下游概念混淆 | chain-breakdown 三类缺口 + 周期位置 |
| 缺周期判断 | 不区分周期顶部 / 底部 | **chain-cycle(新增)周期定位** |
| 缺反证 | 单向看好,缺乏证伪 | chain-verify + 全程反证前置 |
| 结论不稳定 | 同样的研究换个时间出不同结论 | 「周期 × 缺口 × 政策」三角定位法 |

## 📐 8+1 段对齐架构(2026-07-02 升级:新增周期段 + chip-design 子段 + 政策方法论)

```
     ┌─────────────────┐
     │  chain-idea     │ ① 待研究问题 + 口径 + 周期/政策前置
     │  +周期政策前置   │   (借鉴 gushifenxi + 本 skill 独创)
     └──────┬──────────┘
            ▼
     ┌──────────────────┐
     │  chain-data      │ ② 上中下游 + 三端 + 周期性数据
     │  +三端+周期数据  │   (借鉴 gushifenxi)
     └──────┬───────────┘
            ▼
     ┌────────────────────┐
     │ chain-chip-design  │ ②.5 工艺路线 + 衬底设备 + 良率爬升
     │ +chip-design(可选)│   (本 skill 独创 — 半导体/光芯片强相关)
     │ ★ 产业链图生成    │   mermaid.js 内嵌 HTML,每环节标 A 股龙头
     └──────┬─────────────┘
            ▼
     ┌────────────────────┐
     │ chain-breakdown    │ ③ 4 维评分 + 三类缺口 + 周期位置
     │  +三类缺口+周期   │   (借鉴 invest + 本 skill 独创)
     └──────┬─────────────┘
            ▼
     ┌────────────────────┐
     │ chain-cycle(可选) │ ④ 周期类型 + 周期阶段 + 拐点预测
     │  ★强周期行业必跑   │   (本 skill 独创)
     └──────┬─────────────┘
            ▼
     ┌──────────────────────┐
     │ chain-analysis       │ ⑤ 三层价值量 + 微笑曲线 + 利润转移 + 周期影响
     │  +利润转移+周期传导  │   (借鉴 invest)
     └──────┬───────────────┘
            ▼
     ┌──────────────────────┐
     │ chain-report         │ ⑥ 研报骨架 + 数据状态分层
     │  +数据状态列          │   (借鉴 gushifenxi)
     └──────┬───────────────┘
            ▼
     ┌──────────────────────┐
     │ ★ 格式选择卡         │ ⑦ 交互卡二选一(本 skill 独创)
     │  HTML / DOCX         │   HTML 单文件 · DOCX pandoc
     └──────┬───────────────┘
            ▼
     ┌──────────────────────┐
     │ chain-verify         │ ⑦ 反证 + 跟踪 + 周期触发矩阵 + 核销清单
     │  +周期触发矩阵        │   (本 skill 独创)
     └──────┬───────────────┘
            ▼
     ┌──────────────────────┐
     │ chain-stockmap       │ ⑧ 价值量 × 财务 × 估值 × 技术 × 周期
     │  +周期评分因子        │   (借鉴 invest + 本 skill 独创)
     │  → stockmap.md       │   ★ 用户研究目的最终落地
     └──────────────────────┘
```

**可选段**:chain-cycle 仅在**强周期行业**(农业 / 化工 / 半导体 / 钢铁 / 煤炭 / 航运)**必跑**,其他行业可选。

## 🎓 3 大核心原则(Design by Contract)

1. **对齐优先于完美**
   每段产物必须是「上段可消化、本段可执行」的形态。先达成"含义一致",再追求"内容完备"。

2. **永远问"反证条件是什么"**
   任何一个观点/结论,都必须在 chain-analysis/chain-verify 显式列出"什么情况下我会错"。这是 95% → 75% 的去伪关键。

3. **核销清单 = 纪律**
   chain-verify 输出"对齐验收清单",逐条核销 report.md 中的每个结论,直到 ✅。这是对齐的最后一公里。

## 🛠 8 个核心模块(7 段 + 1 可选 + 总纲)

| # | 模块 | 产物 | 输入 | 核心方法论 | 必跑 |
|---|---|---|---|---|---|
| 0 | **总纲**(本文件) | 调度指令 | 用户提问 | 哪一段被激活 | - |
| 1 | **chain-idea** | idea.md | 用户模糊问题 | 三问法 + 口径拆分 + 11 词法 + **周期/政策前置** | ✅ |
| 2 | **chain-data** | data.md | idea.md | 上中下游 + 材料/设备/工艺三端 + **周期性数据** | ✅ |
| 2.5 | **chain-chip-design**(可选) | chip-design.md + 产业链图 HTML | data.md | **device physics 工艺路线 + 良率爬升 + 下一代路径 + mermaid 图** | ⚠️ 半导体/光芯片/化合物半导体必跑 |
| 3 | **chain-breakdown** | breakdown.md | data.md | 4 维评分 + 三类缺口 + **周期位置** | ✅ |
| 4 | **chain-cycle**(可选) | cycle.md | breakdown.md | **6 类周期指标 + 拐点预测** | ⚠️ 强周期必跑 |
| 5 | **chain-analysis** | analysis.md | breakdown + cycle | 三层价值量 + 微笑曲线 + 利润转移 + 周期影响 | ✅ |
| 6 | **chain-report** | report.md | analysis.md | 5 段叙事 + 11 词强制覆盖 + 数据状态分层 | ✅ |
| 6.5 | **★ 格式选择卡** | 卡片按钮回调 | report.md | CardKit 2.0 交互卡 → HTML / DOCX | ✅(report 后必跑) |
| 7 | **chain-verify** | verify.md | report.md | 5 类核销 + **周期触发矩阵** + 月度跟踪 | ✅ |
| 8 | **chain-stockmap** | stockmap.md | report + analysis | 价值量 × 财务 × 估值 × 技术 × **周期** | ✅ |

## 🌟 独特方法论:「周期 × 缺口 × 政策」三角定位法

**这是本 skill 从氟化工 + 猪肉两个案例中提炼出来的独特方法论**,区别于市场上所有同类 skill。

### 核心思想

传统产业链研究:产业链 → 环节 → 公司(单维线性)

本 skill 升级版:**产业链 → 周期定位 × 缺口识别 × 政策环境 → 公司(三维交叉)**

### 三角定位法

每个环节都在三角坐标系中打分,三轴综合评级:

```
                  政策环境
                    ↑
                    │
                    │
                    │
  周期位置 ←────── 环节 ──────→ 缺口识别
(顶部/下降/         │        (瓶颈/增量/
 底部/上升)        │         国产替代/新需求)
                    │
                    │
                    ↓
```

### 16 种组合矩阵(评级表)

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
| ... (其余 8 种组合) | | | ★★★ 中等 | |

### 三轴评分细则

#### 轴 1 · 周期位置(0-10 分)
- 底部 = 10 分(最佳左侧布局点)
- 下降末 = 8 分
- 上升初 = 7 分
- 上升中 = 6 分
- 顶部 = 3 分(规避)
- 下降初 = 4 分(规避)

#### 轴 2 · 缺口类型(0-10 分)
- 国产替代 20-50% 加速阶段 ★ = 10 分
- 卡脖子 + 政策支持 = 9 分
- 新需求型(AI/新能源/固态电池) = 8 分
- 增量型 + 渗透率 < 30% = 7 分
- 瓶颈型 + 涨价 = 6 分
- 成熟期 + 国产化率 > 70% = 3 分

#### 轴 3 · 政策环境(0-10 分)
- 明确支持 + 资金投入 = 10 分
- 明确支持 = 8 分
- 中性 = 5 分
- 政策不确定性 = 4 分
- 政策抑制 = 2 分

**综合评级公式**:`综合分 = 周期 × 0.3 + 缺口 × 0.4 + 政策 × 0.3`(权重可调)

### 应用示例

**案例 1 · 猪肉种猪育种**:
- 周期位置:底部(能繁母猪 3900 万)→ 8 分
- 缺口类型:国产替代 5-20% 阶段 + 卡脖子 → 9 分
- 政策环境:种业振兴明确支持 → 9 分
- **综合**:8×0.3 + 9×0.4 + 9×0.3 = 8.7 → ★★★★★ 最佳

**案例 2 · 氟化工电子级 HF**:
- 周期位置:上升(半导体扩产周期)→ 7 分
- 缺口类型:国产替代 < 20% + 卡脖子 → 10 分
- 政策环境:中性(无明确配额/补贴)→ 5 分
- **综合**:7×0.3 + 10×0.4 + 5×0.3 = 7.7 → ★★★★ 良好

**对比 1 · 房地产链**:
- 周期位置:下降 → 3 分
- 缺口类型:无 → 3 分
- 政策环境:抑制 → 2 分
- **综合**:3×0.3 + 3×0.4 + 2×0.3 = 2.7 → ★★ 规避

## 🎯 用户研究目的的最终落地

**研究目的(用户原话)**:
> 通过产业链研究,**发现卡点 / 国产替代需求 / 新材料新工艺新需求环节**,进而**映射到上市公司的股票挖掘**这个最终目的上。

8 段 pipeline 的目的映射:

| 用户目的 | 对应段 | 产出 |
|---|---|---|
| 卡点识别 | chain-breakdown § 三类缺口 | 瓶颈型环节清单 |
| 国产替代 | chain-breakdown § 三类缺口 + chain-analysis | 0-100% 替代曲线定位 |
| 新材料新工艺新需求 | chain-breakdown + chain-analysis § 新需求型 | 新材料/工艺/应用环节 |
| **股票挖掘(最终目的)** | **chain-stockmap** | **stockmap.md 选股清单 + 评分 + 跟踪** |
| **周期判断(本 skill 独创)** | **chain-cycle + 三角定位** | **cycle.md + 综合评级** |

## 🚦 何时激活

- 用户说"研究一下 XX 产业链"、"拆 XX 上中下游"、"XX 怎么看"
- 用户说"XX 公司值不值得买"(从 chain-idea 开始走)
- 用户说"出选股清单 / 映射到股票"(从 chain-stockmap 开始)
- **强周期行业**(农业/化工/半导体/钢铁/煤炭/航运)— **必跑 chain-cycle**
- 投研任务:写产业链报告、做供应链梳理、画价值量分布、跟踪上市公司公告
- 任何需要"系统化研究问题"而不是"问一句答一句"的场景

## 🚫 红线

- ❌ **不要跳过 chain-idea** 直接列数据 — 立项没想清楚,后面 7 段都白做
- ❌ **不要缺反证条件** — 单向看好 = 让人赔钱的姿势
- ❌ **不要忘记"实现=设计"** — chain-verify 核销 ✅ 之前,不算研究完成
- ❌ **不要硬塞投资建议** — 本 skill 只做产业链研究,chain-stockmap 才给选股清单
- ❌ **不要使用未公开数据** — 数据真实性是根基
- ❌ **不要省略数据状态** — 研报和选股清单的每个数据必须标"已核验/估算/预期/待查证"
- ❌ **强周期行业不跑 chain-cycle** — 周期判断缺失会让分析偏 1-2 个等级

## 📚 借鉴来源 + 本 skill 独创

| 来源 | 借鉴内容 | 类型 |
|---|---|---|
| 大刘《齐码.SKILL》(微信公众号) | 6 段对齐架构 | 借鉴 |
| [harrischen/invest](https://github.com/harrischen/invest) | 三类缺口分类 | 借鉴 |
| [harrischen/invest](https://github.com/harrischen/invest) | 多因子评分 + 选股落地 | 借鉴 |
| [harrischen/invest](https://github.com/harrischen/invest) | 微笑曲线 + 利润转移 | 借鉴 |
| [zhangmusinb/gushifenxi-skill](https://github.com/zhangmusinb-dotcom/gushifenxi-skill) | 口径拆分 | 借鉴 |
| [zhangmusinb/gushifenxi-skill](https://github.com/zhangmusinb-dotcom/gushifenxi-skill) | 三端拆解(材料/设备/工艺) | 借鉴 |
| [zhangmusinb/gushifenxi-skill](https://github.com/zhangmusinb-dotcom/gushifenxi-skill) | 数据状态分层 | 借鉴 |
| **本 skill 独创** | **「周期 × 缺口 × 政策」三角定位法** | **独创** |
| **本 skill 独创** | **chain-cycle 周期段(强周期行业必跑)** | **独创** |
| **本 skill 独创** | **16 种组合矩阵评级表** | **独创** |
| **本 skill 独创** | **chain-breakdown 周期位置列** | **独创** |
| **本 skill 独创** | **chain-verify 周期触发矩阵** | **独创** |
| **本 skill 独创** | **chain-stockmap 周期评分因子** | **独创** |

## 🧰 模板与示例

- `templates/idea.md.template` — chain-idea 的标准产物格式(含周期政策前置)
- `templates/data.md.template` — chain-data 的标准产物格式(含周期性数据)
- `templates/breakdown.md.template` — chain-breakdown(含周期位置)
- `templates/cycle.md.template` — chain-cycle(可选,强周期行业)
- `templates/analysis.md.template` — chain-analysis
- `templates/report.md.template` — chain-report
- `templates/verify.md.template` — chain-verify(含周期触发矩阵)
- `templates/stockmap.md.template` — chain-stockmap(含周期评分)
- `examples/fluorine-case/` — 氟化工完整 7 段样本(弱周期)
- `examples/pig-case/` — 猪肉完整 8 段样本(强周期 + chain-cycle)
- `examples/innovative-drug-case/` — 创新药完整 8 段样本(政策 + 出海)
- `examples/optical-module-case/` — 光模块产业链(2026-07-02 实战,11 只 A 股已核验 ★ 含产业链图)
- `examples/eml-substitution-case/` — EML 国产替代深度(2026-07-02 实战,3 只 A 股已核验 ★ 含工艺路线)
- `examples/eml-chip-design-case/` — EML chip-design 工艺路线卡片(本 skill v3.2 新增)

## 🆕 演进路线

- **v1 (2026-07-01)**:6 段对齐架构 + 借鉴基础
- **v2 (2026-07-02)**:7 段(新增 chain-stockmap)+ 借鉴落地 + 氟化工案例
- **v3 (2026-07-02)**:8 段(新增 chain-cycle)+ 三角定位法 + 猪肉案例 + 创新药案例
- **v3.1 (2026-07-02)**:★ 新增「格式选择卡」末段交付(report.md → HTML/DOCX 二选一)
- **v3.2 (2026-07-02)**:★ 新增「chain-chip-design」工艺路线子段(device physics 拆解 + 良率爬升 + mermaid 产业链图)+ 光模块 + EML 国产替代双案例完整跑通 ← **当前**
- **v4 预研方向**:
  - fetch_stock.py 接港股 18A API(fetch_hk_stock.py)
  - LLM-driven 周期拐点预测
  - 多产业链横向对比矩阵
  - 跟踪指标自动监控(飞书 webhook)
  - PDF 输出(weasyprint / wkhtmltopdf)

---

*— 改编自「齐码.SKILL」by 爱AI的大刘 · Apply to Research Domain · 2026-07-02*
