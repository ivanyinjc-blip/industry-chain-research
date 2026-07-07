## [v4.1.1] - 2026-07-07 · ★ Industrialization(工程化补齐)

**目标**:把方法论优势 + 工程化短板补齐,从"可读 skill"升级到"可生产 skill"。

### 6 阶段升级

1. **数据字段校验**
   - 修复 v4.1.0 bug:`fetch_a_stock.py` 中 f191(PE)/f167(PB) 错误除以 100
   - 新增 `FIELD_META` 字段元数据(19 个字段,带单位/口径/来源)
   - 新增 `validate_valuation()` 异常校验:5 个等级(ok/warning/suspect)
   - 验证用例:茅台 PE 从 -14.43 修复为 25.6(正常区间)

2. **可复现运行环境**
   - 重写 `requirements.txt`:从 4 个包 → 13 个包(带 minor pin)
   - 新增 `pyproject.toml`:PEP 621 标准 + ruff 配置
   - 新增 `Makefile`:8 个 target(install/test/lint/run-*/clean)
   - 新增 `setup.sh`(Linux/macOS)+ `setup.ps1`(Windows)

3. **硬编码路径 → 环境变量**
   - 修复 `fetch_radar_data.py` 和 `fetch_settlement_data.py` 硬编码 `/mnt/e`
   - 新增 `chain-stockmap/scripts/_lib/config.py`:`get_db_path()` 统一入口
   - 不设环境变量时给清晰错误(带 4 平台设置命令)
   - 跨 Win/macOS/Linux 三平台可配置

4. **文档版本一致**
   - 顶部 description:8 段 → 9 段
   - "本 skill 独创" → "本 skill 扩展"(20+ 处)
   - "独特方法论" → "差异化方法论"
   - chain-settlement 归属明确:7.5 段,代码在 chain-stockmap

5. **测试 + CI**
   - 新增 6 个测试文件,25 个用例(全部通过)
   - `pytest.ini` + `ruff.toml`
   - GitHub Actions CI:Ubuntu × Python 3.10/3.11/3.12 矩阵

6. **SKILL.md 重写**
   - 根 SKILL.md 精简到 202 行(原 298 行)
   - 10 个子 SKILL.md 全部加 6 字段契约(触发条件/输入/输出/必填字段/验收清单/失败处理)

### 验收

- 测试:25/25 通过
- 编译:16/16 .py 编译通过
- 文档:0 处"本 skill 独创"残留
- 硬编码:0 处 `/mnt/*`
- 段数:全部统一为 9 段

---

# Changelog · industry-chain-research skill

所有版本变更按 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 格式记录。
版本号遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

---

## [v4.1] - 2026-07-06 · ★ 行业雷达段(第 0 段)

### 新增
- **chain-radar**(第 0 段) · 基于 1,561 只被动指数型 ETF 的「景气 × 趋势 × 拥挤反向」三轴评分
  - 扫描 14 个重点行业 + 自动产出 Top 1-2 推荐研究赛道
  - 三轴评分:景气 12M (40%) / 趋势 6M (30%) / 拥挤反向 1M (30%)
  - 评级映射:★★★★★ R≥7.5 + 12M>5% / ★★★★ R≥6.5 / ★★★ R≥5.0 / ★★ R<5.0
  - 脚本 `fetch_radar_data.py` + `calc_radar_score.py` + `gen_radar_report.py`
  - 数据源:Tushare DuckDB `fund_basic` + `fund_daily`(只读,250 交易日窗口)
  - 实战样本:`chain-radar/examples/radar-2026-07-06/`(2026-07-06 扫描结果)
  - **v1 → v2 关键修复**:趋势分从 6M/12M 比率改为 6M 涨幅绝对值,避免 12M 负数时比率反向上分

### 修复
- 行业分类关键词规则完善(避免长尾 ETF 误归类)

