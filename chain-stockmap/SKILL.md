---
name: chain-stockmap
description: 产业链研究第 7 段 · 选股落地。把 chain-analysis 的"价值量定位"映射到 A 股/港股/美股具体上市公司。激活时机:chain-report 输出后,做最终选股清单。借鉴 invest 多因子评分 + gushifenxi 价值量定位。
---

---

## 📋 SKILL 契约(6 字段 · agent 调用入口)

> 完整的 选股清单 段契约。Claude/Codex 调用本段时,只需读这一节。

### 🎯 触发条件

- 前序段:chain-settlement 7.5 段已产 `07.5_settlement.md`

### 📥 输入文件

- 必填:`07.5_settlement.md` 的 Q3 关注池
- 可选:`04_cycle.md` 的周期评分因子

### 📤 输出文件

- `08_stockmap.md`(选股清单 + 评分 + 跟踪)
- 跟踪指标月度更新机制

### 🔑 必填字段

- 选股清单(Q3 池中精选 5-10 只)
- 多因子评分:价值量 × 财务 × 估值 × 技术 × 周期
- 跟踪触发条件
- 止盈/止损线

### ✅ 验收清单

- [ ] 选股数 5-10 只(可解释)
- [ ] 多因子评分有数字
- [ ] 跟踪触发可量化
- [ ] 止盈/止损线有依据

### ⚠️ 失败处理

- Q3 池 < 3 只 → 警告"行业机会不足"
- 多因子数据缺失 → 仅给评分,不进选股

---
# chain-stockmap · 选股落地段

> 灵感:invest 多因子评分 + gushifenxi 三层价值量定位
> 产物:`stockmap.md`(选股清单)
> 输入:chain-report.md + chain-analysis.md
> 输出:可执行的选股清单,带评分 + 反证 + 跟踪指标

## 🎯 这个 skill 干什么

把"产业链上哪个环节最值钱"**映射到"具体哪只股票值得买"**。

这是研究的最后一公里 —— 也是用户研究目的的核心:
> 通过产业链研究,发现卡点 / 国产替代 / 新材料新工艺新需求 → **映射到上市公司股票挖掘**

## 🧠 核心方法论:价值量定位 × 财务验证 × 估值对比 × 技术位置

每个候选股票都用 4 个维度交叉验证:

| 维度 | 借鉴自 | 解决什么问题 |
|---|---|---|
| **价值量定位** | gushifenxi | 这只股票在产业链的"价值集聚/中转/衰减"位置 |
| **财务验证** | invest | 营收/利润/EBIT/现金流是否支持"值钱" |
| **估值对比** | invest | 当前估值 vs 历史分位 + 同行,是否透支 |
| **技术位置** | invest | 多因子评分:趋势 + 资金 + 情绪 + 周期 + 板块 |

### 决策矩阵

| 价值量 | 财务 | 估值 | 技术 | 综合 |
|---|---|---|---|---|
| 价值集聚 | ✓✓ | < 历史 50% | 健康上行 | **强烈推荐** |
| 价值集聚 | ✓✓ | < 历史 50% | 弱势下行 | 关注底部反转 |
| 价值集聚 | ✓ | > 历史 80% | 健康上行 | 跟踪,等回调 |
| 中转 / 衰减 | ✓ | 任意 | 任意 | 不推荐 |

## 📐 11 词 · 在选股的体现

| 词 | 选股含义 |
|---|---|
| navigate | 下游应用主线 → 选股方向 |
| modal | 选股的最大风险点 |
| confirm | 增量兑现度的验证指标 |
| drawer | 隐藏成本的财务影响 |
| popover | 差异化卖点的可量化指标 |
| bottomsheet | 底部反转的技术信号 |
| toast | 短期跟踪事件(财报/订单/产能) |
| inline-expand | 价值量在个股的占比 |
| inline-edit | 成本结构变化对 EPS 的影响 |
| newtab | 新需求对估值的拉动 |
| download | 财报/估值/技术数据源 |

## 🛠 工作流(可执行版)

