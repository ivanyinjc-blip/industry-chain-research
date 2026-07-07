---
name: chain-report
description: 产业链研究第 5 段 · 研报骨架。把 4 段累积的输出,组织成可读的研报。激活时机:chain-analysis 输出 analysis.md 后。
---

---

## 📋 SKILL 契约(6 字段 · agent 调用入口)

> 完整的 报告渲染 段契约。Claude/Codex 调用本段时,只需读这一节。

### 🎯 触发条件

- 前序段:chain-stockmap 已产 `08_stockmap.md`

### 📥 输入文件

- 必填:`01-08` 全部产物
- 可选:用户偏好(目标读者:散户/机构/内部)

### 📤 输出文件

- `final_report.md`(完整报告)
- `final_report.svg`(可选,产业链图)
- 飞书交互卡(2 选 1 格式)

### 🔑 必填字段

- 完整 8/9 段对齐
- 三角定位法总结
- 飞书交互卡(必出)

### ✅ 验收清单

- [ ] 报告包含完整 8/9 段引用
- [ ] 飞书交互卡可正常渲染
- [ ] 包含 1-2 个反证条件
- [ ] 跟踪清单与 chain-verify 一致

### ⚠️ 失败处理

- 前序产物不全 → 警告,强制跑全流程
- 飞书卡渲染失败 → 退化为纯 markdown

---
# chain-report · 研报骨架段

> 灵感:大刘《齐码.SKILL》vibe-prototype 段
> 产物:`report.md`(研报初稿) + 可选 `report.html` / `report.docx`(排版版)
> 输入:前面 4 段的全部产物
> 输出:研报骨架,等待 chain-verify 校验

## 🎯 这个 skill 干什么

把"立项卡片 + 数据卡 + 拆分卡 + 分析卡"**组装成一篇可读的研报**。

不是堆数据,而是用**结构化叙事**让人愿意读完。

## 🧠 核心方法论:研报 5 段叙事

一篇产业链研报,标准骨架:

```
1. 开场 · 30 秒抓住人
   "过去 3 年 XX 行业最值得关注的变化是 X,本文将回答 3 个问题:Y/Z/W"
   ↓
2. 拆链 · 上中下游怎么切
   "我们将这条链拆为 3 个环节,本节给整体框架"
   ↓
3. 聚焦 · Top 3 环节深挖
   "3 个环节中,真正吸金的是 A,我们用三层价值量解剖它"
   ↓
4. 验证 · 供需与传导
   "看供需缺口 + 跨环节传导,验证我们的判断"
   ↓
5. 结论 · 给读者可行动的话
   "如果你是 X,你应该 Y;如果 Z 数据出现,请重新评估"
```

## 📐 11 词 · 在叙事中的体现

研报中每个 11 词,**至少出现一次**(作为小标题或重点标注):

| 词 | 研报中的位置 |
|---|---|
| navigate | 第 2 段 · 下游主战场 |
| modal | 第 3 段 · 最大风险点 |
| confirm | 第 4 段 · 增量来源 |
| drawer | 第 3 段 · 隐藏成本 |
| popover | 第 3 段 · 差异化卖点 |
| bottomsheet | 第 4 段 · 底部反转 |
| toast | 第 5 段 · 短期跟踪 |
| inline-expand | 第 3 段 · 价值量分布 |
| inline-edit | 第 3 段 · 成本变化 |
| newtab | 第 4 段 · 跨行业新需求 |
| download | 附录 · 数据来源 |

## 🛡 数据状态强制分层(借鉴 gushifenxi)

**每张表格的每一行,都必须标"数据状态"**——这是研究的诚实度底线:

| 数据状态 | 含义 | 何时用 |
|---|---|---|
| **已核验** | 来自公司公告/年报/招股书/官方数据 | 当作事实使用 |
| **估算** | 基于公开数据的推算,需进一步核验 | 注明估算方法 + 来源 |
| **市场预期** | 来自券商研报/媒体,尚未兑现 | 标注"市场预期口径" |
| **待查证** | 没有可靠来源 | 明确写"待查证" |

**信息来源优先级**(借鉴 gushifenxi):
1. 公司公告/年报/季报/交易所披露(可信度:高)
2. 公司官网/投资者关系/新闻稿(可信度:中高)
3. 行业协会/权威行业报告/券商研报(可信度:中)
4. 主流财经媒体/产业媒体(可信度:中)
5. 自媒体/论坛传闻(可信度:低)→ 只写"线索,需交叉验证"

