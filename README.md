# 🔬 industry-chain-research

> **产业链深度研究 8 段对齐 skill · 三大独创方法论 · A 股强周期实战验证**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![v3.4.0](https://img.shields.io/badge/version-v3.4.0-blue)](https://github.com/ivanyinjc-blip/industry-chain-research/releases/tag/v3.4.0)
[![8-Segment Pipeline](https://img.shields.io/badge/8--Segment-Pipeline-success)]()
[![Cycle-Aware](https://img.shields.io/badge/Cycle--Aware-orange)]()
[![Chip-Design v3.2](https://img.shields.io/badge/Chip--Design-v3.2-purple)]()
[![Bootstrap Icons](https://img.shields.io/badge/Icons-Bootstrap-7952B3)](https://icons.getbootstrap.com/)

**`industry-chain-research`** 是一个面向 A 股 / 港股 / 美股产业链投研的 Claude skill,把"模糊研究问题"变成"立得住、还够狠、可核销"的产业链研究报告。

**3 行极简版:**
1. 8 段对齐 pipeline(idea → data → breakdown → cycle → analysis → report → ★格式选择卡 → verify → stockmap)
2. 三角定位法(周期 × 缺口 × 政策)+ 16 组合矩阵
3. 周期触发矩阵(6 RC)· 真实数据接口 · 报告自动渲染 HTML/DOCX

---

## ✨ 核心亮点(为什么要用)

### 🎯 1. 解决产业链研究 6 大痛点

| 痛点 | 现状 | 本 skill 解法 |
|---|---|---|
| 想法飘忽 | "研究一下 AI 芯片" → 没有边界 | **chain-idea** 口径拆分 + 三问法 |
| 数据散乱 | 微信群/研报/招股书各说各话 | **chain-data** 三端拆解(材料/设备/工艺) |
| 环节说不清 | 上中下游概念混淆 | **chain-breakdown** 4 维评分 + 3 类缺口 + 周期位置 |
| 缺周期判断 | 不区分顶部 / 底部 | **★ chain-cycle** 强周期行业必跑 |
| 缺反证 | 单向看好,缺乏证伪 | **chain-verify** 5 类核销 + 周期触发矩阵 |
| 结论不稳定 | 同样的研究换个时间出不同结论 | **三角定位法** 标准化评级 |

### 🏆 2. 三大独创方法论(本 skill 独家)

#### 2.1 「周期 × 缺口 × 政策」三角定位法

传统产业链研究:**产业链 → 环节 → 公司**(单维线性)
本 skill 升级版:**产业链 → 周期定位 × 缺口识别 × 政策环境 → 公司**(三维交叉)

```
                  政策环境
                    ↑
                    │
  周期位置 ←────── 环节 ──────→ 缺口识别
(顶部/下降/         │        (瓶颈/增量/
 底部/上升)        │         国产替代/新需求)
                    │
                    ↓
```

**16 种组合矩阵评级表**(本 skill 首创):

| 周期位置 | 缺口类型 | 政策环境 | 评级 | 典型案例 |
|---|---|---|---|---|
| 底部 | 国产替代 | 支持 | **★★★★★ 最佳** | 猪肉种猪育种 |
| 底部 | 增量 | 中性 | ★★★★ 良好 | - |
| 上升 | 国产替代 | 支持 | ★★★★ 良好 | 氟化工电子 HF |
| 上升 | 新需求 | 支持 | ★★★★ 良好 | 氟化工 PVDF |
| 顶部 | 任何 | 任何 | **★★ 规避** | - |
| 下降 | 任何 | 任何 | **★★ 规避** | - |
| ... (其余 10 种) | | | ★★★ 中等 | |

**对 A 股的关键意义**:A 股政策市特征鲜明(医保/集采/UVL/DRG),政策必须独立成轴 — 同一行业不同环节评级可差 3-4 星。

#### 2.2 三类缺口 + 国产替代 5 阶段(借鉴并升级 invest)

| 缺口类型 | 信号 | 验证方式 | A 股投资节奏 |
|---|---|---|---|
| **瓶颈型** | 涨价 / 交期拉长 / 产能>90% | 涨价持续性 | 看产能扩张 |
| **增量型** | 单位用量提升 / 渗透率加速 | 新需求兑现 | 看下游订单 |
| **★ 国产替代型** | 卡脖子 / 信创 / 政策驱动 | 国产化率 | **0-5% → 5-20% → 20-50% 加速 → 50%+** |
| **新需求型** | AI / 新材料 / 新工艺 | 技术验证 | 看突破节点 |

**国产替代 5 阶段曲线**(5-20% 阶段是 A 股最大投资主题):
```
0-5% 概念验证 → 5-20% 导入客户 → 20-50% 加速替代(★) → 50%+ 格局确立
```

#### 2.3 周期触发矩阵(RC · 6 类触发器 + 6 类反向风险)

| RC 编号 | 触发条件 | 验证时点 | 状态 |
|---|---|---|---|
| **RC-1** | 泽布替宁全球销售 > 30 亿美元/年 | 季度 | ⏳ |
| **RC-2** | 商保创新药目录落地 > 30 个 | 2026 Q3 | ⏳ |
| **RC-3** | 上游试剂市占率突破 30% | 年度 | ⏳ |
| **RC-4** | 美联储利率 < 4.00% | 月度 | ⏳ |
| **RC-5** | GLP-1 中国减肥获批 | 季度 | ⏳ |
| **RC-R** | 美国《生物安全法案》通过 | 实时 | ⚠️ |

**意义**:把"周期判断"从静态打分变成**事件驱动监控**,符合 A 股"政策市 + 资金市"特征。

### 🎁 3. 格式选择卡 · 末段交互式交付(v3.1 升级)

传统研究报告是**一锤子买卖**(发个 PDF 完事)。
本 skill 用 **CardKit 2.0 交互卡**,让用户在**同一会话**里二选一:
- 📄 **HTML** — 单文件 + 内嵌 CSS(响应式 + 数据状态徽章 + 评分星级)· 适合微信/飞书/邮件转发
- 📝 **DOCX** — pandoc 生成 · 适合打印或正式邮件附件

```
[chain-report 段]
   ↓
   报告生成卡(message_id om_xxx)
   ├─ 📄 HTML(推荐)
   └─ 📝 Word
       ↓
       [用户点选] → [card-click 回调] → [渲染] → [文件回传]
```

---

## 🆚 对比原参考 skill(升级点详解)

| 项目 | harrischen/invest | gushifenxi-skill | 齐码.SKILL | **本 skill v3.1** |
|---|---|---|---|---|
| 适用域 | 通用选股 | 个股深度 | 通用产品研发 | **产业链投研** |
| 输出 | 选股清单 | 个股研报 | 6 段对齐文档 | **8 段对齐 + 选股** |
| 周期判断 | 弱(只用周期因子) | 弱 | 无 | **★ 独立段 + 6 RC 监控** |
| 政策维度 | 无 | 弱 | 无 | **★ 三角定位第三轴** |
| 国产替代 | 无 | 弱 | 无 | **★ 5 阶段曲线 + 三角评级** |
| A 股覆盖 | 部分 | 强 | 通用 | **★ 极强(API 验证)** |
| 港股 / 美股 | 部分 | 弱 | 通用 | **A 股最强 / 港股占位 / 美股待定** |
| 报告输出 | 静态 | 静态 | markdown | **★ 交互式选择 HTML / DOCX** |
| 数据状态 | 无 | 估算/已核验 | 无 | **★ 5 层分层** |
| 反证条件 | 无 | verify 段 | 无 | **★ breakdown 段前置** |

### 三大架构升级

1. **6 段 → 8 段**:新增 **chain-cycle**(强周期必跑)+ **★ 格式选择卡**(交互交付)
2. **单维 → 三维**:单因子评分 → **「周期 × 缺口 × 政策」三角定位**
3. **静态 → 事件驱动**:从一次性打分 → **6 RC 周期触发监控**

---

## 🚀 快速开始

### 安装依赖

```bash
# 推荐 Python 3.10+
pip install -r requirements.txt
```

### 一键体验

```bash
# 1. 拉取任意 A 股的全套数据(行情/估值/财务/技术/资金)
python3 chain-stockmap/scripts/fetch_a_stock.py 600519 all

# 2. 周期触发矩阵 demo
python3 chain-verify/scripts/cycle_trigger.py

# 3. 报告渲染(HTML)
python3 chain-report/scripts/render_report.py report.md report.html html
```

### 在 Claude / Codex 中使用

把本仓库克隆到 `~/.claude/skills/industry-chain-research/`,Claude 会自动识别并按 8 段 pipeline 调度。

```bash
git clone https://github.com/<your-account>/industry-chain-research.git \
  ~/.claude/skills/industry-chain-research
```

对话示例:
> "用 industry-chain-research skill 分析创新药产业链"

Claude 会自动跑 8 段 pipeline,产出 6 段 markdown + 13 只 A 股选股清单 + 格式选择卡。

---

## 📁 仓库结构

```
industry-chain-research/
├── SKILL.md                          # 总纲:8 段对齐 + 三角定位法
├── README.md                         # 本文件
├── requirements.txt
│
├── chain-idea/                       # ① 立项段(三问法 + 11 词 + 四度评分)
├── chain-data/                       # ② 数据采集段(上中下游 + 三端 + 数据状态)
├── chain-breakdown/                  # ③ 拆分段(4 维评分 + 3 类缺口 + 周期位置)
├── chain-cycle/                      # ④ 周期段(6 类指标 + 拐点预测)★ 强周期必跑
├── chain-analysis/                   # ⑤ 分析段(三层价值量 + 微笑曲线 + 利润转移)
├── chain-report/                     # ⑥ 报告段(5 段叙事 + 数据状态分层)
│   └── scripts/
│       ├── render_report.py          # md → HTML / DOCX 渲染器
│       └── send_format_card.py       # 格式选择卡生成器
├── chain-verify/                     # ⑦ 验证段(5 类核销 + 周期触发矩阵)
│   └── scripts/
│       └── cycle_trigger.py          # 周期触发矩阵 demo
├── chain-stockmap/                   # ⑧ 选股清单段(价值量 × 财务 × 估值 × 技术)
│   └── scripts/
│       ├── fetch_stock.py            # 统一入口(A/HK/US 自动调度)
│       ├── fetch_a_stock.py          # A 股(东财 push2 + datacenter + AKShare)
│       ├── fetch_hk_stock.py         # 港股(腾讯 API)
│       └── fetch_us_stock.py         # 美股(腾讯 API)
│
├── templates/                        # 7 段产物模板
│   ├── idea.md.template
│   ├── data.md.template
│   ├── breakdown.md.template
│   ├── cycle.md.template
│   ├── analysis.md.template
│   ├── report.md.template
│   └── verify.md.template
│
└── examples/                         # 3 个完整产业链案例
    ├── fluorine-case/                # 氟化工(弱周期)7 段
    ├── pig-case/                     # 猪肉养殖(强周期)8 段 ★ 标杆
    └── innovative-drug-case/         # 创新药(政策 + 出海)8 段
```

---

## 🏭 实战案例

### 案例 1:猪肉养殖产业链(强周期 · 8 段)

**输入**:"用 industry-chain-research skill 分析猪肉养殖产业链"

**输出**:
- **强烈推荐** 1 只:**科前生物 688526**(4.35 分,动保抗周期)
- **推荐** 5 只:牧原 / 温氏 / 生物股份 / 普莱柯
- **中性** 3 只:新希望 / 大北农 / 京基智农

**关键发现**(用真实数据验证 v2 估算):
- 牧原从 v2 估算的 4.40 → v3 实测 3.30(财务塌方)
- 全板块 7 亏 1 微赚,印证 chain-cycle 段的「底部反转初」判断
- 强烈推荐从 v2 的 4 只降至 v3 的 1 只(数据诚实度的胜利)

### 案例 2:创新药产业链(政策 + 出海 · 8 段)

**输入**:"用 industry-chain-research skill 分析创新药行业"

**输出**:
- **强烈推荐** 4 只:**纳微科技 / 药明康德 / 恒瑞医药 / 键凯科技**
- **三角定位 5 环节评级**:
  - ★★★★★ 上游试剂(国产替代 ★)
  - ★★★★★ ADC 平台(出海 + 技术双驱动)
  - ★★★★ GLP-1 减肥(全球爆款新需求)
  - ★★★★ 核药(国产替代 + 新需求)
  - ★★ 规避 CXO 海外(美国《生物安全法案》风险)
- **罕见低估**:纳微科技 PE 10.44(国产替代 ★)

### 案例 3:氟化工产业链(弱周期 · 7 段)

**输入**:"用 industry-chain-research skill 分析氟化工"

**输出**:
- **强烈推荐** 2 只:**多氟多 4.43 / 巨化股份 4.16**
- 巨化 PE 19.5 最合理,多氟多 YoY 净利 +480%
- 全板块 BIAS > +9% 警惕回调

---

## 🛠 API 接入(真实数据)

### A 股 5 大接口

| 接口 | 数据源 | 字段 |
|---|---|---|
| **quote** | 东方财富 push2.eastmoney.com | 价格/换手/量比/PE/PB/市值 |
| **valuation** | 基于 quote 派生 | PE 分位/PS/安全边际 |
| **finance** | 东方财富 datacenter `RPT_F10_FINANCE_MAINFINADATA` | EPS/BVPS/毛利率/ROE/YoY/负债率 |
| **technical** | AKShare `stock_zh_a_hist` + 自计算 | MA5/10/20/60 + MACD + RSI + KDJ |
| **fund_flow** | AKShare `stock_individual_fund_flow` | 主力/超大单/大单/中单/小单 |

### 一键拉取

```bash
# 单股
python3 chain-stockmap/scripts/fetch_a_stock.py 600519 all

# 统一入口(A/HK/US)
python3 chain-stockmap/scripts/fetch_stock.py a 002714 quote
python3 chain-stockmap/scripts/fetch_stock.py hk 00700 finance
python3 chain-stockmap/scripts/fetch_stock.py us NVDA technical
```

---

## 🧠 借鉴 + 独创来源

| 来源 | 借鉴内容 | 类型 |
|---|---|---|
| 大刘《齐码.SKILL》(微信公众号) | 6 段对齐架构 + Design-by-Contract | 借鉴 |
| [harrischen/invest](https://github.com/harrischen/invest) | 多因子评分 + 选股落地 | 借鉴 |
| [zhangmusinb/gushifenxi-skill](https://github.com/zhangmusinb-dotcom/gushifenxi-skill) | 口径拆分 + 三端拆解 + 数据状态 | 借鉴 |
| **本 skill 独创** | **「周期 × 缺口 × 政策」三角定位法** | **独创** |
| **本 skill 独创** | **chain-cycle 周期段(强周期行业必跑)** | **独创** |
| **本 skill 独创** | **16 种组合矩阵评级表** | **独创** |
| **本 skill 独创** | **chain-breakdown 周期位置列** | **独创** |
| **本 skill 独创** | **chain-verify 周期触发矩阵** | **独创** |
| **本 skill 独创** | **chain-stockmap 周期评分因子** | **独创** |
| **本 skill 独创** | **★ 格式选择卡(交互式报告交付)** | **独创** |

---

## 🗺 演进路线

- **v1 (2026-07-01)**:6 段对齐架构 + 借鉴基础
- **v2 (2026-07-02)**:7 段(新增 chain-stockmap)+ 借鉴落地 + 氟化工案例
- **v3 (2026-07-02)**:8 段(新增 chain-cycle)+ 三角定位法 + 猪肉案例
- **v3.1 (2026-07-02)**:★ 新增「格式选择卡」末段交付 + 创新药案例
- **v4 路线**:
  - 港股 18A 接口(`fetch_hk_stock.py` 升级)
  - PDF 输出(weasyprint / wkhtmltopdf)
  - LLM-driven 周期拐点预测
  - 多产业链横向对比矩阵
  - 飞书 webhook 周期触发自动监控

---

## ⚖️ License

MIT License — 详见 [LICENSE](LICENSE) 文件。

## 🤝 贡献

欢迎 Issue / PR!特别欢迎:
- 新产业链案例(必须含 chain-cycle 段)
- 数据源扩展(港股 / 美股)
- 周期指标库扩充
- 报告渲染主题

## 📮 反馈

- **GitHub Issues**:bug / 功能建议 / 案例分享
- **微信公众号**:「爱AI的大刘」(《齐码.SKILL》原文出处)

---

**— 由 industry-chain-research skill 团队 2026-07 开源 · 改编自「齐码.SKILL」by 爱AI的大刘**

---

## 🆕 v3.2 更新(2026-07-02)

新增**第 2.5 段 `chain-chip-design`**(工艺路线分析子段),聚焦 device physics 拆解:

- **五钻探针**:工艺 + 衬底 + 设备 + 下一代 + 良率
- **mermaid.js 产业链图生成器**:`scripts/draw_chain.py`
- **实战案例**:`examples/optical-module-case/` + `examples/eml-substitution-case/`

### 4 张产业链图(单击 HTML 即看)

```bash
python3 chain-chip-design/scripts/draw_chain.py all_in_one diagram.html
```

生成 4 张图(单文件 HTML,mermaid.js CDN):

1. **光模块产业链全景** — 上中下游 + 每个环节 A 股龙头
2. **EML 国产替代链路** — InP 衬底 + MOCVD + 芯片 → 模块厂
3. **EML 工艺分代路线** — 2020 → 2024 → **2026(主流)** → 2028(异质集成)
4. **EML 国产化时间表 Gantt** — 25G ✓ / 50G 2026 H2 / 100G 2027 / 硅光 2027

### 关键实战数据(已核验)

| 数据 | 数值 | 含义 |
|---|---|---|
| 源杰科技 2026Q1 YoY 净利 | **+1153%** | EML 5-20% 阶段实证 ★ |
| 源杰科技 毛利率 | **77.81%** | **超国际同行**(Lumentum 50-55%) |
| 中际旭创 YoY 净利 | **+262%** | 800G 龙头规模壁垒 |
| 新易盛 YoY 营收 | **+106%** | 1.6T 首发 |


---

## 🆕 v3.3 更新(2026-07-03)

**PIL 产业链图生成器** — 把 mermaid.js 升级为高保真 PNG:

- **`chain-chip-design/scripts/draw_chain_v2.py`** — PIL + cairosvg 高保真(1920×1080)
- **18 个 SVG 图标库**:`icon_lib.py`(替代 emoji,跨平台一致)
- **设计语言沉淀**:`chain-chip-design/SKILL.md` 新增「产业链图生成系统」章节
- **实战图 2 张**:光模块 + EML 国产替代

---

## 🆕 v3.4 更新(2026-07-03)· 当前版本 ★

**Bootstrap Icons + 立体光圈** — 视觉对标麦肯锡 / Bloomberg 风格:

### 升级内容

1. **`icon_lib.py` 从自画几何 SVG → 19 个 Bootstrap Icons v1.x 实心版**
   - MIT license · 2000+ 图标库可选
   - CDN 自动下载 + 本地缓存(`~/.cache/bootstrap-icons/`)
   - jsdelivr CDN 取代 raw.githubusercontent.com(解决限速)

2. **`draw_chain_v2.py draw_icon_circle` 立体质感版**
   - 深色描边 + 2 层浅灰阴影(模拟凸起)
   - 18 圈同心圆径向彩色光圈(中心 alpha `0x70` → 边缘 `0x10`)
   - 65% 大号白色实心图标叠在光圈上(类似 app 图标高光)

### 视觉对比

| 维度 | v3.3 | v3.4 |
|---|---|---|
| 图标风格 | 几何描边 · 工程师风 | 工业实心 · 麦肯锡风 |
| 立体感 | 0 分 | ★★★★☆ |
| 图标库 | 18 个手画 | 19 个 Bootstrap(2000+ 可选) |
| 加新产业链图标成本 | 30 min(手画)| 0 min(改一行 `ICON_MAP`)|

### 4 张 demo 图(直接看效果)

| 案例 | v4(几何风)| v5(立体光圈)|
|---|---|---|
| 光模块产业链全景 | [optical-module-v4.png](chain-chip-design/docs/images/optical-module-v4.png) | [optical-module-v5.png](chain-chip-design/docs/images/optical-module-v5.png) |
| EML 国产替代 | — | [eml-substitution-v5.png](chain-chip-design/docs/images/eml-substitution-v5.png) |
| 图标局部放大(看光圈细节)| — | [icon-zoom-v5.png](chain-chip-design/docs/images/icon-zoom-v5.png) |

### 一键生成

```bash
# 光模块产业链图(1920×1080 PNG,带 Bootstrap Icons + 立体光圈)
python3 chain-chip-design/scripts/draw_chain_v2.py \
    optical_module /tmp/output/optical.png

# EML 国产替代图
python3 chain-chip-design/scripts/draw_chain_v2.py \
    eml_substitution /tmp/output/eml.png
```

### 复用成本对比

| 场景 | v3.3 | v3.4 |
|---|---|---|
| 加 1 个新产业链 | 手画 SVG(30 min)| 改 1 行 `ICON_MAP`(0 min) |
| 换风格主题 | 改 18 个 SVG | 改 `DS['blue']` 一个色 |
| 加更多图标 | 写新 SVG | Bootstrap Icons 2000+ 现成 |

### 待办 / v4 预研

- [ ] DALL-E 写实大图(光模块实物 / 数据中心照片)
- [ ] 多语言切换(中/英/日)
- [ ] 暗色模式 / 暖色 / 冷色 多主题

详细说明见:[chain-chip-design/SKILL.md · 产业链图生成系统](chain-chip-design/SKILL.md)


---

## 🆕 v4.0 更新(2026-07-06)· 兑现度筛选

### 痛点
v3.x 给的 10 只候选股只有"评分",**没有回答"哪些已经兑现了"** → 容易推荐到 Q1 同行抢筹高位股 → 用户买了就吃回调。

### 解法
**chain-settlement 4 象限分类**(7.5 段 · P0):

| 象限 | 含义 | 处理 |
|---|---|---|
| **Q1 同行抢筹** | Ps ≥ 6 + Pf ≥ 6 | ⚠️ 警惕追高 |
| **Q2 兑现期** | Ps ≥ 6 + Pf < 6 | ❌ 规避 |
| **Q3 价值洼地** ★ | Ps < 6 + Pf ≥ 6 | ✅ **关注池** |
| **Q4 潜伏** | Ps < 6 + Pf < 6 | 🔍 观察池 |

**评分公式**:`S = 0.6 × Ps(股价兑现) + 0.4 × Pf(业绩兑现)`
- `Ps(0-10)`:12M 涨幅 vs 行业中位数
- `Pf(0-10)`:0.5 × 扣非 12M 增速 + 0.5 × 经营现金流 12M 同比

### 数据访问加固
- **引擎层只读**:`duckdb.connect(DB_PATH, read_only=True)`
- **审计日志**:每次 exit 打印 `[DuckDB-AUDIT] 本次发起 N 个 SELECT,无可写操作`
- 拒绝 `INSERT` / `UPDATE` / `CREATE` / `DELETE` / `ATTACH`

### 实战案例(机器人产业链)
- **关注池 Q3**:鸣志电器(S=5.99) + 汇川技术(S=5.87)
- **警惕池 Q1**:绿的谐波 +314% / 埃斯顿 +143% 等 7 只

---

## 🆕 v4.1 更新(2026-07-06)· ★ 行业雷达 · 当前版本 ★★

### 痛点
**用户上来就"研究点啥好"** → 没人能给推荐 → 凭感觉选 → 行业研究做了 8 段但选错赛道 → 全部白做。

### 解法
**chain-radar 行业雷达(第 0 段)**:自动扫 1,561 只被动指数型 ETF → 三轴评分筛出 Top 1-2 行业 → 再走后续 8 段。

### 三轴评分
- **景气(40%)**:12M 涨幅 → [-25%, +25%] 映射 [0, 10]
- **趋势(30%)**:6M 涨幅(绝对值)→ [-25%, +25%] 映射 [0, 10]
- **拥挤反向(30%)**:1M 涨幅反向 → ≤-10% 给 10 分(超跌),≥+20% 给 0 分(过热)

**综合公式**:`R = 0.4 × 景气 + 0.3 × 趋势 + 0.3 × 拥挤反向`

### 评级映射
- ★★★★★ R ≥ 7.5 且 12M > 5%
- ★★★★ R ≥ 6.5
- ★★★ R ≥ 5.0
- ★★ R < 5.0 或 12M < -10%(规避)

### 关键修复(趋势分 v1 → v2)
- **v1 错误**:用 6M/12M 比率作为趋势分 → 当 12M 为负时比率反向上分
  - 例:医药 -2% / -5.85% = 2.84 → 趋势分 8.5 → 排第一(违反直觉)
- **v2 修复**:趋势分改为 6M 涨幅**绝对值**
- **关键洞察**:**当 12M 是负数时,任何比率计算都会反向,必须用绝对值**

### 实战扫描(2026-07-06)
| 排名 | 行业 | 雷达分 | 12M | 1M | 评级 |
|---|---|---|---|---|---|
| 1 | **光伏** | **8.71** | +48.1% | -10.0% | ★★★★★ |
| 2 | **AI** | **8.30** | +44.4% | +6.7% | ★★★★★ |
| 3 | **储能/碳中和** | **8.18** | +35.1% | -4.2% | ★★★★★ |
| 4 | **机器人/智造** | **7.96** | +44.9% | +9.5% | ★★★★★ |
| 5 | 新能源车 | 7.31 | +17.6% | -2.8% | ★★★★ |
| 6 | 周期资源 | 6.65 | +12.2% | -6.0% | ★★★★ |

### 9 段对齐架构(v4.1)
```
chain-radar (v4.1 新增)
  → chain-idea
  → chain-data
  → chain-chip-design (可选 · 半导体/光芯片)
  → chain-breakdown
  → chain-cycle (可选 · 强周期)
  → chain-analysis
  → chain-report
  → chain-settlement (v4.0 P0 · 兑现度筛选)
  → chain-stockmap
+ chain-verify(全程反证核销)
```

### 一键体验
```bash
# 1. 不知道研究哪个行业
python3 chain-radar/scripts/fetch_radar_data.py
python3 chain-radar/scripts/calc_radar_score.py /tmp/radar_raw.json /tmp/radar_scores.json
python3 chain-radar/scripts/gen_radar_report.py /tmp/radar_scores.json /tmp/radar.md
# → 选 Top 1-2 行业

# 2. 进入 9 段流水线(以 AI 为例)
# (按 segment 顺序跑 idea → data → breakdown → analysis → report → settlement → stockmap)
```

### 待办 / v5 预研
- [ ] 港股 18A API 接入(`fetch_hk_stock.py` 完善)
- [ ] LLM-driven 周期拐点预测
- [ ] 多产业链横向对比矩阵
- [ ] 飞书 webhook 自动跟踪(月度财报 + 公告)
- [ ] PDF 输出(weasyprint / wkhtmltopdf)

详细见 [CHANGELOG.md](CHANGELOG.md) 和 [docs/releases/v4.1.md](docs/releases/v4.1.md)。
