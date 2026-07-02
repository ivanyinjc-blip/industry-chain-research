#!/usr/bin/env python3
"""
chain-chip-design/scripts/draw_chain.py
产业链图 + 工艺路线图生成器(HTML 内嵌 mermaid.js,飞书/微信转发即看)

用法:
  python3 draw_chain.py <mode> <output.html>
  mode in [chain_eml, chain_module, route_eml, all_in_one]

输出:单文件 HTML,内嵌 mermaid.js CDN + 自定义主题
"""
import sys
import os
from pathlib import Path
from datetime import datetime


# ========== mermaid 源码 ==========

MERMAID_CHAIN_MODULE = """
flowchart TB
    %% 光模块产业链全景图
    subgraph 上游[上游 · 光芯片 + 电芯片 + 器件]
        direction TB
        L1[EML 25G/50G/100G 光芯片<br/>★ 国产替代 10-15%]
        L2[VCSEL 850nm 短距<br/>国产 30-50%]
        L3[CW Laser 50G 连续波<br/>国产 5-10%]
        L4[高速 PCB M6/M7<br/>国产 40%]
        L5[外壳 + 套管<br/>国产 >90%]
        L1_company[源杰 688498<br/>长光华芯 688048<br/>仕佳光子 688313]
        L2_company[纵慧芯光<br/>长光华芯]
        L3_company[源杰 688498<br/>仕佳光子 688313]
        L4_company[生益科技 600183<br/>沪电股份 002463]
        L5_company[太辰光 300570]
    end

    subgraph 中游[中游 · 光模块组装 ★ 规模壁垒]
        direction TB
        M1[800G 数通模块<br/>⭐ 全球 1]
        M2[1.6T 数通模块<br/>⭐ 商业化元年]
        M3[电信模块<br/>稳态]
        M4[相干模块 200G+]
        M1_company[中际旭创 300308<br/>新易盛 300502<br/>华工科技 000988]
        M2_company[中际旭创 300308<br/>新易盛 300502]
        M3_company[光迅科技 002281<br/>中兴通讯 000063]
        M4_company[中际旭创 + 光迅<br/>新易盛]
    end

    subgraph 下游[下游 · 应用场景]
        direction TB
        D1[北美超大规模数据中心<br/>⭐ MSFT/GOOG/META]
        D2[国内云厂商<br/>阿里/腾讯/字节/百度]
        D3[电信运营商<br/>移动/电信/联通]
        D4[卫星激光通信<br/>⭐ 新需求]
    end

    L1 --> M1
    L1 --> M2
    L2 --> M1
    L3 --> M1
    L4 --> M1
    L4 --> M2
    L5 --> M1
    L5 --> M2
    L1_company -.-> L1
    L2_company -.-> L2
    L3_company -.-> L3
    L4_company -.-> L4
    L5_company -.-> L5

    M1 --> D1
    M2 --> D1
    M3 --> D3
    M4 --> D2
    D4 --> M1
    M1_company -.-> M1
    M2_company -.-> M2
    M3_company -.-> M3
    M4_company -.-> M4

    classDef upstream fill:#ffe5e5,stroke:#cc0000,stroke-width:2px
    classDef midstream fill:#fff4e5,stroke:#ff8800,stroke-width:3px
    classDef downstream fill:#e5f0ff,stroke:#0066cc,stroke-width:2px
    classDef gold fill:#fff9c4,stroke:#f57f17,stroke-width:3px

    class L1,L2,L3,L4,L5,L1_company,L2_company,L3_company,L4_company,L5_company upstream
    class M1,M2,M3,M4,M1_company,M2_company,M3_company,M4_company midstream
    class D1,D2,D3,D4 downstream
    class M1,M2 gold
"""

