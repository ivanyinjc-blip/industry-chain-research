---
name: chain-chip-design
description: 产业链研究 chip-design 子段 · 深度工艺路线分析。聚焦半导体/光芯片/光模块等需要工艺拆解的产业链,从制程角度分析国产替代窗口、瓶颈环节、技术代际差距。激活时机:研究含芯片/晶圆/光芯片/光模块/化合物半导体的产业链时,在 chain-data 之后、chain-breakdown 之前调用。
---

---

## 📋 SKILL 契约(6 字段 · agent 调用入口)

> 完整的 工艺路线(可选) 段契约。Claude/Codex 调用本段时,只需读这一节。

### 🎯 触发条件

- 研究对象是半导体 / 光芯片 / MEMS 等工艺复杂行业
- 前序段:chain-data 已产 `02_data.md`

### 📥 输入文件

- 必填:`02_data.md` 中的工艺相关数据
- 可选:晶圆厂 roadmap 公开文件

### 📤 输出文件

- `02.5_chip_design.md`(工艺路线图)
- 可选:`chip_design.svg`(链图)

### 🔑 必填字段

- 工艺节点(28nm/14nm/7nm)
- 衬底/设备清单
- 良率爬升曲线
- 关键瓶颈环节

### ✅ 验收清单

- [ ] 工艺节点有公开依据(白皮书/财报)
- [ ] 良率数据有来源
- [ ] 与 chain-data 中的数据一致
- [ ] 输出可被 chain-breakdown 引用

### ⚠️ 失败处理

- 工艺不公开(商业机密)→ 标注"行业惯例 X nm"
- 良率数据缺失 → 仅给工艺路线,不给良率

---
# chain-chip-design · 工艺路线分析段

> 灵感:从 device physics 角度拆解「能否国产替代」+「技术代际差距」+「工艺路线的拐点」
> 产物:`chip-design.md`(工艺路线卡片)+ 可选 `chip-design-diagram.html`(可视化)
> 输入:链 data.md(尤其是上游设备/材料/工艺 list)
> 输出:可被 chain-breakdown 直接消费的 chip-design.md

## 🎯 这个 skill 干什么

在标准 9 段 pipeline 的 data → breakdown 之间,插入一个 **device physics 拆解段**(可选)。

普通研报只看「上下游有哪些公司」,**这个段告诉你**:
- 这条工艺路线上,**具体哪一道工序是卡脖子点?**
- 国产化进度在 **device level** 是几分?
- 下一代(50G/100G/200G)用什么新工艺?量子点、硅光异质集成、InP-on-Si?
- **工艺拐点**(良率 50% → 70%)预期何时?

## 🧠 核心方法论:五钻探针

| 维度 | 做什么 | 关键问题 |
|---|---|---|
| **工艺路线** | 主流量产工艺是什么 | MOCVD / MBE / 湿法刻蚀 / 干法刻蚀 哪种是主流? |
| **衬底** | 哪类 wafer 是基础 | InP / Si / GaAs / GaN / 蓝宝石 哪种? 国产率? |
| **设备** | 关键设备供应商 | MOCVD 国产率?测试设备国产率? |
| **下一代** | 工艺路线的 2-3 代后再突破 | 50G EML → 100G EML → 200G 异质集成 → 量子点 EML? |
| **良率** | 当前良率水平 + 突破时点 | 25G EML 良率?什么时候能 70%? |

## 📐 应用场景

| 产业链 | 关键 chip-design 内容 |
|---|---|
| **光模块** | EML 工艺路线 + InP 衬底 + MOCVD 设备 + 硅光集成 |
| **存储/半导体** | NAND/NOR flash 制程 + 光刻机 + 国产化 |
| **化合物半导体** | GaN on Si / GaAs / InP 工艺路线 |
| **锂电材料** | 隔膜 + 电解液 + 正极材料工艺 |
| **创新药** | ADC linker + 双抗 + GLP-1 工艺路线 |

## 📊 产出模板(chip-design.md)

```markdown
# [产业链名] · chip-design 工艺路线卡片

## 0. 一句话结论
[这条工艺路线的核心卡点 + 国产窗口期一句话]

## 1. 工艺拓扑
### 1.1 主流量产工艺
| 工艺 | 主流用途 | 国产率 | 关键设备 | A 股标的 |
|---|---|---|---|---|

### 1.2 衬底 + 设备
| 衬底 | 主流尺寸 | 国产率 | 关键厂 |
|---|---|---|---|

### 1.3 工艺路线分代
- **第 1 代(2020)**:25G EML on 3-inch InP
- **第 2 代(2024)**:25G/50G EML on 4-inch InP
- **第 3 代(2026)**:50G/100G EML on 6-inch InP
- **第 4 代(2028)**:200G 硅光异质集成 / 量子点 EML

## 2. 良率爬升路径
[从 30% → 70% 的时点 + 关键事件]

## 3. 下一代工艺路线
- 50G → 100G 的具体突破点
- 200G 异质集成路径
- 量子点 EML 路线

## 4. 关键设备国产化
- MOCVD
- 测试设备(DCA, OSA)
- 光刻机

## 5. 与下游的契约
- **给 chain-breakdown**: 工艺路线 + 良率基线 + 卡点明细
- **给 chain-stockmap**: device-level 国产化率 + 公司卡位
```

