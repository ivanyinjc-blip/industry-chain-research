#!/usr/bin/env python3
"""
chain-chip-design/scripts/draw_chain_v2.py
产业链全景图生成器 · PIL 版 · 高保真

设计系统(继承自 v3 已认可的风格):
- 16:9 (1920×1080),纯白背景
- 深蓝标题 + 灰色副标题
- 三栏布局: 上游蓝 / 中游蓝 / 下游绿
- 卡片化设计 + 卡片阴影
- SVG 图标(替代 emoji)
- WenQuanYi Micro Hei 中文
- 底部:产业链总结 + 投资要点(蓝色勾)

用法:
  python3 draw_chain_v2.py <mode> <output.png>
  mode: optical_module | eml_substitution

输出: 单文件 1920×1080 PNG,高质量
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import cairosvg
from io import BytesIO


# =====================
# 设计系统(Design System)
# =====================
DS = {
    # 画布
    'W': 1920,
    'H': 1080,
    'bg': '#FFFFFF',

    # 标题
    'title_color': '#0B3A82',
    'title_size': 44,
    'sub_color': '#6B7B91',
    'sub_size': 22,

    # 卡片
    'card_bg': '#FAFBFD',
    'card_bg_green': '#F0FDF4',
    'card_border': '#E6EDF5',
    'card_radius': 6,

    # 主色
    'blue': '#2F80ED',
    'blue_dark': '#1E5BB8',
    'cyan': '#00B8D9',
    'green': '#22C55E',
    'green_dark': '#16A34A',

    # 文字
    'text': '#1a1a1a',
    'gray': '#6B7B91',
    'gray_dark': '#4A5568',

    # 介绍框
    'intro_bg': '#EFF6FF',
    'intro_border': '#BFDBFE',

    # 字号
    'card_name': 16,
    'card_desc': 12,
    'card_stock': 12,
    'step_name': 13,
    'step_desc': 10,
    'logo_name': 13,
    'logo_desc': 10,
    'footer_title': 15,
    'footer_text': 12,
}

# 中文字体路径(显式)
FONT_REG = '/home/ivanyinjc/.fonts/wqy-microhei.ttc'
FONT_MONO = '/home/ivanyinjc/.fonts/wqy-microhei.ttc'


def font(size, weight='reg'):
    """获取中文字体对象"""
    fp = FONT_REG
    return ImageFont.truetype(fp, size)


def svg_to_pil(svg_str, size):
    """SVG 字符串 → PIL Image"""
    png_bytes = cairosvg.svg2png(bytestring=svg_str.encode('utf-8'),
                                  output_width=size, output_height=size)
    return Image.open(BytesIO(png_bytes))


def text_w(draw, txt, fnt):
    """计算文本宽度"""
    bbox = draw.textbbox((0, 0), txt, font=fnt)
    return bbox[2] - bbox[0]


def text_h(draw, txt, fnt):
    bbox = draw.textbbox((0, 0), txt, font=fnt)
    return bbox[3] - bbox[1]


def rounded(draw, xy, radius, fill, outline=None, width=1):
    """画圆角矩形"""
    draw.rounded_rectangle(xy, radius=radius, fill=fill,
                            outline=outline, width=width)


def draw_gradient_header(draw, x, y, w, h, color1, color2):
    """画水平渐变 header"""
    # PIL 不直接支持渐变,用横条模拟
    for i in range(w):
        ratio = i / w
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        draw.line([(x + i, y), (x + i, y + h)], fill=(r, g, b))


def draw_shadow_card(draw, x, y, w, h, radius=DS['card_radius']):
    """画卡片 + 阴影效果"""
    # 阴影
    shadow = (200, 210, 220, 80)
    for offset in range(3, 0, -1):
        draw.rounded_rectangle(
            [x + offset, y + offset, x + w + offset, y + h + offset],
            radius=radius, fill=shadow)
    # 卡片
    draw.rounded_rectangle(
        [x, y, x + w, y + h],
        radius=radius, fill=DS['card_bg'],
        outline=DS['card_border'], width=1)


def draw_icon_circle(im, draw, x, y, size, icon_name, color=DS['blue']):
    """画圆形图标底 + SVG 图标。要求调用方传入主 Image(im)用于 paste。"""
    # 白色圆
    draw.ellipse([x, y, x + size, y + size], fill='#FFFFFF',
                 outline=DS['card_border'], width=1)
    # SVG 图标(65% of size)
    icon_size = int(size * 0.65)
    from icon_lib import icon_svg
    svg_str = icon_svg(icon_name, size=icon_size, color=color)
    if svg_str and im is not None:
        icon_im = svg_to_pil(svg_str, icon_size)
        if icon_im.mode != 'RGBA':
            icon_im = icon_im.convert('RGBA')
        im.paste(icon_im, (x + (size - icon_size) // 2,
                           y + (size - icon_size) // 2), icon_im)


def card_template(im, draw, x, y, w, h, icon_name, name, desc, stocks, stocks_color=DS['blue']):
    """画一张通用卡片(上游/下游都用这个)"""
    draw_shadow_card(draw, x, y, w, h)
    # 图标
    icon_size = 50
    draw_icon_circle(im, draw, x + 16, y + (h - icon_size) // 2, icon_size, icon_name)
    # 文字
    fnt_name = font(DS['card_name'])
    fnt_desc = font(DS['card_desc'])
    fnt_stock = font(DS['card_stock'])
    text_x = x + 16 + icon_size + 14
    draw.text((text_x, y + 14), name, fill=DS['title_color'], font=fnt_name)
    draw.text((text_x, y + 14 + 22), desc, fill=DS['gray'], font=fnt_desc)
    draw.text((text_x, y + 14 + 22 + 20),
             f"A 股龙头:{stocks}", fill=stocks_color, font=fnt_stock)


# =====================
# 模板:光模块
# =====================
def build_optical_module(out_path):
    W, H = DS['W'], DS['H']
    im = Image.new('RGB', (W, H), DS['bg'])
    d = ImageDraw.Draw(im)

    # ---- 标题 ----
    fnt_title = font(DS['title_size'])
    fnt_sub = font(DS['sub_size'])
    title = '光模块产业链全景图(上中下游 × A 股龙头)'
    sub = '一图看懂光模块从设计到应用的完整流程'
    d.text((W // 2 - text_w(d, title, fnt_title) // 2, 50),
           title, fill=DS['title_color'], font=fnt_title)
    d.text((W // 2 - text_w(d, sub, fnt_sub) // 2, 100),
           sub, fill=DS['gray'], font=fnt_sub)

    # ---- 三栏 ----
    col_y = 145
    col_h = 690
    col_w = 600
    gap = 20
    left_x = 30
    mid_x = left_x + col_w + gap
    right_x = mid_x + col_w + gap

    # === 左:上游 ===
    d.rounded_rectangle([left_x, col_y, left_x + col_w, col_y + col_h],
                        radius=8, fill='#FFFFFF', outline=DS['card_border'])
    draw_gradient_header(d, left_x, col_y, col_w, 50, DS['blue'], DS['blue_dark'])
    d.text((left_x + 18, col_y + 30),
           '上游 · 原材料 & 零部件', fill='#FFFFFF',
           font=font(20))

    upstreams = [
        ('chip', '光芯片', '光信号产生与电信号转换', '中际旭创 · 源杰科技'),
        ('chip', '电芯片', '驱动、放大、信号处理', '源杰科技 · 思瑞浦'),
        ('optic', '光器件', '光路传输、探测器、WDH', '光迅科技 · 华工科技'),
        ('pcb', 'PCB', '电路基板', '深南电路 · 沪电股份'),
        ('housing', '结构件', '外壳、散热器、连接器', '立讯精密 · 中航光电'),
        ('fiber', '光纤光缆', '光信号传输介质', '长飞光纤 · 亨通光电'),
        ('material', '其他辅材', '滤光片、透镜、散热材料', '永鼎股份 · 天孚通信'),
    ]
    for i, (icon, name, desc, stocks) in enumerate(upstreams):
        cy = col_y + 60 + i * 86
        card_template(im, d, left_x + 12, cy, col_w - 24, 76, icon, name, desc, stocks)

    # === 中:中游 ===
    d.rounded_rectangle([mid_x, col_y, mid_x + col_w, col_y + col_h],
                        radius=8, fill='#FFFFFF', outline=DS['card_border'])
    draw_gradient_header(d, mid_x, col_y, col_w, 50, DS['blue'], DS['blue_dark'])
    d.text((mid_x + 18, col_y + 30),
           '中游 · 光模块设计 & 制造(核心环节)', fill='#FFFFFF',
           font=font(20))

    # 6 步 3x2
    steps = [
        ('1', 'doc', '需求定义', '明确应用场景、速率、距离、接口参数'),
        ('2', 'design', '方案设计', '光电架构设计、电路设计、结构设计'),
        ('3', 'components', '器件选型', '选择芯片、激光器、探测器'),
        ('4', 'integrate', '模块集成', '光学对准、PCB 焊接、结构装配'),
        ('5', 'test', '测试验证', '性能测试、可靠性验证、兼容性'),
        ('6', 'ship', '封装出货', '老化测试、包装、出货给客户'),
    ]
    step_w = (col_w - 36) // 3
    step_h = 130
    for i, (num, icon, name, desc) in enumerate(steps):
        sx = mid_x + 12 + (i % 3) * (step_w + 6)
        sy = col_y + 60 + (i // 3) * (step_h + 10)
        d.rounded_rectangle([sx, sy, sx + step_w, sy + step_h],
                            radius=6, fill=DS['card_bg'],
                            outline=DS['card_border'])
        # 圆形编号
        cx, cy_n = sx + step_w // 2, sy + 22
        d.ellipse([cx - 14, cy_n - 14, cx + 14, cy_n + 14],
                  fill=DS['blue'])
        d.text((cx - 5, cy_n - 8), num, fill='#FFFFFF',
               font=font(14))
        # 图标
        icon_size = 30
        from icon_lib import icon_svg
        svg_str = icon_svg(icon, size=icon_size, color=DS['blue'])
        icon_im = svg_to_pil(svg_str, icon_size)
        im.paste(icon_im, (sx + step_w // 2 - icon_size // 2, sy + 38),
                 icon_im if icon_im.mode == 'RGBA' else None)
        # 名称 + 描述
        d.text((sx + step_w // 2, sy + 78), name, fill=DS['title_color'],
               font=font(DS['step_name']), anchor='mm')
        # 描述换行
        for j, line in enumerate(_wrap(desc, 12)):
            d.text((sx + step_w // 2, sy + 98 + j * 14), line,
                   fill=DS['gray_dark'], font=font(DS['step_desc']), anchor='mm')

    # 中游代表企业
    comp_y = col_y + 60 + 2 * (step_h + 10) + 6
    d.rounded_rectangle([mid_x + 12, comp_y, mid_x + col_w - 12, comp_y + 134],
                        radius=6, fill=DS['card_bg'],
                        outline=DS['card_border'])
    d.text((mid_x + col_w // 2, comp_y + 22),
           '中游代表企业(A 股龙头)', fill=DS['title_color'],
           font=font(13), anchor='mm')

    comps = [
        ('中际旭创', '全球高速光模块龙头'),
        ('新易盛', '高速光模块领先者'),
        ('天孚通信', '光器件 + 模块一体化'),
        ('光迅科技', '光器件 + 模块'),
        ('剑桥科技', '电信光模块领先'),
    ]
    cw = (col_w - 36) // 5
    for i, (n, d_text) in enumerate(comps):
        cx = mid_x + 14 + i * (cw + 4)
        cy = comp_y + 36
        d.rounded_rectangle([cx, cy, cx + cw, cy + 80],
                            radius=4, fill='#FFFFFF',
                            outline=DS['card_border'])
        d.text((cx + cw // 2, cy + 24), n, fill=DS['title_color'],
               font=font(12), anchor='mm')
        # 描述换行
        for j, line in enumerate(_wrap(d_text, 7)):
            d.text((cx + cw // 2, cy + 44 + j * 14), line,
                   fill=DS['gray'], font=font(9), anchor='mm')

    # === 右:下游 ===
    d.rounded_rectangle([right_x, col_y, right_x + col_w, col_y + col_h],
                        radius=8, fill='#FFFFFF', outline=DS['card_border'])
    draw_gradient_header(d, right_x, col_y, col_w, 50, DS['green'], DS['green_dark'])
    d.text((right_x + 18, col_y + 30),
           '下游 · 应用领域', fill='#FFFFFF',
           font=font(20))

    downs = [
        ('datacenter', '数据中心', '紫光股份 · 浪潮信息'),
        ('telecom', '电信网络', '中兴通讯 · 烽火通信'),
        ('telecom', '5G / 基站', '中兴通讯 · 大唐电信'),
        ('cloud', '云计算', '金山办公 · 用友网络'),
        ('ai', '人工智能', '海光信息 · 寒武纪'),
    ]
    for i, (icon, name, stocks) in enumerate(downs):
        cy = col_y + 60 + i * 86
        # 复用 card_template,但下游用绿底
        draw_shadow_card_green(d, right_x + 12, cy, col_w - 24, 76)
        # 图标
        icon_size = 50
        draw_icon_circle(im, d, right_x + 28, cy + (76 - icon_size) // 2,
                       icon_size, icon, color=DS['green_dark'])
        # 文字
        fnt_name = font(DS['card_name'])
        fnt_stock = font(DS['card_stock'])
        text_x = right_x + 12 + 16 + icon_size + 14
        d.text((text_x, cy + 14), name, fill=DS['title_color'], font=fnt_name)
        d.text((text_x, cy + 14 + 28),
               f"A 股龙头:{stocks}", fill=DS['green_dark'], font=fnt_stock)

    # ---- 介绍框 ----
    intro_y = 850
    intro_h = 70
    d.rounded_rectangle([30, intro_y, W - 30, intro_y + intro_h],
                        radius=6, fill=DS['intro_bg'],
                        outline=DS['intro_border'])
    # icon
    d.text((50, intro_y + 24), '💡', fill=DS['title_color'], font=font(28))
    d.text((108, intro_y + 22),
           '光模块是什么?', fill=DS['title_color'],
           font=font(15))
    d.text((108, intro_y + 44),
           '光模块是实现光电信号转换的核心器件,广泛应用于数据中心、电信网络等领域,把电信号转换为光信号进行传输,再把光信号转换回电信号。',
           fill=DS['gray_dark'], font=font(13))

    # ---- 底部 ----
    bot_y = 940
    bot_h = 110
    # 总结
    d.rounded_rectangle([30, bot_y, 1240, bot_y + bot_h],
                        radius=6, fill='#FFFFFF',
                        outline=DS['card_border'])
    d.text((50, bot_y + 22),
           '📌 产业链总结', fill=DS['title_color'],
           font=font(DS['footer_title']))
    d.text((50, bot_y + 50),
           '上游原材料 & 核心零件 → 中游模块设计、集成与测试 → 下游应用于各类通信与计算场景。',
           fill=DS['gray_dark'], font=font(DS['footer_text']))
    d.text((50, bot_y + 70),
           '光模块是数字经济的"高速公路",AI 驱动决定全产业链 5G 建设的持续增长。',
           fill=DS['gray_dark'], font=font(DS['footer_text']))

    # 投资要点
    d.rounded_rectangle([1260, bot_y, 1810, bot_y + bot_h],
                        radius=6, fill='#FFFFFF',
                        outline=DS['card_border'])
    d.text((1280, bot_y + 22),
           '✓ 投资要点', fill=DS['title_color'],
           font=font(DS['footer_title']))
    bullets = [
        'AI 算力驱动:数据中心高速光模块需求爆发',
        '国产替代加速:光芯片/光器件国产化率提升',
        '行业高景气:全球光模块市场强劲扩张',
    ]
    for i, b in enumerate(bullets):
        d.text((1280, bot_y + 48 + i * 22),
               f'✔ {b}', fill=DS['gray_dark'],
               font=font(DS['footer_text']))

    # QR 占位
    d.rounded_rectangle([1830, bot_y, 1890, bot_y + bot_h],
                        radius=6, fill='#FFFFFF',
                        outline=DS['card_border'])
    # 二维码简易模拟
    d.text((1860, bot_y + 30), '▦', fill=DS['gray'],
           font=font(28), anchor='mm')
    d.text((1860, bot_y + 70), '关注我们', fill=DS['gray'],
           font=font(10), anchor='mm')
    d.text((1860, bot_y + 86), '产业图谱', fill=DS['gray'],
           font=font(10), anchor='mm')

    im.save(out_path, 'PNG', optimize=True)
    print(f"[✓] {out_path} ({Path(out_path).stat().st_size // 1024} KB)")


def draw_shadow_card_green(draw, x, y, w, h, radius=DS['card_radius']):
    """绿色背景卡片(下游用)"""
    shadow = (200, 210, 220, 80)
    for offset in range(3, 0, -1):
        draw.rounded_rectangle(
            [x + offset, y + offset, x + w + offset, y + h + offset],
            radius=radius, fill=shadow)
    draw.rounded_rectangle(
        [x, y, x + w, y + h],
        radius=radius, fill=DS['card_bg_green'],
        outline=DS['card_border'], width=1)


def _wrap(text, max_chars):
    """简单换行"""
    if len(text) <= max_chars:
        return [text]
    mid = len(text) // 2
    for j in range(mid, len(text)):
        if text[j] in '、,。':
            return [text[:j + 1], text[j + 1:]]
    return [text[:mid], text[mid:]]


# =====================
# 模板:EML 国产替代
# =====================
def build_eml_substitution(out_path):
    W, H = DS['W'], DS['H']
    im = Image.new('RGB', (W, H), DS['bg'])
    d = ImageDraw.Draw(im)

    # 标题
    fnt_title = font(DS['title_size'])
    fnt_sub = font(DS['sub_size'])
    title = 'EML 国产替代产业链全景图(衬底 → 芯片 → 模块)'
    sub = '一图看懂 EML 光芯片从 InP 衬底到 1.6T 模块的国产替代路线'
    d.text((W // 2 - text_w(d, title, fnt_title) // 2, 50),
           title, fill=DS['title_color'], font=fnt_title)
    d.text((W // 2 - text_w(d, sub, fnt_sub) // 2, 100),
           sub, fill=DS['gray'], font=fnt_sub)

    # 三栏
    col_y = 145
    col_h = 690
    col_w = 600
    gap = 20
    left_x = 30
    mid_x = left_x + col_w + gap
    right_x = mid_x + col_w + gap

    # === 左:上游(衬底 + 设备 + 工艺)===
    d.rounded_rectangle([left_x, col_y, left_x + col_w, col_y + col_h],
                        radius=8, fill='#FFFFFF', outline=DS['card_border'])
    draw_gradient_header(d, left_x, col_y, col_w, 50, DS['blue'], DS['blue_dark'])
    d.text((left_x + 18, col_y + 30),
           '上游 · 衬底 + 设备 + 工艺', fill='#FFFFFF',
           font=font(20))

    upstreams = [
        ('chip', 'InP 磷化铟衬底', '2/3/4 英寸 · Sumitomo 90%+', '中科晶电 · 通美晶体'),
        ('design', 'MOCVD 设备', '金属有机化学气相沉积', '中微公司 688012'),
        ('design', '外延片生长', 'InP 基 MQW 量子阱', '源杰 · 长光华芯'),
        ('optic', '光刻 + 刻蚀', '量子阱结构工艺', '中微 · 北方华创'),
        ('test', '金属化 + 测试', 'P/N 接触 + DCA 验证', '通美晶体 · 源杰'),
        ('material', '测试设备 DCA/OSA', '国产 <10%', 'EXFO · Anritsu'),
    ]
    for i, (icon, name, desc, stocks) in enumerate(upstreams):
        cy = col_y + 60 + i * 92
        # 红色边框强调卡脖子
        draw_shadow_card_red(d, left_x + 12, cy, col_w - 24, 80)
        icon_size = 50
        draw_icon_circle(None, d, left_x + 28, cy + 15,
                       icon_size, icon, color='#B71C1C')
        text_x = left_x + 12 + 16 + icon_size + 14
        fnt_name = font(DS['card_name'])
        fnt_desc = font(DS['card_desc'])
        fnt_stock = font(DS['card_stock'])
        d.text((text_x, cy + 18), name, fill=DS['title_color'], font=fnt_name)
        d.text((text_x, cy + 40), desc, fill=DS['gray'], font=fnt_desc)
        d.text((text_x, cy + 60),
               f"A 股:★ {stocks}", fill='#B71C1C', font=fnt_stock)

    # === 中:中游 EML 芯片 ===
    d.rounded_rectangle([mid_x, col_y, mid_x + col_w, col_y + col_h],
                        radius=8, fill='#FFFFFF', outline=DS['card_border'])
    draw_gradient_header(d, mid_x, col_y, col_w, 50, DS['blue'], DS['blue_dark'])
    d.text((mid_x + 18, col_y + 30),
           '中游 · EML 芯片(卡脖子核心)', fill='#FFFFFF',
           font=font(20))

    # 6 步工艺路线
    steps = [
        ('1', 'design', '25G EML', '★ 已突破良率 70%'),
        ('2', 'design', '50G EML', '★ 验证期(送样)'),
        ('3', 'design', '100G EML', '概念验证阶段'),
        ('4', 'components', 'CW Laser', '配套芯片'),
        ('5', 'test', '良率爬升', '50% → 70% 拐点'),
        ('6', 'ship', '封装出货', 'OSA / TO 封装'),
    ]
    step_w = (col_w - 36) // 3
    step_h = 130
    for i, (num, icon, name, desc) in enumerate(steps):
        sx = mid_x + 12 + (i % 3) * (step_w + 6)
        sy = col_y + 60 + (i // 3) * (step_h + 10)
        d.rounded_rectangle([sx, sy, sx + step_w, sy + step_h],
                            radius=6, fill=DS['card_bg'],
                            outline=DS['card_border'])
        cx, cy_n = sx + step_w // 2, sy + 22
        d.ellipse([cx - 14, cy_n - 14, cx + 14, cy_n + 14],
                  fill=DS['blue'])
        d.text((cx - 5, cy_n - 8), num, fill='#FFFFFF',
               font=font(14))
        icon_size = 30
        from icon_lib import icon_svg
        svg_str = icon_svg(icon, size=icon_size, color=DS['blue'])
        icon_im = svg_to_pil(svg_str, icon_size)
        im.paste(icon_im, (sx + step_w // 2 - icon_size // 2, sy + 38),
                 icon_im if icon_im.mode == 'RGBA' else None)
        d.text((sx + step_w // 2, sy + 78), name, fill=DS['title_color'],
               font=font(13), anchor='mm')
        d.text((sx + step_w // 2, sy + 98), desc, fill=DS['gray_dark'],
               font=font(10), anchor='mm')
        d.text((sx + step_w // 2, sy + 116), desc.split('(')[0],
               fill=DS['gray_dark'], font=font(10), anchor='mm')

    # EML 三剑客
    comp_y = col_y + 60 + 2 * (step_h + 10) + 6
    d.rounded_rectangle([mid_x + 12, comp_y, mid_x + col_w - 12, comp_y + 134],
                        radius=6, fill='#FAFBFD',
                        outline=DS['card_border'])
    d.text((mid_x + col_w // 2, comp_y + 22),
           '中游代表企业(A 股龙头 · EML 三剑客)',
           fill=DS['title_color'],
           font=font(13), anchor='mm')

    comps = [
        ('源杰科技 688498', '⭐ 强烈推荐', 'YoY +1153%'),
        ('长光华芯 688048', '推荐', 'VCSEL 第一'),
        ('仕佳光子 688313', '推荐', 'CW + PLC'),
        ('中微公司 688012', '★ 设备突破', 'MOCVD'),
        ('通美晶体', '★ 衬底卡脖子', '未上市'),
    ]
    cw = (col_w - 36) // 5
    for i, (n, rating, growth) in enumerate(comps):
        cx = mid_x + 14 + i * (cw + 4)
        cy = comp_y + 36
        d.rounded_rectangle([cx, cy, cx + cw, cy + 80],
                            radius=4, fill='#FFFFFF',
                            outline=DS['card_border'])
        d.text((cx + cw // 2, cy + 18), n[:8], fill=DS['title_color'],
               font=font(10), anchor='mm')
        rating_color = DS['blue'] if '⭐' in rating else DS['green_dark'] if '推荐' in rating else '#B71C1C'
        d.text((cx + cw // 2, cy + 40), rating, fill=rating_color,
               font=font(10), anchor='mm')
        d.text((cx + cw // 2, cy + 60), growth, fill=DS['gray_dark'],
               font=font(9), anchor='mm')

    # === 右:下游模块厂 ===
    d.rounded_rectangle([right_x, col_y, right_x + col_w, col_y + col_h],
                        radius=8, fill='#FFFFFF', outline=DS['card_border'])
    draw_gradient_header(d, right_x, col_y, col_w, 50, DS['green'], DS['green_dark'])
    d.text((right_x + 18, col_y + 30),
           '下游 · 模块厂(EML 客户)', fill='#FFFFFF',
           font=font(20))

    downs = [
        ('datacenter', '800G 模块', '4 颗 EML/只', '中际旭创 · 新易盛'),
        ('datacenter', '1.6T 模块', '8 颗 EML/只', '中际旭创 · 新易盛'),
        ('telecom', '相干模块 200G+', 'EML + 相干技术', '光迅 · Coherent'),
        ('cloud', '电信运营商', 'DCI 长距', '中兴 · 烽火'),
        ('ai', '卫星激光通信', '新需求增长', 'SpaceX · 中国星网'),
    ]
    for i, (icon, name, desc, stocks) in enumerate(downs):
        cy = col_y + 60 + i * 86
        draw_shadow_card_green(d, right_x + 12, cy, col_w - 24, 76)
        icon_size = 50
        draw_icon_circle(None, d, right_x + 28, cy + 13,
                       icon_size, icon, color=DS['green_dark'])
        text_x = right_x + 12 + 16 + icon_size + 14
        fnt_name = font(DS['card_name'])
        fnt_desc = font(DS['card_desc'])
        fnt_stock = font(DS['card_stock'])
        d.text((text_x, cy + 14), name, fill=DS['title_color'], font=fnt_name)
        d.text((text_x, cy + 14 + 22), desc, fill=DS['gray'], font=fnt_desc)
        d.text((text_x, cy + 14 + 22 + 20),
               f"A 股:{stocks}", fill=DS['green_dark'], font=fnt_stock)

    # ---- 介绍框 ----
    intro_y = 850
    intro_h = 70
    d.rounded_rectangle([30, intro_y, W - 30, intro_y + intro_h],
                        radius=6, fill=DS['intro_bg'],
                        outline=DS['intro_border'])
    d.text((50, intro_y + 24), '🔬', fill=DS['title_color'], font=font(28))
    d.text((108, intro_y + 22),
           'EML 光芯片是什么?', fill=DS['title_color'],
           font=font(15))
    d.text((108, intro_y + 44),
           'EML(电吸收调制激光器)是 800G/1.6T 光模块的核心芯片,海外 Lumentum + 三菱 + Coherent 三强垄断 90%+;中国正从 5-20% 替代率突破 30%。',
           fill=DS['gray_dark'], font=font(13))

    # ---- 底部 ----
    bot_y = 940
    bot_h = 110
    d.rounded_rectangle([30, bot_y, 1240, bot_y + bot_h],
                        radius=6, fill='#FFFFFF',
                        outline=DS['card_border'])
    d.text((50, bot_y + 22),
           '📌 产业链总结', fill=DS['title_color'],
           font=font(DS['footer_title']))
    d.text((50, bot_y + 50),
           'InP 衬底 → MOCVD 设备 → 外延 → EML 芯片 → 800G/1.6T 模块 → 数据中心。',
           fill=DS['gray_dark'], font=font(DS['footer_text']))
    d.text((50, bot_y + 70),
           'EML 是 AI 算力神经末梢,源杰 +1153% YoY 验证 5-20% 阶段金矿。',
           fill=DS['gray_dark'], font=font(DS['footer_text']))

    d.rounded_rectangle([1260, bot_y, 1810, bot_y + bot_h],
                        radius=6, fill='#FFFFFF',
                        outline=DS['card_border'])
    d.text((1280, bot_y + 22),
           '✓ 投资要点', fill=DS['title_color'],
           font=font(DS['footer_title']))
    bullets = [
        '⭐ 源杰科技 688498:毛利 77.81% 超国际同行',
        '★ 卡脖子 5-20% 阶段是国产替代金矿',
        '★ 美 EML 禁运法案(2026 末预警)',
    ]
    for i, b in enumerate(bullets):
        d.text((1280, bot_y + 48 + i * 22),
               f'✔ {b}', fill=DS['gray_dark'],
               font=font(DS['footer_text']))

    d.rounded_rectangle([1830, bot_y, 1890, bot_y + bot_h],
                        radius=6, fill='#FFFFFF',
                        outline=DS['card_border'])
    d.text((1860, bot_y + 30), '▦', fill=DS['gray'],
           font=font(28), anchor='mm')
    d.text((1860, bot_y + 70), '关注我们', fill=DS['gray'],
           font=font(10), anchor='mm')
    d.text((1860, bot_y + 86), '产业图谱', fill=DS['gray'],
           font=font(10), anchor='mm')

    im.save(out_path, 'PNG', optimize=True)
    print(f"[✓] {out_path} ({Path(out_path).stat().st_size // 1024} KB)")


def draw_shadow_card_red(draw, x, y, w, h, radius=DS['card_radius']):
    """红色边框卡片(强调卡脖子)"""
    draw.rounded_rectangle([x, y, x + w, y + h],
                            radius=radius, fill='#FFF5F5',
                            outline='#FFCDD2', width=1)


# =====================
# Main
# =====================
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: draw_chain_v2.py <mode> <output.png>")
        print("  mode: optical_module | eml_substitution")
        sys.exit(1)
    mode = sys.argv[1]
    out = sys.argv[2]
    if mode == 'optical_module':
        build_optical_module(out)
    elif mode == 'eml_substitution':
        build_eml_substitution(out)
    else:
        print(f"未知 mode: {mode}")
        sys.exit(1)

