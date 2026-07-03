"""
chain-chip-design/scripts/icon_lib.py
轻量级 SVG 图标库 — 16 个产业链常用 icon(替代 emoji)
风格:扁平化、几何、统一线宽、Fluent 风
"""

def icon_svg(name, size=24, color="#0B3A82"):
    """返回 SVG path 字符串。name 必须在 ICONS 中。"""
    if name not in ICONS:
        return ''
    return ICONS[name].format(size=size, color=color)


# === 16 个产业图标 ===
# 每个图标用 viewBox="0 0 24 24" 的几何 path

ICONS = {
    # 上游:芯片类
    'chip': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <rect x="6" y="6" width="12" height="12" rx="2" fill="none" stroke="{color}" stroke-width="1.8"/>
      <rect x="9" y="9" width="6" height="6" fill="{color}"/>
      <line x1="3" y1="9" x2="6" y2="9" stroke="{color}" stroke-width="1.5"/>
      <line x1="3" y1="15" x2="6" y2="15" stroke="{color}" stroke-width="1.5"/>
      <line x1="18" y1="9" x2="21" y2="9" stroke="{color}" stroke-width="1.5"/>
      <line x1="18" y1="15" x2="21" y2="15" stroke="{color}" stroke-width="1.5"/>
      <line x1="9" y1="3" x2="9" y2="6" stroke="{color}" stroke-width="1.5"/>
      <line x1="15" y1="3" x2="15" y2="6" stroke="{color}" stroke-width="1.5"/>
      <line x1="9" y1="18" x2="9" y2="21" stroke="{color}" stroke-width="1.5"/>
      <line x1="15" y1="18" x2="15" y2="21" stroke="{color}" stroke-width="1.5"/>
    </svg>''',

    # 上游:电路板
    'pcb': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24">
      <rect x="3" y="5" width="18" height="14" rx="1" fill="none" stroke="{color}" stroke-width="1.5"/>
      <circle cx="7" cy="10" r="1" fill="{color}"/>
      <circle cx="17" cy="10" r="1" fill="{color}"/>
      <circle cx="7" cy="14" r="1" fill="{color}"/>
      <circle cx="17" cy="14" r="1" fill="{color}"/>
      <path d="M7 10 L11 10 L11 14 L17 14" stroke="{color}" stroke-width="1" fill="none"/>
      <path d="M11 10 L15 10" stroke="{color}" stroke-width="1" fill="none"/>
    </svg>''',

    # 上游:光器件(光路)
    'optic': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24">
      <circle cx="6" cy="12" r="3" fill="none" stroke="{color}" stroke-width="1.8"/>
      <circle cx="18" cy="12" r="3" fill="none" stroke="{color}" stroke-width="1.8"/>
      <line x1="9" y1="12" x2="15" y2="12" stroke="{color}" stroke-width="1.5"/>
      <line x1="6" y1="6" x2="6" y2="9" stroke="{color}" stroke-width="1"/>
      <line x1="6" y1="15" x2="6" y2="18" stroke="{color}" stroke-width="1"/>
      <line x1="18" y1="6" x2="18" y2="9" stroke="{color}" stroke-width="1"/>
      <line x1="18" y1="15" x2="18" y2="18" stroke="{color}" stroke-width="1"/>
    </svg>''',

    # 上游:外壳(立方体)
    'housing': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24">
      <path d="M4 8 L12 4 L20 8 L20 16 L12 20 L4 16 Z" fill="none" stroke="{color}" stroke-width="1.5"/>
      <path d="M4 8 L12 12 L20 8" stroke="{color}" stroke-width="1" fill="none"/>
      <line x1="12" y1="12" x2="12" y2="20" stroke="{color}" stroke-width="1"/>
    </svg>''',

    # 上游:光纤
    'fiber': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24">
      <circle cx="4" cy="12" r="2" fill="{color}"/>
      <line x1="6" y1="12" x2="20" y2="12" stroke="{color}" stroke-width="1.5"/>
      <circle cx="20" cy="12" r="2" fill="none" stroke="{color}" stroke-width="1.5"/>
    </svg>''',

    # 上游:材料
    'material': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24">
      <rect x="4" y="4" width="6" height="6" fill="{color}"/>
      <rect x="14" y="4" width="6" height="6" fill="none" stroke="{color}" stroke-width="1.5"/>
      <rect x="4" y="14" width="6" height="6" fill="none" stroke="{color}" stroke-width="1.5"/>
      <rect x="14" y="14" width="6" height="6" fill="{color}"/>
    </svg>''',

    # 中游:流程(箭头链)
    'flow': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24">
      <circle cx="5" cy="12" r="2" fill="{color}"/>
      <circle cx="12" cy="12" r="2" fill="{color}"/>
      <circle cx="19" cy="12" r="2" fill="{color}"/>
      <line x1="7" y1="12" x2="10" y2="12" stroke="{color}" stroke-width="1.5"/>
      <line x1="14" y1="12" x2="17" y2="12" stroke="{color}" stroke-width="1.5"/>
    </svg>''',

    # 中游:文档
    'doc': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24">
      <path d="M5 3 L15 3 L19 7 L19 21 L5 21 Z" fill="none" stroke="{color}" stroke-width="1.5"/>
      <path d="M15 3 L15 7 L19 7" stroke="{color}" stroke-width="1" fill="none"/>
      <line x1="8" y1="11" x2="16" y2="11" stroke="{color}" stroke-width="1"/>
      <line x1="8" y1="15" x2="16" y2="15" stroke="{color}" stroke-width="1"/>
    </svg>''',

    # 中游:芯片
    'design': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24">
      <rect x="6" y="6" width="12" height="12" fill="none" stroke="{color}" stroke-width="1.5"/>
      <text x="12" y="16" font-size="10" font-weight="700" fill="{color}" text-anchor="middle">A</text>
    </svg>''',

    # 中游:组件
    'components': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24">
      <circle cx="8" cy="8" r="2.5" fill="{color}"/>
      <rect x="13" y="6" width="6" height="4" fill="{color}"/>
      <rect x="6" y="14" width="6" height="4" fill="{color}"/>
      <circle cx="17" cy="17" r="2" fill="none" stroke="{color}" stroke-width="1.5"/>
    </svg>''',

    # 中游:集成
    'integrate': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24">
      <rect x="3" y="3" width="8" height="8" fill="{color}"/>
      <rect x="13" y="3" width="8" height="8" fill="none" stroke="{color}" stroke-width="1.5"/>
      <rect x="3" y="13" width="8" height="8" fill="none" stroke="{color}" stroke-width="1.5"/>
      <rect x="13" y="13" width="8" height="8" fill="{color}"/>
    </svg>''',

    # 中游:测试(对勾)
    'test': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24">
      <circle cx="12" cy="12" r="9" fill="none" stroke="{color}" stroke-width="1.5"/>
      <path d="M7 12 L11 16 L17 9" stroke="{color}" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>''',

    # 中游:出货(盒子)
    'ship': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24">
      <path d="M3 7 L12 3 L21 7 L21 17 L12 21 L3 17 Z" fill="none" stroke="{color}" stroke-width="1.5"/>
      <path d="M3 7 L12 11 L21 7" stroke="{color}" stroke-width="1.5" fill="none"/>
      <line x1="12" y1="11" x2="12" y2="21" stroke="{color}" stroke-width="1.5"/>
    </svg>''',

    # 下游:数据中心
    'datacenter': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24">
      <rect x="3" y="4" width="18" height="4" fill="none" stroke="{color}" stroke-width="1.5"/>
      <rect x="3" y="10" width="18" height="4" fill="{color}"/>
      <rect x="3" y="16" width="18" height="4" fill="none" stroke="{color}" stroke-width="1.5"/>
      <circle cx="6" cy="6" r="0.5" fill="{color}"/>
      <circle cx="6" cy="18" r="0.5" fill="{color}"/>
    </svg>''',

    # 下游:电信(信号塔)
    'telecom': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24">
      <line x1="12" y1="3" x2="12" y2="21" stroke="{color}" stroke-width="2"/>
      <path d="M6 9 L12 6 L18 9" stroke="{color}" stroke-width="1.5" fill="none"/>
      <path d="M4 13 L12 8 L20 13" stroke="{color}" stroke-width="1.5" fill="none"/>
      <circle cx="12" cy="3" r="1.5" fill="{color}"/>
      <line x1="9" y1="21" x2="15" y2="21" stroke="{color}" stroke-width="2"/>
    </svg>''',

    # 下游:云
    'cloud': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24">
      <path d="M6 17 C3 17 3 13 5 12 C5 9 8 7 11 9 C12 6 17 7 17 11 C20 11 20 16 17 17 Z" fill="none" stroke="{color}" stroke-width="1.5"/>
    </svg>''',

    # 下游:AI(机器人)
    'ai': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24">
      <rect x="6" y="8" width="12" height="10" rx="1" fill="none" stroke="{color}" stroke-width="1.5"/>
      <circle cx="9" cy="13" r="1" fill="{color}"/>
      <circle cx="15" cy="13" r="1" fill="{color}"/>
      <line x1="12" y1="4" x2="12" y2="8" stroke="{color}" stroke-width="1.5"/>
      <circle cx="12" cy="3" r="1" fill="{color}"/>
    </svg>''',

    # 通用:箭头右
    'arrow_right': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24">
      <line x1="4" y1="12" x2="18" y2="12" stroke="{color}" stroke-width="2"/>
      <path d="M14 8 L18 12 L14 16" stroke="{color}" stroke-width="2" fill="none"/>
    </svg>''',

    # 通用:对勾
    'check': '''<svg width="{size}" height="{size}" viewBox="0 0 24 24">
      <path d="M5 12 L10 17 L19 7" stroke="{color}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>''',
}

# 兼容名映射(老的 emoji 字符 → 新 icon)
EMOJI_TO_ICON = {
    '🔆': 'optic', '⚡': 'chip', '🔬': 'optic', '🧩': 'pcb',
    '🔌': 'components', '💡': 'fiber', '🔧': 'material',
    '📋': 'doc', '🎨': 'design', '🧠': 'design', '🔩': 'integrate',
    '🧪': 'test', '📦': 'ship',
    '🖥️': 'datacenter', '📡': 'telecom', '📶': 'telecom',
    '☁️': 'cloud', '🤖': 'ai',
}