## 🌟 核心创新 (五大法宝)

### ① 工艺分代(3 generations ahead)
不只看当前代,要看到 2-3 代后的工艺拐点。
**A 股特别适用**:科技自立自强是 5-10 年国策,需要看清楚每代工艺对应的国产窗口期。

### ② 衬底独立性分析
衬底是工艺的根(InP / Si / GaAs),大部分产业链的真正卡点在衬底。
- InP 衬底 Sumitomo/JEPIX 占 90%+
- Si 衬底中国 12 寸已突破
- GaAs 衬底中国 IVT/云南锗业突破

### ③ 良率爬升路线图
**良率 50% → 70% 是商用化的关键拐点**。这是 device physics 的硬约束。
- 25G EML:2025 良率 50% → 2026Q1 70%(源杰已过)
- 50G EML:2026 良率 <30% → 2026 H2 突破 50%
- 100G EML:2026 概念验证 → 2027 突破 70%

### ④ 异质集成 vs 分立器件
**长期路线**:分立 EML → 硅光异质集成 → 量子点 EML
- 分立 EML:2026 主流(国产正在替代)
- 硅光异质集成:2027-2028 突破(Intel 主导)
- 量子点 EML:2028+ 概念阶段

### ⑤ 五钻探针(5 dimensions)
- 工艺 + 衬底 + 设备 + 下一代 + 良率
- **device-level 国产化** vs **工艺级卡点**

## 🚦 何时启用

- chain-data 上游有设备/材料 list,需要 device-level 拆分
- chain-breakdown 写不出"哪道工序是卡脖子"
- 用户问"XX 光芯片能不能做""XX 材料工艺差距"
- 强周期行业的工艺代际分析

## ⚠️ 红线

- ❌ 不准只看当前代 — 必须看到 2-3 代后的工艺路线
- ❌ 不准忽略衬底 — 90% 卡点在衬底,不在器件本身
- ❌ 不准用「差不多」描述良率 — 必须给出当前具体数字
- ❌ 不准假设工艺路线单一 — 必须列出 2-3 条 parallel 路径

## 🔗 与上下游的契约

- **给 chain-breakdown**: 工艺路线表 + 良率基线 + 卡点明细
- **给 chain-stockmap**: device-level 国产化率 + 公司工艺卡位 + 量价齐升预测

---

## 🖼️ 产业链图生成系统(PIL · 高保真 · 2026-07-03 升级)

