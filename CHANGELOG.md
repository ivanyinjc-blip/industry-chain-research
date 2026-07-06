# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.1.0] - 2026-07-06 · ★ 行业雷达段(第 0 段)

### Added · 新增
- ★ **chain-radar 行业雷达**(第 0 段) · 基于 1,561 只被动指数型 ETF 的「景气 × 趋势 × 拥挤反向」三轴评分
  - 三轴评分:景气 12M (40%) / 趋势 6M (30%) / 拥挤反向 1M (30%)
  - 评级映射:★★★★★ R≥7.5 + 12M>5% | ★★★★ R≥6.5 | ★★★ R≥5.0 | ★★ R<5.0 或 12M<-10%
  - SKILL.md(方法论 + 14 个重点行业)
  - scripts/fetch_radar_data.py(DuckDB 只读扫描 1,561 只 ETF)
  - scripts/calc_radar_score.py(三轴评分 + 评级映射)
  - scripts/gen_radar_report.py(出 Markdown 报告)
  - examples/radar-2026-07-06/(2026-07-06 扫描样本:光伏 8.71 · AI 8.30 · 储能 8.18 · 机器人 7.96)
- ★ **数据访问加固**(沿用 v4.0):`_ReadOnlyDuckDB` + `duckdb.connect(DB_PATH, read_only=True)` + SQL 审计日志
- ★ **总纲升级**:`SKILL.md` 加 chain-radar 第 0 段,9 段对齐架构图更新
- **实战案例**:光伏 v4.1(雷达分 8.71 · 第 1)+ AI v4.1(雷达分 8.30 · 第 2)+ 储能 v4.1 + 机器人 v4.1

### Fixed · 修复
- **趋势分 v1 语义错误 → v2 修复**:v1 用 6M/12M 比率作为趋势分,12M 为负时比率反向上分(医药 -2% / -5.85% = 2.84 → 趋势分 8.5 → 排第一,违反直觉)
  - v2 修复:趋势分改为 6M 涨幅**绝对值**,直接看绝对涨幅
  - 关键洞察:当 12M 是负数时,任何比率计算都会反向,必须用绝对值

### Verified · 实战验证
- 扫描样本 1,561 只 ETF · 14 个重点行业 · 250 交易日窗口
- 推荐研究 Top 4:光伏 / AI / 储能 / 机器人
- 输出文件:radar.md(评分卡) + radar_scores.json(评分数据) + radar_raw.json(原始数据)

## [4.0.0] - 2026-07-06 · ★ 兑现度筛选段(chain-settlement · P0)

### Added · 新增
- ★ **chain-settlement**(7.5 段 · P0) · 在 stockmap 候选清单上做 4 象限兑现度筛选
  - 评分公式:`S = 0.6 × Ps(股价兑现) + 0.4 × Pf(业绩兑现)`
  - 4 象限分类:Q1 同行抢筹(警惕追高)/ Q2 兑现期(规避)/ Q3 价值洼地(关注池 ★)/ Q4 潜伏(观察池)
  - SKILL.md 增加「chain-settlement 子段」章节
  - scripts/fetch_settlement_data.py(K线 + 季报 + 资金流 + 行业 ETF)
  - scripts/calc_settlement_score.py(评分算法 + 4 象限分类)
  - scripts/gen_settlement_report.py(出 Markdown 报告)
  - templates/settlement.md.template
  - examples/robot-case/settlement.md + settlement_data.json + settlement_scores.json
- ★ **数据访问加固**:`_ReadOnlyDuckDB` 类强制只读 + 审计日志
  - DuckDB 引擎层只读:`duckdb.connect(DB_PATH, read_only=True)`
  - SQL 审计:每次 exit 打印 `[DuckDB-AUDIT] 本次发起 N 个 SELECT,无可写操作`
  - 零依赖 `local_api.py` 是否被改
  - 拒绝操作:`INSERT` / `UPDATE` / `CREATE` / `DELETE` / `ATTACH`

### Verified · 实战验证(机器人产业链)
- **关注池(Q3 价值洼地)**:鸣志电器(603728, S=5.99)+ 汇川技术(300124, S=5.87)
- **警惕池(Q1 已充分兑现)**:绿的谐波 +314% / 埃斯顿 +143% / 奥普特 +76% / 恒立液压 +77% 等 7 只
- **Q4 观察池**:秦川机床(业绩未兑现)

