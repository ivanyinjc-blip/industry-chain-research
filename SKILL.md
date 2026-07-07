---
name: industry-chain-research
description: |
  产业链深度研究 9 段对齐 skill(2026-07-06 v4.1:在 8+1 之前加 chain-radar 行业雷达)。
  基于「齐码.SKILL」Design-by-Contract 思想 + harrischen/invest 多因子评分
  + zhangmusinb/gushifenxi 深度研究方法,形成「周期 × 缺口 × 政策」三角定位法。
  每段输入=上段产物,实现"结论=证据"的全链路对齐。
  包含三层价值量(成本/利润/瓶颈)、三类缺口(瓶颈/增量/国产替代/新需求)、
  反证条件、跟踪指标。聚焦 A 股 + 港股 + 美股产业链投研。
---

# 产业链深度研究 Skill · 9 段对齐(2026-07-06 v4.1 升级:新增 chain-radar)

> **作者**:Claude(阿超投资助理) · **适用**:A 股 / 港股 / 美股产业链投研(二级市场视角)
> **完整 SKILL 列表**:见各 `chain-*/SKILL.md`(每段 20-40 行结构化契约)

---

## 🎯 解决什么

| 痛点 | 解法 | 触发段 |
|---|---|---|
| 想法飘忽 | chain-idea 口径拆分 + 三问法 | ① |
| 数据散乱 | chain-data 三端拆解 + 11 词 | ② |
| 环节说不清 | chain-breakdown 三类缺口 + 周期位置 | ③ |
| 缺周期判断 | chain-cycle 周期类型 + 拐点 | ④ |
| 工艺路线复杂(半导体) | chain-chip-design 工艺 + 良率 | ②.5(可选) |
| 缺反证 | chain-verify 反证前置 | ⑥ |
| 结论不稳定 | 「周期 × 缺口 × 政策」三角定位 | ⑤ |
| 不知道研究哪个行业 | **chain-radar**(v4.1 新增)三轴扫 1,561 ETF | 0 |
| 选出 10 只不知哪只已兑现 | chain-settlement 4 象限分类 | ⑦.5 |

---

## 📐 9 段对齐架构

```
       ┌──────────────────┐
       │  chain-radar     │ 0 行业雷达(可选入口)
       │  (v4.1 新增)     │   「景气 × 趋势 × 拥挤度」三轴
       └────────┬─────────┘
                ▼
       ┌──────────────────┐
       │  chain-idea      │ ① 口径拆分 + 周期/政策前置
       └────────┬─────────┘
                ▼
       ┌──────────────────┐
       │  chain-data      │ ② 上中下游 + 三端 + 11 词
       └────────┬─────────┘
                ▼
       ┌─────────────────────┐
       │ chain-chip-design   │ ②.5 工艺路线 + 良率(半导体/光芯片必跑)
       │ (可选)              │
       └────────┬────────────┘
                ▼
       ┌─────────────────────┐
       │ chain-breakdown     │ ③ 4 维评分 + 三类缺口 + 周期位置
       └────────┬────────────┘
                ▼
       ┌─────────────────────┐
       │ chain-cycle         │ ④ 周期类型 + 阶段 + 拐点(强周期必跑)
       └────────┬────────────┘
                ▼
       ┌─────────────────────┐
       │ chain-analysis      │ ⑤ 三层价值量 + 微笑曲线 + 利润转移
       └────────┬────────────┘
                ▼
       ┌─────────────────────┐
       │ chain-verify        │ ⑥ 反证条件 + 触发矩阵
       └────────┬────────────┘
                ▼
       ┌─────────────────────┐
       │ chain-settlement    │ ⑦.5 兑现度筛选(4 象限分类)★ v4 P0
       └────────┬────────────┘
                ▼
       ┌─────────────────────┐
       │ chain-stockmap      │ ⑧ 选股清单 + 评分 + 跟踪
       └────────┬────────────┘
                ▼
       ┌─────────────────────┐
       │ chain-report        │ ⑨ 报告渲染 + 交互卡
       └─────────────────────┘
```

---

## 📋 每段 SKILL 契约(统一 6 字段)

每段都是独立的"可执行合同",agent 调用时**只需读对应 chain-*/SKILL.md**:

| 段 | 文件 | 一句话 |
|---|---|---|
| 0 | [chain-radar/SKILL.md](chain-radar/SKILL.md) | 三轴评分扫 ETF,筛 Top 行业 |
| ① | [chain-idea/SKILL.md](chain-idea/SKILL.md) | 口径拆分 + 周期/政策前置 |
| ② | [chain-data/SKILL.md](chain-data/SKILL.md) | 上中下游 + 三端数据 + 11 词 |
| ②.5 | [chain-chip-design/SKILL.md](chain-chip-design/SKILL.md) | 工艺 + 良率(可选,半导体必跑) |
| ③ | [chain-breakdown/SKILL.md](chain-breakdown/SKILL.md) | 4 维评分 + 三类缺口 + 周期位置 |
| ④ | [chain-cycle/SKILL.md](chain-cycle/SKILL.md) | 周期类型 + 阶段 + 拐点 |
| ⑤ | [chain-analysis/SKILL.md](chain-analysis/SKILL.md) | 三层价值量 + 微笑曲线 + 利润转移 |
| ⑥ | [chain-verify/SKILL.md](chain-verify/SKILL.md) | 反证条件 + 触发矩阵 |
| ⑦.5 | [chain-stockmap/SKILL.md](chain-stockmap/SKILL.md) | settlement 子段(4 象限分类) |
| ⑧ | [chain-stockmap/SKILL.md](chain-stockmap/SKILL.md) | 选股清单 + 评分 + 跟踪 |
| ⑨ | [chain-report/SKILL.md](chain-report/SKILL.md) | 报告渲染 + 交互卡 |

**每段都按 6 字段写**:触发条件 / 输入文件 / 输出文件 / 必填字段 / 验收清单 / 失败处理。

---

## 🚀 一键使用

### 安装

```bash
git clone https://github.com/ivanyinjc-blip/industry-chain-research
cd industry-chain-research
bash setup.sh      # Linux/macOS
# 或 .\setup.ps1   # Windows
```

### 调用

```bash
# 全流程:从想法到选股清单
make run-radar      # 0 段:扫 ETF
make run-stockmap   # ⑧ 段:选股清单
make run-report     # ⑨ 段:报告渲染
```

### 测试

```bash
make test    # 25+ 用例
make lint    # ruff 检查
```

---

## 📁 项目结构

```
industry-chain-research/
├── chain-radar/          # 0 段
├── chain-idea/           # 1 段
├── chain-data/           # 2 段
├── chain-chip-design/    # 2.5 段(可选)
├── chain-breakdown/      # 3 段
├── chain-cycle/          # 4 段
├── chain-analysis/       # 5 段
├── chain-verify/         # 6 段
├── chain-stockmap/       # 7.5 + 8 段
├── chain-report/         # 9 段
├── docs/
│   ├── data-fields.md    # 字段元数据
│   ├── setup.md          # 跨平台配置
│   └── releases/         # 版本历史
├── tests/                # 25+ 用例
├── examples/             # 完整样本
├── requirements.txt
├── pyproject.toml
├── Makefile
├── setup.sh              # Linux/macOS
├── setup.ps1             # Windows
└── SKILL.md              # 本文件(总纲)
```

---

## 🆚 版本历史

- **v4.1.1** (2026-07-07) — ★ Industrialization:字段校验、跨平台配置、测试、CI、SKILL 模板
- **v4.1.0** (2026-07-06) — ★ 新增 chain-radar(行业雷达)第 0 段
- **v4.0.0** (2026-07-06) — ★ 新增 chain-settlement 7.5 段(兑现度筛选)
- **v3.0.0** (2026-07-02) — 8 段(新增 chain-cycle)+ 三角定位法
- **v2.0.0** (2026-07-02) — 7 段 + 借鉴落地
- **v1.0.0** — 初版

---

## 📚 借鉴来源

| 来源 | 借鉴内容 |
|---|---|
| 「爱AI的大刘」《齐码.SKILL》(2026-06) | 6 段对齐架构 + Design-by-Contract 思想 |
| [harrischen/invest](https://github.com/harrischen/invest) | 多因子评分 + 选股落地 |
| [zhangmusinb/gushifenxi-skill](https://github.com/zhangmusinb-dotcom/gushifenxi-skill) | 口径拆分 + 三层价值量 + 数据状态 |

**本 skill 的扩展**:
- 「周期 × 缺口 × 政策」三角定位法
- chain-cycle 周期段(强周期行业必跑)
- 16 种组合矩阵评级表
- chain-breakdown 周期位置列
- chain-verify 周期触发矩阵
- chain-stockmap 周期评分因子
- chain-radar ETF 三轴扫描
- chain-settlement 4 象限兑现度筛选
- chain-chip-design 工艺路线子段 + 良率爬升

---

## ⚖️ License

MIT