MERMAID_CHAIN_EML = """
flowchart TB
    %% EML 国产替代产业链
    subgraph InP[上游 · 衬底 + 设备 + 工艺]
        direction TB
        S1[磷化铟 InP 衬底<br/>2/3/4 英寸<br/>国产 5-10%]
        S2[MOCVD 设备<br/>金属有机化学气相沉积<br/>国产 <5%]
        S3[外延片生长<br/>InP-based MQW<br/>国产 30%+]
        S1_company[北京通美晶体 未上市<br/>中科晶电]
        S2_company[中微公司 688012<br/>北方华创 002371]
        S3_company[源杰 内部自研<br/>长光华芯]
    end

    subgraph CHIP[中游 · EML 芯片 ★ 卡脖子]
        direction TB
        C1[25G EML<br/>⭐ 5-20% 加速 ★]
        C2[50G EML<br/>⭐ 验证期(送样)]
        C3[100G EML<br/>概念验证]
        C4[CW Laser 25G<br/>⭐ 5-10%]
        C1_company[⭐ 源杰 688498 ★★<br/>长光华芯 688048]
        C2_company[源杰 688498<br/>长光华芯 688048]
        C3_company[源杰 内部研发]
        C4_company[仕佳光子 688313<br/>源杰 688498]
    end

    subgraph DOWN[下游 · 模块厂客户]
        direction TB
        U1[800G 模块<br/>4 颗 EML/只]
        U2[1.6T 模块<br/>8 颗 EML/只]
        U1_company[中际旭创 300308<br/>新易盛 300502<br/>Coherent COHR]
        U2_company[中际旭创 300308<br/>新易盛 300502]
    end

    S1 --> S3
    S2 --> S3
    S3 --> C1
    S3 --> C2
    S3 --> C4
    S1_company -.-> S1
    S2_company -.-> S2
    S3_company -.-> S3

    C1 --> U1
    C2 --> U1
    C2 --> U2
    C4 --> U1
    C1_company -.-> C1
    C2_company -.-> C2
    C3_company -.-> C3
    C4_company -.-> C4

    U1 --> U1_company
    U2 --> U2_company

    classDef upstream fill:#ffe5e5,stroke:#cc0000,stroke-width:2px
    classDef midstream fill:#fff4e5,stroke:#ff8800,stroke-width:3px
    classDef downstream fill:#e5f0ff,stroke:#0066cc,stroke-width:2px
    classDef gold fill:#fff9c4,stroke:#f57f17,stroke-width:4px
    classDef critical fill:#ffcdd2,stroke:#b71c1c,stroke-width:4px

    class S1,S2,S3,S1_company,S2_company,S3_company upstream
    class C1,C2,C3,C4,C1_company,C2_company,C3_company,C4_company midstream
    class U1,U2,U1_company,U2_company downstream
    class C1_company,C1 gold
    class S1 critical
"""

MERMAID_ROUTE_EML = """
flowchart LR
    %% EML 工艺路线分代图(2-3 代 ahead)
    G1[第 1 代 2020<br/>25G EML on 3-inch InP<br/>国产 0-5%<br/>★ 验证期]
    G2[第 2 代 2024<br/>25G/50G EML on 4-inch InP<br/>国产 5-15%<br/>★★★ 加速 ★]
    G3[第 3 代 2026<br/>⭐ 50G/100G EML on 6-inch InP<br/>国产 15-30%<br/>★★★★★ 主流]
    G4[第 4 代 2028<br/>200G 硅光异质集成<br/>+ 量子点 EML<br/>★★★★ 研发]

    G1 -->|2024 突破| G2
    G2 -->|2026 H2 良率 70%| G3
    G3 -->|2027 突破| G4

    G3 -.->|国产对标| Target[源杰 50G 验证 ★]
    G3 -.->|海外压制| Suppress[Lumentum<br/>三菱 + 住友<br/>占 90%+]
    G4 -.->|下一代卡位| Future[Intel 硅光<br/>TFLN 量子点]

    classDef gen1 fill:#e1f5ff,stroke:#01579b
    classDef gen2 fill:#b3e5fc,stroke:#0277bd
    classDef gen3 fill:#fff9c4,stroke:#f57f17,stroke-width:4px
    classDef gen4 fill:#ffe0b2,stroke:#e65100,stroke-width:3px

    class G1 gen1
    class G2 gen2
    class G3 gen3
    class G4 gen4
"""