## 🛠 工作流(可执行版)

```
输入: idea.md + data.md + breakdown.md + analysis.md
  ↓
[Step 1: 提取核心结论]
  从 analysis.md 提取 Top 3 环节的"价值量定位"
  ↓
[Step 2: 5 段叙事组装]
  按 5 段叙事模板组装
  ↓
[Step 3: 数据回填]
  把 data.md 中的关键数字,填到对应段落(标注来源)
  ↓
[Step 4: 反证条件前置]
  在每段结论后,挂上反证条件
  ↓
[Step 5: 排版版本生成]
  report.md → report.html / report.docx
  ↓
[Step 6: 输出到 chain-verify]
```

## 📄 report.md 输出模板

```markdown
# [项目名] · 产业链研究报告

> 立项:idea.md | 数据:data.md | 拆分:breakdown.md | 分析:analysis.md
> 报告生成:YYYY-MM-DD  | 报告版本:v0.1(待 verify)

---

## 摘要
[3 段,每段 50 字]
- 一句话定义研究边界
- 3 个核心结论(每个 Top 1 环节一句)
- 1 个最大风险点

---

## 1. 开场 · 为什么研究这个
### 1.1 3 个具体问题
1. [问题 1 — 来自 idea.md § 1.3]
2. [问题 2]
3. [问题 3]

### 1.2 我们的回答
1. ...
2. ...
3. ...

---

## 2. 拆链 · 整体框架
### 2.1 上中下游全景
[图 + 表,来自 data.md § 1]

### 2.2 三层价值量总览
[图,来自 analysis.md 全部环节的"价值量定位"]

---

## 3. 聚焦 · Top 3 环节深挖

### 3.1 环节 A · [环节名](价值集聚/壁垒/颠覆)
#### 3.1.1 成本层
[来自 analysis § 1.1]

#### 3.1.2 利润层
[来自 analysis § 1.2]

#### 3.1.3 瓶颈层
[来自 analysis § 1.3]

#### 3.1.4 差异化卖点(popover)
[具体数据,来自 analysis § 1.2]

#### 3.1.5 隐藏成本(drawer)
[具体数据,来自 analysis § 1.1]

#### 3.1.6 成本变化(inline-edit)
[3 年变化,来自 analysis § 1.1]

#### 3.1.7 价值量分布(inline-expand)
[百分比分布,来自 analysis § 1.5]

### 3.2 环节 B
(同上结构)

### 3.3 环节 C
(同上结构)

---

## 4. 验证 · 供需与传导

### 4.1 供需验证
[来自 analysis § 1.4,Top 3 环节逐个]

### 4.2 跨环节传导
[来自 analysis 末节]

### 4.3 增量来源(confirm)
[已确认/可能/未知 — 来自 data.md § 11 词]

### 4.4 底部反转信号(bottomsheet)
[具体信号 + 历史可重复性]

---

## 5. 结论 · 可行动的话
### 5.1 给三类读者的建议
- 给投资者:[具体动作]
- 给从业者:[具体动作]
- 给研究者:[待继续研究的问题]

### 5.2 短期跟踪事件(toast)
[3 个近期需要关注的事件/数据点]

### 5.3 跨行业新需求(newtab)
[新的需求场景,具体体量]

---

## 附录 A · 数据来源(download)
[来自 data.md § 11 词 download]

## 附录 B · 反证条件汇总
[从 breakdown + analysis 汇总所有反证条件]

## 附录 C · 术语表
[专业术语解释]

---

> 待 chain-verify 校验 · 进入核销清单
```

## 🚦 何时启用

- chain-analysis 完成 analysis.md 后,自动进入
- chain-verify 上游缺失 report.md
- 用户要求"先出研报初稿"

## ⚠️ 红线

- ❌ 不准 5 段叙事缺一段 — 这是经过验证的叙事结构
- ❌ 不准"反证条件"不挂 — 反证是研报的诚实度底线
- ❌ 不准 11 词全部缺位 — 否则是产业链研究的标准缺失
- ❌ 不准结论超过 5 条 — 重点不突出 = 没结论
- ❌ 不准表格缺"数据状态"列 — 数据状态是研报的可信度底线

## 🔗 与上下游的契约

- **上游**:前 4 段产物全部
- **下游(chain-verify)**:report.md 的"反证条件汇总" + "结论" → 是核销基线

