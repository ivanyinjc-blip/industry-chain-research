---
name: chain-verify
description: 产业链研究第 6 段 · 核销清单。把研报所有判断,转成可核销的任务。激活时机:chain-report 输出 report.md 后。
---

# chain-verify · 核销清单段

> 灵感:大刘《齐码.SKILL》vibe-implement 段
> 产物:`verify.md`(核销清单) + `tracking/` 目录(跟踪表)
> 输入:report.md + 前 4 段产物
> 输出:可执行的核销清单 + 持续跟踪机制

## 🎯 这个 skill 干什么

把研报里的所有"判断、断言、预估、承诺",**转成可勾选的核销任务**。

研究报告最大的问题不是"写错",而是"写完没人跟进"。chain-verify 解决这个。

## 🧠 核心方法论:核销清单 = 纪律

核销清单包含 5 类条目,每类都有"必填字段":

### 类 1 · 反证条件(最高优先级)
来自:breakdown + analysis
字段:触发条件 / 检测方式 / 触发后动作 / 负责人

### 类 2 · 待补数据
来自:data.md § 不可得数据
字段:数据点 / 期望来源 / 截止日期

### 类 3 · 短期跟踪事件
来自:report.md § toast + newtab
字段:事件名 / 预期日期 / 影响判断

### 类 4 · 长期假设(待证伪)
来自:report.md § 结论 + 11 词
字段:假设 / 证伪条件 / 验证周期

### 类 5 · 读者行动项
来自:report.md § 5.1
字段:行动 / 触发条件 / 期望产出

## 📐 11 词 · 在核销的体现

| 词 | 核销项类型 |
|---|---|
| navigate | 类 3 · 下游需求数据跟踪 |
| modal | 类 1 · 风险点监测 |
| confirm | 类 1 · 增量来源验证 |
| drawer | 类 4 · 隐藏成本变化 |
| popover | 类 4 · 差异化卖点可持续性 |
| bottomsheet | 类 1 · 底部反转信号 |
| toast | 类 3 · 短期跟踪事件 |
| inline-expand | 类 4 · 价值量分布变化 |
| inline-edit | 类 4 · 成本结构变化 |
| newtab | 类 3 · 跨行业新需求 |
| download | 类 2 · 待补数据 |

每个词,**至少 1 个核销项**。

## 🛠 工作流(可执行版)

```
输入: report.md + 前 4 段产物
  ↓
[Step 1: 提取所有判断/断言/预估]
  从 report.md 全文提取
  ↓
[Step 2: 分类]
  按 5 类分入核销清单
  ↓
[Step 3: 字段补全]
  每类按必填字段补全(允许"未指定"占位)
  ↓
[Step 4: 优先级排序]
  反证条件 > 短期跟踪 > 待补数据 > 长期假设 > 读者行动项
  ↓
[Step 5: 跟踪表初始化]
  创建 tracking/ 目录,放 tracking.md 跟踪表
  ↓
[Step 6: 输出 verify.md]
```

## 📄 verify.md 输出模板

```markdown
# [项目名] · 核销清单

> 报告:report.md v0.1
> 核销生成:YYYY-MM-DD
> 下次评审:YYYY-MM-DD(默认 30 天后)

---

## 优先级 · P0 · 反证条件(最高优先)

### RC-1 · [反证条件名]
- 来自:breakdown § 2.1 / analysis § 1.6
- 触发条件:[具体数字/事件]
- 检测方式:[数据源 + 频率]
- 触发后动作:[重新评估某环节 / 修正结论 / 撤回报告]
- 负责人:[未指定]
- 状态:🟡 监控中

### RC-2 · ...
(同上结构)

---

## 优先级 · P1 · 短期跟踪事件

### TT-1 · [事件名]
- 来自:report § 5.2 / data § 11 词 toast
- 预期日期:YYYY-MM-DD
- 影响判断:[对哪个结论有影响]
- 检测方式:[公告 / 数据发布]
- 状态:🟡 等待中

---

## 优先级 · P2 · 待补数据

### MD-1 · [数据名]
- 来自:data.md § 4 不可得数据
- 数据点:[具体想要什么]
- 期望来源:[哪个机构/渠道]
- 截止日期:YYYY-MM-DD
- 状态:🔴 未启动

---

## 优先级 · P3 · 长期假设(待证伪)

### LH-1 · [假设名]
- 来自:report § 5.1 / data § 11 词
- 假设内容:[用一句话描述]
- 证伪条件:[什么数据/事件出现,假设被推翻]
- 验证周期:[每月 / 每季度 / 每年]
- 状态:🟡 监控中

---

## 优先级 · P4 · 读者行动项

### RA-1 · [行动名]
- 来自:report § 5.1
- 行动:[具体做什么]
- 触发条件:[什么时候执行]
- 期望产出:[可衡量的产出]
- 状态:🔴 待启动

---

## 跟踪表

### 状态图例
- 🟢 已核销
- 🟡 监控中
- 🔴 待启动 / 未启动
- ⚪ 已撤销(原条件失效)

### 月度核销节奏
- 每月 1 日:更新 TT(短期跟踪事件)
- 每月 15 日:更新 RC(反证条件)
- 每季度:更新 LH(长期假设)
- 每半年:更新 MD(待补数据)
```

## 📁 tracking/ 目录约定

```
tracking/
├── verify.md           # 主核销清单
├── 2026-08-01.md      # 月度更新日志(模板)
└── README.md           # 跟踪表使用说明
```

## 🚦 何时启用

- chain-report 完成 report.md 后,自动进入
- 用户要求"建跟踪表"
- 报告发布 30 天后,做第一次核销

## ⚠️ 红线

- ❌ 不准反证条件不挂优先级 — 没优先级就是全部拖
- ❌ 不准待补数据"无截止日期" — 没截止就是永远不做
- ❌ 不准长期假设"无证伪条件" — 不能证伪的假设是信仰
- ❌ 不准核销清单 > 50 条 — 多了就不是清单是噪音

## 🔗 与上下游的契约

- **上游(chain-report)**:report.md 所有"判断" → 是核销项的来源
- **上游(chain-analysis)**:analysis.md "反证条件" → 是 P0 输入
- **上游(chain-breakdown)**:breakdown.md "反证条件" → 是 P0 输入
- **下游**:研究报告完成 → 但核销清单永远在演进

## 🧰 推荐跟踪工具

```python
# 核销状态机
class VerifyItem:
    def __init__(self, code, content, priority, source):
        self.code = code
        self.content = content
        self.priority = priority  # P0/P1/P2/P3/P4
        self.source = source
        self.status = "🔴 未启动"
        self.history = []
    
    def mark_monitor(self):
        self.status = "🟡 监控中"
        self.history.append(("monitor", now()))
    
    def mark_verified(self, evidence):
        self.status = "🟢 已核销"
        self.history.append(("verified", now(), evidence))
    
    def mark_revoked(self, reason):
        self.status = "⚪ 已撤销"
        self.history.append(("revoked", now(), reason))
```

## 🔁 闭环

```
chain-verify → 月度评审 → 触发新一轮研究?
                ↓
            触发条件:
            1. P0 反证条件被触发 → 立即更新报告
            2. 多个 P3 假设同时被证伪 → 重新立项
            3. P2 待补数据被获取 → 补强原报告
```

核销清单 = 研究的"动态性"。报告不是死的,核销清单让研究**永远在更新**。