MERMAID_GANTT = """
gantt
    title EML 国产化时间表(2024-2028)
    dateFormat YYYY-MM
    axisFormat %Y-%m

    section 衬底 + 设备
    InP 衬底国产化(5-15%)           :active, s1, 2024-01, 2026-12
    InP 衬底国产化突破(30%)         : s2, 2027-01, 2028-06
    MOCVD 设备(InP)                : s3, 2025-06, 2027-12

    section 25G EML(已突破)
    25G EML 良率 70%               :done, crit, m1, 2024-01, 2026-06
    25G EML 国产化 30%             : m2, 2024-01, 2027-06

    section 50G EML(进行中)
    50G EML 送样验证               :active, crit, m3, 2026-01, 2026-12
    50G EML 良率 50%               : m4, 2026-09, 2027-06
    50G EML 量产突破               : m5, 2027-06, 2028-06

    section 100G EML(研发)
    100G EML 概念验证               : m6, 2026-06, 2027-12
    100G EML 良率 50%              : m7, 2027-12, 2028-12

    section 200G 异质集成(远期)
    硅光异质集成突破                : m8, 2027-01, 2029-06
    量子点 EML 概念                 : m9, 2028-01, 2029-12
"""


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.0/dist/mermaid.min.js"></script>
<style>
:root {{
  --primary: #1f4e79;
  --secondary: #2e75b6;
  --bg: #fafbfc;
  --text: #1a1a1a;
  --border: #e1e4e8;
  --gold: #f57f17;
  --critical: #b71c1c;
}}
* {{ box-sizing: border-box; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
  line-height: 1.7;
  color: var(--text);
  background: var(--bg);
  max-width: 1100px;
  margin: 0 auto;
  padding: 40px 24px 80px;
}}
h1, h2, h3 {{ color: var(--primary); margin-top: 1.5em; }}
h1 {{
  font-size: 2em;
  border-bottom: 3px solid var(--primary);
  padding-bottom: 12px;
}}
h2 {{
  font-size: 1.5em;
  border-bottom: 1px solid var(--border);
  padding-bottom: 6px;
}}
.legend {{
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  margin: 24px 0;
  padding: 16px;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 6px;
}}
.legend-item {{
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9em;
}}
.legend-color {{
  width: 24px;
  height: 24px;
  border-radius: 4px;
}}
.diagram-block {{
  margin: 32px 0;
  padding: 24px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}}