```
输入: chain-report.md + chain-analysis.md
  ↓
[Step 1: 候选股池建立]
  从 chain-report § 5 受益标的清单 + Top 3 环节的代表公司
  ↓
[Step 2: 价值量定位]
  对每只候选股,在产业链的"价值集聚/中转/衰减"位置
  ↓
[Step 3: 财务验证(脚本)]
  python3 scripts/fetch_stock.py a <code> finance
  → 营收增速 / EBIT / 现金流
  ↓
[Step 4: 估值对比(脚本)]
  python3 scripts/fetch_stock.py a <code> valuation
  → PE/PB/PS 历史分位
  ↓
[Step 5: 技术位置(脚本)]
  python3 scripts/fetch_stock.py a <code> technical
  → 多因子评分
  ↓
[Step 6: 综合打分]
  价值量 30% + 财务 25% + 估值 20% + 技术 25%
  ↓
[Step 7: 反证 + 跟踪清单]
  每只股票挂反证条件 + 短期跟踪事件
  ↓
[Step 8: 输出 stockmap.md]
```

## 📄 stockmap.md 输出模板

```markdown
# [项目名] · 选股清单

> 上游:chain-report v0.1 + chain-analysis
> 选股生成:YYYY-MM-DD  | 数据截止:YYYY-MM-DD

---

## 1. 候选股池

### 1.1 Top 3 环节映射
| 环节 | 缺口类型 | 价值量 | 候选股 | 代码 | 入选理由 |
|---|---|---|---|---|---|
| 环节 A | 国产替代 | 价值集聚 | | | |
| 环节 B | 瓶颈型 | 价值集聚 | | | |
| 环节 C | 新需求型 | 中转 | | | |

### 1.2 过滤规则
- ✓ 财务质量红旗(应收/存货/现金流)无问题
- ✓ 主营收入占比 > 50% 在产业链
- ✓ 排除 ST/退市风险
- ✓ 排除主营业务尚在概念阶段

---

## 2. 财务验证(脚本:scripts/fetch_stock.py finance)

| 公司 | 代码 | 营收增速 | EBIT Margin | 现金流 | 财务质量 | 数据状态 |
|---|---|---|---|---|---|---|
| | | | | | ✓/⚠️ | 已核验/估算/待查证 |

**财务红旗**:[如"应收 > 营收"等]

---

## 3. 估值对比(脚本:valuation)

| 公司 | PE | PE 历史分位 | 行业 PE | PS | 判断 | 数据状态 |
|---|---|---|---|---|---|---|
| | | | | | 便宜/合理/贵 | |

**隐含预期**:当前估值隐含未来需要 X% 增速才合理

---

## 4. 技术位置(脚本:technical · 多因子)

| 公司 | 趋势30% | 资金30% | 情绪20% | 周期10% | 板块10% | 总分 | 趋势阶段 | 数据状态 |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | 健康上行/震荡/弱势 | |

**关键位置**:当前价/支撑/压力

---

## 5. 综合评分

| 公司 | 价值量30% | 财务25% | 估值20% | 技术25% | **总分** | 评级 | 数据状态 |
|---|---|---|---|---|---|---|---|
| | | | | | | 强烈推荐/推荐/中性/谨慎 | |

评级:≥ 4.0 强烈推荐 | 3.0-3.9 推荐 | 2.0-2.9 中性 | < 2.0 谨慎

---

## 6. 反证 + 跟踪清单(每只股票)

### 公司 A · [代码]
- **反证条件**:
  - [ ] 若 [X 数据] 出现,评级下调
  - [ ] 若 [Y 事件] 发生,逻辑失效
- **短期跟踪事件**:
  - [ ] YYYY-MM-DD 财报
  - [ ] [公司事件]
- **关键财务指标**:
  - 营收增速 > 20%
  - EBIT Margin > 行业均值
  - 经营现金流 > 0

### 公司 B · [代码]
(同上结构)

---

## 7. 行动方案(借鉴 invest · 风险管理)

| 公司 | 仓位 | 买入区间 | 止损(-7%~-10%) | 第一目标 | 第二目标 | 移动止损 |
|---|---|---|---|---|---|---|
| | | | | | | 盈利>15% 上移至成本 |

---

## 8. 数据局限性与免责声明

- 数据来源:[腾讯/新浪API + Tushare + 协会数据],YYYY-MM-DD
- 局限性:
  - 财务数据可能滞后 1 个季度
  - 技术数据盘中可能变动
  - 估值历史分位基于近 3 年,极端行情外推风险
- **免责声明**:本清单仅供参考,不构成任何投资建议。投资有风险,入市需谨慎。
```

## 📁 scripts/ 目录