## 🧰 推荐排版工具

```bash
# Markdown → HTML
python -m markdown report.md > report.html

# Markdown → DOCX
pandoc report.md -o report.docx

# 自定义主题(参考 weekly-review-style)
# 主题:极简 / 学术 / 投资风
```

---

## 🚀 末段交付 · 格式选择卡(本 skill 扩展 · v3 升级)

**这是 chain-report 段的最后一步** — 让用户用交互卡选择 HTML / DOCX 输出格式。

### 设计背景

传统研究报告输出痛点:
| 场景 | 痛点 | 本 skill 解法 |
|---|---|---|
| 微信/飞书转发 | Word 格式在手机上排版混乱 | **HTML 单文件 + 内嵌 CSS**(自适应) |
| 邮件正式投递 | HTML 在 Outlook/邮箱客户端支持差 | **DOCX**(pandoc 生成) |
| 打印 / 归档 | HTML 不适合打印 | **DOCX** |
| 屏幕阅读 | DOCX 在飞书卡片里只显示文件名 | **HTML 渲染卡** |

### 工作流(在 chain-report 输出 report.md 后执行)

```
[Step 5: report.md 已生成]
  ↓
[Step 6: 构造格式选择卡]
  运行:python3 scripts/send_format_card.py <chat_id> <report.md> <名称>
  ↓
[Step 7: lark-cli 发送选择卡到当前 chat]
  cat <card.json> | lark-cli im send-card --chat-id <id> --card -
  ↓
[Step 8: 等待用户点击]
  用户点 HTML → 收到 [card-click] {format: "html", ...}
  用户点 DOCX → 收到 [card-click] {format: "docx", ...}
  ↓
[Step 9: Claude 根据 format 执行渲染]
  format=html → python3 scripts/render_report.py <md> <out.html> html
  format=docx → python3 scripts/render_report.py <md> <out.docx> docx
  ↓
[Step 10: 把生成的文件回传给用户]
  HTML:作为飞书文件消息发送(用户可点击预览 + 下载)
  DOCX:作为飞书文件消息发送
```

### 选择卡结构(CardKit 2.0)

```json
{
  "schema": "2.0",
  "header": {
    "title": {"tag": "plain_text", "content": "📄 报告生成 · <报告名>"},
    "template": "blue"
  },
  "body": {
    "elements": [
      {
        "tag": "div",
        "text": {
          "tag": "lark_md",
          "content": "**报告文件**:`<path>`\n**报告大小**:X KB\n\n请选择输出格式:"
        }
      },
      {"tag": "hr"},
      {
        "tag": "action",
        "actions": [
          {
            "tag": "button",
            "text": {"tag": "plain_text", "content": "📄 生成 HTML(推荐 · 易读可转发)"},
            "type": "primary",
            "value": {
              "__bridge_cb": true,
              "bridge_token": "<SIGNED_TOKEN>",
              "format": "html",
              "report_path": "<path>",
              "report_name": "<name>",
              "chat_id": "<chat_id>",
              "action": "render_report"
            }
          },
          {
            "tag": "button",
            "text": {"tag": "plain_text", "content": "📝 生成 Word(DOCX · 适合正式投递)"},
            "type": "default",
            "value": {
              "__bridge_cb": true,
              "bridge_token": "<SIGNED_TOKEN>",
              "format": "docx",
              "report_path": "<path>",
              "report_name": "<name>",
              "chat_id": "<chat_id>",
              "action": "render_report"
            }
          }
        ]
      },
      {
        "tag": "div",
        "text": {
          "tag": "lark_md",
          "content": "💡 **HTML**:单文件 + 内嵌 CSS,微信/飞书/邮件直接转发\n💡 **DOCX**:pandoc 生成,适合打印或正式邮件附件"
        }
      }
    ]
  }
}
```

### Claude 处理 `[card-click]` 回调的标准动作

```python
# 收到类似:[card-click] {"format": "html", "report_path": "/tmp/.../report.md", ...}

# 1. 校验 bridge_token(由 bridge 自动完成)
# 2. 提取 format / report_path / report_name / chat_id
# 3. 调用 render_report.py
import subprocess
report_name = data["report_name"]
fmt = data["format"]  # html / docx
output_ext = "html" if fmt == "html" else "docx"
output_path = f"/tmp/{report_name}.{output_ext}"

result = subprocess.run([
    "python3", 
    "/home/ivanyinjc/.claude/skills/industry-chain-research/chain-report/scripts/render_report.py",
    data["report_path"],
    output_path,
    fmt
], capture_output=True, text=True)

# 4. 把生成的文件用 lark-cli im upload 发送回 chat
# lark-cli im upload --chat-id <id> --file <output_path>
# 然后回复用户:"✅ HTML 报告已生成(11.7 KB),点击查看"
```