.diagram-block h3 {{
  margin-top: 0;
  font-size: 1.3em;
  color: var(--primary);
  border-bottom: 2px solid var(--secondary);
  padding-bottom: 8px;
}}
.mermaid {{
  text-align: center;
  font-size: 16px;
}}
.meta {{
  font-size: 0.85em;
  color: #777;
  margin-top: 12px;
}}
.summary {{
  background: linear-gradient(135deg, #f0f7ff, #fff9c4);
  border-left: 4px solid var(--gold);
  padding: 16px;
  border-radius: 0 4px 4px 0;
  margin: 20px 0;
}}
</style>
</head>
<body>

<h1>{title}</h1>
<p class="meta">📅 生成时间:{date} | 工具:chain-chip-design/draw_chain.py | 数据来源:industry-chain-research skill v3.1</p>

<div class="summary">
<h3>🎯 这张图回答的问题</h3>
<p>{summary}</p>
</div>

<div class="legend">
  <div class="legend-item"><div class="legend-color" style="background:#ffe5e5;border:2px solid #cc0000"></div>上游(衬底/设备/材料)</div>
  <div class="legend-item"><div class="legend-color" style="background:#fff4e5;border:2px solid #ff8800"></div>中游(制造/芯片)</div>
  <div class="legend-item"><div class="legend-color" style="background:#e5f0ff;border:2px solid #0066cc"></div>下游(模块/客户)</div>
  <div class="legend-item"><div class="legend-color" style="background:#fff9c4;border:3px solid #f57f17"></div>⭐ 强烈推荐标的</div>
  <div class="legend-item"><div class="legend-color" style="background:#ffcdd2;border:3px solid #b71c1c"></div>★ 关键卡脖子</div>
</div>

{blocks}

<script>
mermaid.initialize({{
  startOnLoad: true,
  theme: 'default',
  flowchart: {{ curve: 'basis', padding: 20 }},
  themeVariables: {{
    fontSize: '14px',
    fontFamily: '"PingFang SC","Microsoft YaHei",sans-serif'
  }}
}});
</script>

</body>
</html>
"""

BLOCK_TPL = '<div class="diagram-block"><h3>{title}</h3><div class="mermaid">{mermaid}</div></div>'


def gen_one(name, mermaid_src, title, output):
    blocks = BLOCK_TPL.format(title=title, mermaid=mermaid_src)
    html = HTML_TEMPLATE.format(
        title="光模块 + EML 国产替代 · 产业链全景图",
        date=datetime.now().strftime('%Y-%m-%d %H:%M'),
        summary="① 光模块产业链上中下游全景,每个环节标注 A 股龙头 | ② EML 卡脖子 5-20% 阶段路径,InP 衬底 + 设备 + 芯片 + 模块厂全打通 | ③ EML 工艺分代路线(2020-2028),看下一代 200G 异质集成 | ④ 国产化 Gantt 时间表(2024-2028) | ⑤ ⭐⭐⭐⭐⭐ = 强烈推荐标的,★ 红色 = 关键卡脖子",
        blocks=blocks
    )
    Path(output).write_text(html, encoding='utf-8')
    print(f"[✓] {output} ({len(html)} bytes)")


def main():
    if len(sys.argv) < 3:
        print("用法: draw_chain.py <mode> <output.html>")
        print("  mode: chain_module | chain_eml | route_eml | gantt | all_in_one")
        sys.exit(1)

    mode = sys.argv[1]
    output = sys.argv[2]

    if mode == 'chain_module':
        gen_one('chain_module', MERMAID_CHAIN_MODULE, '1. 光模块产业链全景图(上中下游 × A 股龙头)', output)
    elif mode == 'chain_eml':
        gen_one('chain_eml', MERMAID_CHAIN_EML, '2. EML 国产替代产业链(衬底/设备 → EML 芯片 → 模块厂)', output)
    elif mode == 'route_eml':
        gen_one('route_eml', MERMAID_ROUTE_EML, '3. EML 工艺分代路线(2020-2028,2-3 代 ahead)', output)
    elif mode == 'gantt':
        gen_one('gantt', MERMAID_GANTT, '4. EML 国产化时间表(2024-2028 Gantt)', output)
    elif mode == 'all_in_one':
        # 单文件包含 4 张图
        blocks = '\n'.join([
            BLOCK_TPL.format(title='1. 光模块产业链全景图(上中下游 × A 股龙头)', mermaid=MERMAID_CHAIN_MODULE),
            BLOCK_TPL.format(title='2. EML 国产替代产业链(衬底/设备 → 芯片 → 模块厂)', mermaid=MERMAID_CHAIN_EML),
            BLOCK_TPL.format(title='3. EML 工艺分代路线(2020-2028)', mermaid=MERMAID_ROUTE_EML),
            BLOCK_TPL.format(title='4. EML 国产化时间表(2024-2028)', mermaid=MERMAID_GANTT),
        ])
        html = HTML_TEMPLATE.format(
            title="光模块 + EML 国产替代 · 产业链全景图 · v1.0",
            date=datetime.now().strftime('%Y-%m-%d %H:%M'),
            summary="① 光模块产业链上中下游 | ② EML 国产替代全链路 | ③ EML 工艺分代 | ④ 国产化时间表 | ⑤ ⭐= 强烈推荐,★红=关键卡脖子",
            blocks=blocks
        )
        Path(output).write_text(html, encoding='utf-8')
        print(f"[✓] {output} ({len(html)} bytes, 4 张图)")
    else:
        print(f"未知模式: {mode}")
        sys.exit(1)


if __name__ == '__main__':
    main()