```
scripts/
├── fetch_stock.py        # 统一入口(a / hk / us)
├── fetch_a_stock.py      # A 股:腾讯/新浪
├── fetch_hk_stock.py     # 港股:腾讯/新浪
├── fetch_us_stock.py     # 美股:腾讯
└── requirements.txt      # httpx, pandas, akshare
```

## 🚦 何时启用

- chain-report 完成报告后,做最终选股落地
- 用户明确要求"出选股清单"
- chain-verify 发现反证条件触发时,回查 stockmap

## ⚠️ 红线

- ❌ 不准"价值量定位"空着 — 没定位的选股是赌博
- ❌ 不准财务红旗出现却无说明 — 风险被忽略 = 推荐失败
- ❌ 不准技术位置总分 < 2.5 仍给"推荐" — 一致性检查必做
- ❌ 不准省略反证条件 + 跟踪清单 — 选股不是一次性输出
- ❌ 不准隐瞒数据局限性 — 免责声明是底线

## 🔗 与上下游的契约

- **上游(chain-report)**:受益标的清单 + Top 3 环节价值量定位
- **上游(chain-analysis)**:三层价值量定位 + 反证条件
- **下游(chain-verify)**:stockmap.md 的"反证条件 + 跟踪事件" → 直接进入核销清单

## 🧰 脚本接口(借鉴 invest run.py)

```bash
# 统一入口
python3 scripts/fetch_stock.py <market> <code> <data_type>

# 示例
python3 scripts/fetch_stock.py a 600519 finance
python3 scripts/fetch_stock.py hk 00700 technical
python3 scripts/fetch_stock.py us NVDA valuation

# market: a / hk / us
# data_type: quote / finance / technical / fund_flow / valuation / all
```

**首次运行**:自动创建虚拟环境 + 安装依赖(httpx + pandas + akshare)

**降级策略**(借鉴 invest):
- L1 精确:脚本返回 `status: ok` → `[腾讯/新浪API, 日期]`
- L2 近似:脚本失败 + WebSearch 拿到 → `[搜索摘要, 日期, 可能存在偏差]`
- L3 缺失:脚本 + 搜索均失败 → `N/A(获取失败)` + 评分取保守值

---

## 🆕 chain-settlement 子段(兑现度筛选 · 7.5 段 · 2026-07-06 v4 P0 新增)

> **归属说明**:chain-settlement 是 chain-stockmap 的 7.5 段(在 stockmap 选股清单基础上做兑现度筛选),代码共用 `chain-stockmap/scripts/`,文档共用 `chain-stockmap/SKILL.md`。


> 痛点:既有 stockmap 给的 10 只股票,只有"评分",没有回答"哪些已经兑现了"
> 解法:在 stockmap 候选清单上做 4 象限筛选,提纯出真正值得关注池

### 1. 兑现度评分算法

```
S(综合) = 0.6 × Ps(股价兑现) + 0.4 × Pf(业绩兑现)

其中:
- Ps(0-10):12M 涨幅 vs 行业中位数(中位数 = 5,超额 +100pp = 10)
- Pf(0-10):0.5 × 扣非 12M 增速 + 0.5 × 经营现金流 12M 同比
```

### 2. 4 象限分类

| 象限 | 含义 | 处理 |
|---|---|---|
| **Q1 同行抢筹** | Ps ≥ 6 + Pf ≥ 6(业绩兑现 + 股价兑现) | ⚠️ 警惕追高 |
| **Q2 兑现期 / 终结期** | Ps ≥ 6 + Pf < 6(股价兑现但业绩未跟上) | ❌ 规避 |
| **Q3 价值洼地** ★ | Ps < 6 + Pf ≥ 6(业绩兑现但股价未涨) | ✅ **关注池** |
| **Q4 潜伏 / 没起来** | Ps < 6 + Pf < 6(业绩未兑现,市场未抢) | 🔍 观察池 |

### 3. 兑现度反例

筛选 `fund_flow > 1 亿(60 日)+ 涨幅 < 行业基准 + Pf ≥ 6` 的标的 = 资金已埋伏但股价未涨 = 强信号关注。

### 4. 脚本与产物

