# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[3.1.0]: https://github.com/ivanyinjc-blip/industry-chain-research/releases/tag/v3.1.0
[3.0.0]: https://github.com/ivanyinjc-blip/industry-chain-research/releases/tag/v3.0.0
[2.0.0]: https://github.com/ivanyinjc-blip/industry-chain-research/releases/tag/v2.0.0
[1.0.0]: https://github.com/ivanyinjc-blip/industry-chain-research/releases/tag/v1.0.0