### 实战案例
- **光伏 v4.1** — 雷达分 8.71(第 1),关注池 爱旭股份(BC)+ 大全能源(多晶硅价格触底)
- **AI v4.1** — 雷达分 8.30(第 2),方向:算力 / 模型 / 应用三层
- **储能/碳中和 v4.1** — 雷达分 8.18(第 3),方向:大储 / 工商业储能 / 户储 + 逆变器 + 电池
- **机器人/智造 v4.1** — 雷达分 7.96(第 4),方向:减速器 / 丝杠 / 伺服 / 传感器

---

## [v4.0] - 2026-07-06 · ★ 兑现度筛选段(chain-settlement · P0)

### 新增
- **chain-settlement**(7.5 段 · P0) · 在 stockmap 候选清单上做 4 象限兑现度筛选
  - 评分公式:`S = 0.6 × Ps(股价兑现) + 0.4 × Pf(业绩兑现)`
  - 4 象限分类:Q1 同行抢筹(警惕追高)/ Q2 兑现期(规避)/ Q3 价值洼地(关注池 ★)/ Q4 潜伏(观察池)
  - 兑现度反例:fund_flow > 1 亿(60 日)+ 涨幅 < 行业基准 + Pf ≥ 6 = 资金已埋伏但股价未涨
  - 脚本 `fetch_settlement_data.py` + `calc_settlement_score.py` + `gen_settlement_report.py`
  - 数据源:东财 push2his K线 + AKShare 季度财务 + Tushare DuckDB 行业 ETF(只读)+ 东财 60 日主力净流入
  - 实战样本:`chain-stockmap/examples/robot-case/`(机器人产业链)
  - **数据访问加固**: `_ReadOnlyDuckDB` 类 + `duckdb.connect(DB_PATH, read_only=True)` + SQL 审计日志

### 实战案例
- **机器人 v4.0** — 关注池 Q3:鸣志电器(S=5.99)+ 汇川技术(S=5.87)
- 警惕池 Q1:绿的谐波 +314% / 埃斯顿 +143% / 奥普特 +76% / 恒立液压 +77%
- Q4 观察池:秦川机床(业绩未兑现)

---

## [v3.4] - 2026-07-03 · 产业链图视觉升级

### 新增
- Bootstrap Icons v1.x 实心版 19 个图标(MIT · CDN 自动缓存)
- 径向彩色光圈 + 立体描边阴影(参考 Apple Keynote 风格)
- 替换原 emoji 图标,提升专业感

### 修复
- chain-chip-design 模板统一设计语言

---

## [v3.3] - 2026-07-03 · 产业链图系统升级

### 新增
- 产业链图生成系统升级为 PIL + cairosvg 高保真版(替代 mermaid)
- 18 个 SVG 图标库(`chain-chip-design/scripts/icon_lib.py`)
- chain-chip-design/SKILL.md 沉淀设计语言 + 复用模板

---

## [v3.2] - 2026-07-02 · ★ 工艺路线子段(chain-chip-design)

### 新增
- **chain-chip-design**(2.5 段 · 可选) · 半导体/光芯片/化合物半导体的工艺路线拆解
  - device physics 拆解 + 衬底选型 + 良率爬升曲线 + 下一代路径
  - 内嵌 HTML mermaid.js 产业链图,每环节标 A 股龙头
  - 模板 + 双案例:光模块 + EML 国产替代
- 工具链:`draw_chain.py` + `draw_chain_v2.py` + `icon_lib.py`

### 实战案例
- **光模块 v3.2** — 11 只 A 股已核验 ★
- **EML 国产替代 v3.2** — 3 只 A 股已核验 ★

---

## [v3.1] - 2026-07-02 · ★ 格式选择卡(末段交付)

### 新增
- 「格式选择卡」末段交付(report.md → HTML / DOCX 二选一交互卡)
- HTML 单文件 + DOCX pandoc 双格式输出
- CardKit 2.0 schema(已发飞书用户确认)