### HTML 渲染特性(借鉴 weekly-review-style 极简学术风)

- **响应式布局**:max-width 960px,手机/桌面自适应
- **数据状态徽章**:自动识别 `**已核验**` → 绿色徽章 / `**估算**` → 黄色徽章 / `**待查证**` → 红色徽章
- **评分星级高亮**:★★★★★ 自动着色
- **表格美化**:斑马纹 + hover 高亮 + 表头蓝色
- **反证框**:红色边框突出
- **跟踪清单框**:黄色边框突出
- **元信息框**:蓝色渐变 + 项目名 / 数据源 / 评级
- **页脚**:自动签名 + 生成时间

### DOCX 渲染特性(pandoc)

- 默认 pandoc markdown → docx
- 可选 `--reference-doc=reference.docx` 自定义 Word 样式
- 适合打印 / 邮件附件 / 正式投递

### 🚦 何时启用

- chain-report 完成 report.md 后,**必须** 触发格式选择卡
- 用户明确要求"出 Word 版"/"出 HTML 版"/"出 PDF 版"
- 用户在群聊里 @ 你 + 「给我看下报告」

### ⚠️ 红线

- ❌ 不要跳过选择卡,直接渲染一种格式 — 用户选择权是体验底线
- ❌ 不要在选择卡里塞私货(广告 / 无关推荐)— 卡片只承载 2 个按钮
- ❌ 不要忘记校验 bridge_token — 防止伪造回调
- ❌ 不要把 .html 文件作为附件发 — 直接用飞书卡片预览(HTML 渲染)
- ❌ DOCX 必须 pandoc 生成,不要用 python-docx(样式太丑)

### 🔗 与上下游的契约

- **上游**:chain-report 的 report.md → 选择卡的输入
- **下游**:用户点击 → Claude 渲染 → 文件回传 → 用户接收
- **下游(chain-verify)**:如用户在卡片后追加"再核销一遍",仍走 chain-verify 段

## 🧰 推荐工具

```bash
# 1. 生成格式选择卡 JSON
python3 scripts/send_format_card.py <chat_id> <report.md> "报告名"

# 2. 用 lark-cli 发送卡片
cat <card.json> | lark-cli im send-card --chat-id <chat_id> --card -

# 3. 收到 [card-click] 后渲染
python3 scripts/render_report.py <report.md> <output.html> html
# 或
python3 scripts/render_report.py <report.md> <output.docx> docx

# 4. 把文件回传给用户
lark-cli im upload --chat-id <chat_id> --file <output.html>
```

---

## 📊 完整 8 段 pipeline 闭环(创新药链 · 实际跑通案例)

```
chain-idea       →  idea.md       (118 行 · 三问法 + 11 词 + 四度评分 30/40)
  ↓
chain-data       →  data.md       (132 行 · 上中下游 24 家公司)
  ↓
chain-breakdown  →  breakdown.md  (95 行 · 4 维评分 + Top 4 环节)
  ↓
chain-cycle      →  cycle.md      (157 行 · 政策+出海+技术+资金 四周期叠加 + 6 RC)
  ↓
chain-analysis   →  analysis.md   (304 行 · Top 4 三层价值量深挖)
  ↓
chain-report     →  report.md     (75 行 · 5 段叙事 + 数据状态分层)
  ↓                    ↓
                   [格式选择卡]   ←  ★ 本段新增 v3
                   /            \
                  ↓              ↓
              HTML(11.7 KB)   DOCX(pandoc)
                  ↓              ↓
                  └──────┬───────┘
                         ↓
chain-verify    →  verify.md     (135 行 · 5 类核销 + 月度跟踪)
  ↓
chain-stockmap   →  stockmap.md   (299 行 · 13 只 A 股全核验)
```

**新增闭环**:在 chain-report 末尾,用户用交互卡选择格式,Claude 在同一会话里渲染并回传文件,真正实现"研究 → 报告 → 交付"的端到端自动化。