### Changed · 升级
- **SKILL.md 升级**:chain-stockmap 段加 settlement 子段
- **8+1 段对齐 → 8+2 段对齐**:8 段 + chain-settlement 7.5 段 + chain-stockmap 8 段
- 数据源:东财 push2his(直调)+ AKShare 季度财务 + Tushare DuckDB(只读)+ 东财 60 日主力净流入

## [3.1.0] - 2026-07-02

### Added · 新增
- ★ **格式选择卡(末段交互式交付)**:CardKit 2.0 交互卡,用户二选一 HTML / DOCX
- ★ **HTML 报告渲染器**:`chain-report/scripts/render_report.py`(内嵌 CSS · 响应式 · 数据状态徽章)
- ★ **格式选择卡生成器**:`chain-report/scripts/send_format_card.py`
- **创新药产业链完整案例**:`examples/innovative-drug-case/`(政策 + 出海 + 8 段)

### Changed · 升级
- **fetch_a_stock.py v3**:finance 改用东方财富 datacenter `RPT_F10_FINANCE_MAINFINADATA`(完整 4 季度财务)
- **fund_flow 修复**:AKShare 需带 `market` 参数才能正确返回
- **SKILL.md 总纲升级到 v3.1**:新增 ★ 格式选择卡节点

### Verified · 实战验证
- **氟化工案例** v3:多氟多 4.43 / 巨化股份 4.16 强烈推荐(移除退市股 600636)
- **猪肉案例** v3:科前生物 4.35 唯一强烈推荐(财务数据塌方 → 8 只中 7 亏 1 微赚)
- **创新药案例** v1:纳微 / 药明 / 恒瑞 / 键凯 4 只强烈推荐(PE 10.44 罕见低估)
- **85 个真实 API 调用** 全部 OK(4 接口 × 21 只股票)



## [3.4.0] - 2026-07-03

### Added · 新增
- ★ **icon_lib 升级到 Bootstrap Icons v1.x**:`chain-chip-design/scripts/icon_lib.py`(MIT license · 19 个图标 · 自动下载 + 本地缓存 `~/.cache/bootstrap-icons/`)
- ★ **径向彩色光圈**:`draw_icon_circle` 新增 18 圈同心圆径向渐变(中心 alpha 0x70 → 边缘 alpha 0x10)
- ★ **立体描边阴影**:深色描边 + 浅灰阴影,模拟参考图的"凸起实心"质感
- ★ **设计语言沉淀**:chain-chip-design/SKILL.md 新增 Bootstrap Icons 映射说明 + 升级理由

### Changed · 升级
- **icon_lib.py 重写**:从 19 个自画几何 SVG → 19 个 Bootstrap Icons fill 版(cpu-fill / motherboard-fill / cloud-fill / robot ...)
- **draw_icon_circle 重构**:白色圆 + 单一图标 → 描边阴影 + 径向光圈 + 大号白色实心图标
- **cdn.jsdelivr.net 取代 raw.githubusercontent.com**:GitHub raw 限速问题解
- **SKILL.md 升级到 v3.4**:总纲新增 v3.4 行 + 演进路线

### Tested · 验证
- optical-module-v5c.png (239 KB · 19 个 Bootstrap 图标全部生效)
- eml-substitution-v5.png (218 KB · 中下游光圈效果显著)
- 用户确认接受"立体实心"风格

## [3.3.0] - 2026-07-03

## [3.2.0] - 2026-07-02

### Added · 新增
- ★ **chain-chip-design 模块**(第 2.5 段 · 工艺路线分析段):device physics 拆解 + 5 钻探针(工艺 + 衬底 + 设备 + 下一代 + 良率)
  - SKILL.md(方法论 + 适用场景)
  - templates/chip-design.md.template(7 个章节模板)
  - scripts/draw_chain.py(mermaid.js 内嵌 HTML 产业链图生成器)
  - examples/eml-25g/ + examples/eml-route/(EML 工艺路线卡片)
