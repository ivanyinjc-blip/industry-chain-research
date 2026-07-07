"""
chain-chip-design/scripts/icon_lib.py
Bootstrap Icons 实心版 · 19 个产业链图标

设计来源:
  - Bootstrap Icons v1.x(MIT license · 2000+ icon)
  - 通过 cdn.jsdelivr.net/gh/twbs/icons 在线加载 + 本地缓存
  - 实心(fill)版,接近 Fluent 2 实心风

用法:
  from icon_lib import icon_svg, ICON_NAMES
  svg = icon_svg('chip', size=32, color='#2F80ED')

兼容:
  EMOJI_TO_ICON 字典:旧代码 emoji 字符 → 图标名
"""

import os
import urllib.request

# 本地缓存目录
CACHE_DIR = os.path.expanduser('~/.cache/bootstrap-icons')
os.makedirs(CACHE_DIR, exist_ok=True)

# jsdelivr CDN(比 raw.githubusercontent.com 更稳)
CDN_BASE = 'https://cdn.jsdelivr.net/gh/twbs/icons@main/icons/'

# === 19 个图标(产业链常用)===
ICON_MAP = {
    # 上游
    'chip':       'cpu-fill',
    'pcb':        'motherboard-fill',
    'optic':      'optical-audio-fill',
    'housing':    'box-seam-fill',
    'fiber':      'hdd-stack-fill',
    'material':   'stack',
    # 中游
    'flow':       'diagram-3-fill',
    'doc':        'file-earmark-text-fill',
    'design':     'easel-fill',
    'components': 'puzzle-fill',
    'integrate':  'diagram-3-fill',
    'test':       'beaker-fill',
    'ship':       'truck',
    # 下游
    'datacenter': 'hdd-rack-fill',
    'telecom':    'broadcast',
    'cloud':      'cloud-fill',
    'ai':         'robot',
    # 通用
    'arrow_right':'arrow-right',
    'check':      'check-circle-fill',
}

ICON_NAMES = list(ICON_MAP.keys())


def _load_svg(bi_name):
    cache_path = os.path.join(CACHE_DIR, f'{bi_name}.svg')
    if os.path.exists(cache_path) and os.path.getsize(cache_path) > 100:
        with open(cache_path, 'r', encoding='utf-8') as f:
            return f.read()
    url = CDN_BASE + bi_name + '.svg'
    try:
        urllib.request.urlretrieve(url, cache_path)
        with open(cache_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f'[icon_lib] 下载失败 {url}: {e}')
        return ''


def _colorize(svg_raw, color, size):
    if not svg_raw:
        return ''
    out = svg_raw.replace('fill="currentColor"', f'fill="{color}"', 1)
    out = out.replace('width="16"', f'width="{size}"', 1)
    out = out.replace('height="16"', f'height="{size}"', 1)
    return out


def icon_svg(name, size=24, color='#0B3A82'):
    if name not in ICON_MAP:
        return ''
    bi_name = ICON_MAP[name]
    raw = _load_svg(bi_name)
    return _colorize(raw, color, size)


EMOJI_TO_ICON = {
    '🔆': 'optic', '⚡': 'chip', '🔬': 'optic', '🧩': 'pcb',
    '🔌': 'components', '💡': 'fiber', '🔧': 'material',
    '📋': 'doc', '🎨': 'design', '🧠': 'design', '🔩': 'integrate',
    '🧪': 'test', '📦': 'ship',
    '🖥️': 'datacenter', '📡': 'telecom', '📶': 'telecom',
    '☁️': 'cloud', '🤖': 'ai',
    '✅': 'check', '➡️': 'arrow_right', '🔗': 'integrate',
}


if __name__ == '__main__':
    print('=== icon_lib 自检 ===')
    print(f'图标数:{len(ICON_NAMES)}')
    for name in ICON_NAMES:
        svg = icon_svg(name, 32, '#2F80ED')
        print(f'  {name:15s}: {len(svg):4d} chars  ({ICON_MAP[name]})')