> 用户对 v3 的视觉风格已认可(16:9, #0B3A82 标题, 三栏布局, 蓝绿配色)。本节沉淀为可复用技能。

### 设计语言(Design Tokens)

```
画布      :1920×1080 (16:9)
背景      :#FFFFFF 纯白
标题色    :#0B3A82  深蓝
副标题    :#6B7B91  灰
主蓝      :#2F80ED  / 深蓝 #1E5BB8
青色辅    :#00B8D9
下游绿    :#22C55E  / 深绿 #16A34A
卡片底    :#FAFBFD  / 绿色 #F0FDF4
卡片描边  :#E6EDF5  1px
介绍框    :#EFF6FF  + #BFDBFE 边
圆角      :6-8 px
字体      :WenQuanYi Micro Hei(macOS/Linux 一致)
```

### 三栏布局(主图通用)

```
┌──────────┬──────────┬──────────┐
│  上游蓝  │  中游蓝  │  下游绿  │
│  ──────  │  ──────  │  ──────  │
│  卡片×N  │  步骤×N  │  卡片×N  │
│  龙头×N  │  龙头×N  │  龙头×N  │
└──────────┴──────────┴──────────┘
     ┌──── intro 介绍框(蓝色 light)────┐
     ┌──── 总结 ────┬──── 投资要点 ────┬── QR ──┐
```

### 文件结构

```
chain-chip-design/
├── SKILL.md                           ← 本文件
├── scripts/
│   ├── icon_lib.py                    ← 19 个 Bootstrap Icons 实心版(MIT · CDN 自动缓存)
│   └── draw_chain_v2.py               ← 主图生成器(PIL + 立体光圈)
└── templates/
    └── chip-design.md.template
```

### icon_lib.py(19 个 Bootstrap Icons 实心版 · v3.4 升级)

**v3.4 重要升级**:从自画几何 SVG 改为 Bootstrap Icons v1.x(MIT license · 2000+ 图标 · 实心 fill 版)。

跨平台一致 + 自动下载 + 本地缓存(`~/.cache/bootstrap-icons/`)。
完全替代 emoji,接近 Fluent 2 实心风的视觉冲击力。

```python
from icon_lib import icon_svg, ICON_NAMES, EMOJI_TO_ICON

# 单个图标
svg_str = icon_svg('chip', size=32, color='#2F80ED')

# 列出所有图标名(19 个)
print(ICON_NAMES)
# ['chip', 'pcb', 'optic', 'housing', 'fiber', 'material',
#  'flow', 'doc', 'design', 'components', 'integrate', 'test', 'ship',
#  'datacenter', 'telecom', 'cloud', 'ai', 'arrow_right', 'check']

# emoji → 图标映射(用于旧代码兼容)
EMOJI_TO_ICON = {
    '💡': 'fiber', '🔬': 'optic', '🧩': 'pcb',
    '🖥️': 'datacenter', '📡': 'telecom', '☁️': 'cloud', '🤖': 'ai',
    ...
}
```

图标清单(19 个 · Bootstrap Icons 映射):
- **设备类**:chip→cpu-fill, pcb→motherboard-fill, housing→box-seam-fill, fiber→hdd-stack-fill, material→stack
- **光学类**:optic→optical-audio-fill
- **流程类**:flow→diagram-3-fill, doc→file-earmark-text-fill, design→easel-fill, components→puzzle-fill, integrate→diagram-3-fill, test→beaker-fill, ship→truck
- **场景类**:datacenter→hdd-rack-fill, telecom→broadcast, cloud→cloud-fill, ai→robot
- **辅助类**:arrow_right→arrow-right, check→check-circle-fill

**为什么从自画 SVG 升级到 Bootstrap Icons**
1. 视觉更接近参考图(实心 + 立体)而不是工程师风(描边 + 几何)
2. 2000+ 现成图标覆盖所有产业链节点,不需要每个新链都手画
3. MIT 商用免费 · 跨平台一致 · 像素级 sharp

### draw_chain_v2.py(主图生成器)

**PIL + cairosvg 混合方案**:
- PIL 画布 + 文字 + 渐变 header + 阴影卡片
- cairosvg 渲染 SVG 图标 → 字节 → PIL paste

**两种预设模式**:

```bash
# 光模块产业链全景图
python3 draw_chain_v2.py optical_module /tmp/out/optical.png

# EML 国产替代产业链
python3 draw_chain_v2.py eml_substitution /tmp/out/eml.png
```

**核心 API**:

```python
# 设计系统(DS dict)— 修改一处全局生效
DS = {
    'W': 1920, 'H': 1080, 'bg': '#FFFFFF',
    'title_color': '#0B3A82', 'title_size': 44,
    'blue': '#2F80ED', 'blue_dark': '#1E5BB8',
    'cyan': '#00B8D9', 'green': '#22C55E', 'green_dark': '#16A34A',
    ...
}

# 主函数签名
def build_optical_module(out_path: str):
    """生成光模块产业链全景图:三栏 + 介绍框 + 总结 + 投资要点"""

def build_eml_substitution(out_path: str):
    """生成 EML 国产替代产业链图:衬底 → 芯片 → 模块(红色卡脖子高亮)"""
```

**辅助函数**:

```python
font(size)                                  # 中文字体对象
svg_to_pil(svg_str, size)                   # SVG → PIL Image
draw_gradient_header(d, x, y, w, h, c1, c2) # 水平渐变 header
draw_shadow_card(d, x, y, w, h, r=6)        # 阴影卡片
draw_shadow_card_green(d, x, y, w, h, r=6)  # 绿色阴影卡片
draw_shadow_card_red(d, x, y, w, h, r=6)    # 红色卡脖子卡片
draw_icon_circle(im, d, x, y, size, name, c)# 圆形图标 + 立体光圈(径向渐变 + 白色实心)
card_template(im, d, x, y, w, h, icon, name, desc, stocks, color)
                                            # 通用卡片(上游/下游)
```

### 复用步骤(给其他产业链)

1. **复制 `draw_chain_v2.py`** 为 `draw_<your_chain>.py`
2. **修改 DS 字典**(配色,字体大小)
3. **写 `build_<your_chain>(out_path)`** 函数,顺序调用辅助函数
4. **准备数据 list**:`(icon, name, desc, stocks)`
5. **跑**:`python3 draw_<your_chain>.py <output.png>`

### 故障排查

| 症状 | 原因 | 解法 |
|---|---|---|
| 中文显示 □□ | 字体路径错 | 确认 `/home/ivanyinjc/.fonts/wqy-microhei.ttc` 存在 |
| `ModuleNotFoundError: cairosvg` | pip 装错 venv | 用 `/home/ivanyinjc/.local/share/pipx/venvs/hermes-agent/bin/python` |
| `AttributeError: NoneType.paste` | 漏传 Image | `draw_icon_circle(im, ...)` 第一个参数不能是 None |
| SVG 解析报 not well-formed | 文本含 `&` | 调用前 `re.sub(r'&(?!(amp;\|lt;\|gt;)', '&amp;', text)` |
| PNG < 100 KB | 中文 fallback | 检查字体加载是否成功 |