- ★ **产业链全景图生成器**:draw_chain.py 支持 4 种图(光模块全景 / EML 国产替代链 / 工艺分代路线 / 国产化 Gantt 时间表),每张图每个环节标注 A 股龙头
- ★ **光模块产业链实战案例**:`examples/optical-module-case/`(8 段全跑,11 只 A 股已核验 · 含产业链图)
- ★ **EML 国产替代深度案例**:`examples/eml-substitution-case/`(8 段全跑,3 只 A 股已核验 · 源杰 +1153% YoY 实证 5-20% 阶段)

### Changed · 升级
- **SKILL.md 升级到 v3.2**:**8+1 段对齐**(原 8 段 + 新增 chain-chip-design 2.5 段)
- 模块表新增行 2.5:`chain-chip-design`(半导体/光芯片/化合物半导体必跑)
- 演进路线新增 `v3.2 (2026-07-02)`
- 案例列表新增:`optical-module-case` / `eml-substitution-case`

### Tested · 验证
- 85+ API 真实调用 × 14 只 A 股已核验(光模块 11 + EML 3 + 长光)
- 关键数据:源杰科技 2026Q1 YoY 净利 **+1153%** + 毛利率 **77.81%**(超国际同行)
- 4 张产业链图用 mermaid.js v10.9 CDN 渲染验证

## [3.0.0] - 2026-07-02

### Added · 新增
- **8 段对齐 pipeline**:idea → data → breakdown → cycle → analysis → report → verify → stockmap
- ★ **chain-cycle 周期段**:6 类周期指标 + 拐点预测(强周期行业必跑)
- ★ **「周期 × 缺口 × 政策」三角定位法**:16 种组合矩阵评级表
- ★ **周期触发矩阵(RC)**:6 类触发器 + 反向风险监控
- ★ **国产替代 5 阶段模型**:0-5% → 5-20% → 20-50% 加速 → 50%+
- **多因子评分**:趋势 30% + 资金 30% + 情绪 20% + 周期 10% + 板块 10%
- **AKShare + 东方财富 push2 + datacenter 真实数据接入**
- **5 层数据状态分层**:已核验 / 估算 / 市场预期 / 待查证 / 不可得

### Examples · 案例
- **氟化工案例** v1(`examples/fluorine-case/`):弱周期 7 段
- **猪肉案例** v1(`examples/pig-case/`):强周期 8 段 ★ 标杆

## [2.0.0] - 2026-07-02

### Added · 新增
- **7 段对齐 pipeline**:在《齐码.SKILL》6 段基础上 + chain-stockmap
- **三类缺口分类**:瓶颈型 / 增量型 / 国产替代型
- **借鉴 harrischen/invest**:多因子评分 + 微笑曲线 + 利润转移
- **借鉴 gushifenxi**:口径拆分 + 三端拆解 + 数据状态分层

## [1.0.0] - 2026-07-01

### Added · 新增
- **6 段对齐架构**:基于《齐码.SKILL》Design-by-Contract
- **11 词法**:navigate / modal / confirm / drawer / popover / bottomsheet / toast / inline-expand / inline-edit / newtab / download
- **四度评分**:流变重构 / 成本坍缩 / 人即环境 / 可验证黑盒

[4.1.0]: https://github.com/ivanyinjc-blip/industry-chain-research/releases/tag/v4.1.0
[4.0.0]: https://github.com/ivanyinjc-blip/industry-chain-research/releases/tag/v4.0.0
[3.4.0]: https://github.com/ivanyinjc-blip/industry-chain-research/releases/tag/v3.4.0
[3.3.0]: https://github.com/ivanyinjc-blip/industry-chain-research/releases/tag/v3.3.0
[3.2.0]: https://github.com/ivanyinjc-blip/industry-chain-research/releases/tag/v3.2.0
[3.1.0]: https://github.com/ivanyinjc-blip/industry-chain-research/releases/tag/v3.1.0
[3.0.0]: https://github.com/ivanyinjc-blip/industry-chain-research/releases/tag/v3.0.0
[2.0.0]: https://github.com/ivanyinjc-blip/industry-chain-research/releases/tag/v2.0.0
[1.0.0]: https://github.com/ivanyinjc-blip/industry-chain-research/releases/tag/v1.0.0