---

## [v3.0] - 2026-07-02 · ★ 周期段(chain-cycle) + 三角定位法

### 新增
- **chain-cycle**(第 4 段 · 可选 · 强周期行业必跑)
  - 6 类周期指标(能繁母猪 / PPI / 价格 / 库存 / 产能利用率 / 信贷)
  - 拐点预测 + 16 种组合矩阵评级表
- 「周期 × 缺口 × 政策」**三角定位法**(本 skill 扩展)
  - 三轴评分:周期位置(0-10)/ 缺口类型(0-10)/ 政策环境(0-10)
  - 综合公式:`R = 0.3 × 周期 + 0.4 × 缺口 + 0.3 × 政策`
- chain-breakdown 增加「周期位置」列
- chain-verify 增加「周期触发矩阵」

### 实战案例
- **猪肉 v3.0** — 完整 8 段样本(强周期 + chain-cycle 必跑)
- **创新药 v3.0** — 完整 8 段样本(政策 + 出海 + chain-cycle)

---

## [v2.0] - 2026-07-02 · ★ 选股段(chain-stockmap)

### 新增
- **chain-stockmap**(第 8 段) · 把 chain-analysis 的「价值量定位」映射到 A 股/港股/美股
- 4 维评分:价值量 30% / 财务 25% / 估值 20% / 技术 25%
- 多市场支持:A 股(腾讯/新浪)+ 港股 + 美股
- 脚本 `fetch_stock.py` + `fetch_a_stock.py` + `fetch_hk_stock.py` + `fetch_us_stock.py`
- 「行动方案」表(借鉴 invest · 风险管理)

### 实战案例
- **氟化工 v2.0** — 完整 7 段样本(弱周期 · 周期×缺口×政策 = 7.7 → ★★★★)
  - 三角定位:上升周期(7)+ 国产替代(10)+ 中性政策(5) → 7.7

---

## [v1.0] - 2026-07-01 · 初版 6 段对齐架构

### 新增
- 借鉴「齐码.SKILL」6 段对齐架构
- 借鉴 harrischen/invest 多因子评分 + 选股落地
- 借鉴 zhangmusinb/gushifenxi-skill 口径拆分 + 三端拆解 + 数据状态分层
- 5 段核心:chain-idea → chain-data → chain-breakdown → chain-analysis → chain-report → chain-verify
- 7 个模板:`templates/*.md.template`

---

## 📊 版本路线图(2026 Q3)

| 版本 | 计划 |
|---|---|
| v4.2 | fetch_stock.py 接港股 18A API(已有 fetch_hk_stock.py 待完善) |
| v4.3 | LLM-driven 周期拐点预测 |
| v4.4 | 多产业链横向对比矩阵(同时跑 5 个行业) |
| v4.5 | 跟踪指标自动监控(飞书 webhook) |
| v5.0 | PDF 输出(weasyprint / wkhtmltopdf) |

---

## 🔗 实战案例库(`examples/`)

| 案例 | 行业 | 雷达分 | 段数 | 路径 |
|---|---|---|---|---|
| 光伏 | 新能源 | 8.71(★ 第 1) | 10 段 | `examples/pv-case/` |
| AI | 计算机 | 8.30(★ 第 2) | 10 段 | `examples/ai-case/` |
| 机器人 | 智造 | 7.96(★ 第 4) | 10 段 | `examples/robot-case/` |
| 氟化工 | 化工 | - | 7 段 | `examples/fluorine-case/` |
| 猪肉 | 农业(强周期) | - | 8 段 + cycle | `examples/pig-case/` |
| 创新药 | 医药 | - | 8 段 + 出海 | `examples/innovative-drug-case/` |
| AI-HBM | 计算机 | - | 7 段(简化) | `examples/ai-hbm-chain/` |

---

*Generated by industry-chain-research skill · 维护者 Claude(阿超投资助理)*