```
chain-stockmap/
├── scripts/
│   ├── fetch_settlement_data.py  # 数据采集(K线/季报/资金流/行业 ETF)
│   ├── calc_settlement_score.py  # 评分算法 + 4 象限分类
│   └── gen_settlement_report.py  # 出 Markdown 报告
├── templates/
│   └── settlement.md.template    # 报告模板
└── examples/
    └── robot-case/
        ├── settlement.md          # 机器人产业链样本报告
        ├── settlement_data.json   # 全量原始数据
        └── settlement_scores.json # 评分 + 关注池
```

### 5. 用法

```bash
# 1. 采集数据(从 stockmap.md 解析股票清单)
python3 scripts/fetch_settlement_data.py \
  /path/to/case/09-stockmap/stockmap.md \
  /tmp/settlement_data.json \
  562500.SH,159770.SZ,562360.SH,159258.SZ
# ↑ 第三个参数:行业 ETF 基准列表(逗号分隔)

# 2. 算评分
python3 scripts/calc_settlement_score.py \
  /tmp/settlement_data.json \
  /tmp/settlement_scores.json

# 3. 出报告
python3 scripts/gen_settlement_report.py \
  /tmp/settlement_scores.json \
  /path/to/case/09-stockmap/settlement.md \
  /path/to/case/09-stockmap/stockmap.md \
  "机器人产业链"
```

### 6. 数据源(已确认全部接通)

| 数据 | 源 |
|---|---|
| K 线 12M | 东财 push2his.eastmoney.com(直调) |
| 4 季度财务 | AKShare stock_profit_sheet_by_quarterly_em + stock_cash_flow_sheet_by_quarterly_em |
| 行业 ETF 基准 | Tushare DuckDB(本地数据库,见 ~/.local/share/tushare_pipeline/local_api.py) |
| 60 日主力净流入 | 东财 push2his 资金流接口 |

### 7. 与总框架的关系

- **位置**:`chain-verify` 和 `chain-stockmap` 之间(第 7.5 段)— 即核销清单后、最终选股清单前
- **输入**:`stockmap.md` 候选清单(10-30 只)
- **输出**:`settlement.md`(包含 4 象限 + 关注池 + 反例 + 跟踪指标)
- **建议**:在得到 stockmap.md 后**先**跑 settlement 筛选,再把 settlement.md 喂给用户作为最终选股交付

### 8. 兑现度反例(参考 · 2026-07-06 机器人产业链案例)

| 关注池(Q3 价值洼地) | S | 说明 |
|---|---|---|
| 鸣志电器(603728) | 5.99 | Ps=5.99 < 6(股价涨 23% < 行业 43%),Pf=6.0 ≥ 6(业绩兑现) |
| 汇川技术(300124) | 5.87 | Ps=5.64, Pf=6.22 |

**警惕池(Q1 已充分兑现)**:绿的谐波 +314%、埃斯顿 +143%、奥普特 +76%、恒立液压 +77% 等 7 只
**Q4 观察池**:秦川机床(业绩未兑现)

---

## 🔒 数据访问约束(2026-07-06 加固)

### DuckDB 只读访问(强约束)

`fetch_settlement_data.py` 中的 `_ReadOnlyDuckDB` 类:
- **强制** `duckdb.connect(DB_PATH, read_only=True)` — DuckDB 引擎级别写保护
- **审计** 每次 exit 打印 `[DuckDB-AUDIT] 本次发起 N 个 SELECT,无可写操作`
- **fallback** DB 失败立即走东财,不重试(避免无意中写入)
- **零依赖** 不依赖 local_api.py 是否被改 — 自己建立只读连接

DuckDB 引擎对 read_only 连接,所有 DDL/DML 都会被拒绝:

```
✓ SELECT OK
✓ INSERT 被拒绝: InvalidInputException
✓ UPDATE 被拒绝
✓ CREATE 被拒绝
✓ DELETE 被拒绝
✓ ATTACH 被拒绝(避免"复制 DB"逃逸)
```

### 已验证(机器人产业链样本运行后)

```
[DuckDB-AUDIT] 本次发起 4 个 SELECT,无可写操作
access_mode: read_only
```

### local_api.py 可选加固(待用户决定)

`_ReadOnlyDuckDB` 已经足够安全,如果想让 4 个项目内所有脚本都默认只读,可在 `local_api.py` 顶部替换:

```python
def get_conn():
    return duckdb.connect(str(DB_PATH), read_only=True)  # 加 read_only=True
```

这是用户的脚本,改动与否由你决定。 我会**建议**加但**不主动改**(我没有写权限)。
