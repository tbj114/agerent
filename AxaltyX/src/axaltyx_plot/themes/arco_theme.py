# Arco Design 色彩主题

# 主色调
ARCO_PRIMARY = '#165DFF'
ARCO_SUCCESS = '#00B42A'
ARCO_WARNING = '#FF7D00'
ARCO_ERROR = '#F53F3F'
ARCO_INFO = '#86909C'

# 中性色
ARCO_WHITE = '#FFFFFF'
ARCO_BLACK = '#000000'
ARCO_GRAY_1 = '#F7F8FA'
ARCO_GRAY_2 = '#F2F3F5'
ARCO_GRAY_3 = '#E5E6EB'
ARCO_GRAY_4 = '#C9CDD4'
ARCO_GRAY_5 = '#86909C'
ARCO_GRAY_6 = '#4E5969'
ARCO_GRAY_7 = '#272E3B'
ARCO_GRAY_8 = '#1D2129'

# 功能色
ARCO_LINK = '#165DFF'
ARCO_BG_COLOR = '#F5F5F5'
ARCO_TEXT_COLOR = '#1D2129'
ARCO_TEXT_COLOR_SECONDARY = '#4E5969'

# 渐变色
ARCO_GRADIENTS = {
    'blue': ['#165DFF', '#7292FF'],
    'green': ['#00B42A', '#52C41A'],
    'orange': ['#FF7D00', '#FFB000'],
    'red': ['#F53F3F', '#FF4D4F'],
    'purple': ['#722ED1', '#B37FEB']
}

# 配色方案
ARCO_COLORS = [
    ARCO_PRIMARY,  # 主色
    '#722ED1',     # 紫色
    '#0FC6C2',     # 青色
    ARCO_SUCCESS,  # 绿色
    '#FF7D00',     # 橙色
    ARCO_ERROR,    # 红色
    '#7292FF',     # 浅蓝
    '#13C2C2',     # 深青
    '#52C41A',     # 浅绿
    '#FAAD14',     # 黄色
    '#F759AB',     # 粉色
    '#1890FF'      # 亮蓝
]

# Matplotlib 配色映射
MATPLOTLIB_CMAPS = {
    'arco_blue': 'Blues',
    'arco_green': 'Greens',
    'arco_orange': 'Oranges',
    'arco_red': 'Reds',
    'arco_purple': 'Purples',
    'arco_gradient': 'viridis'
}

# 主题配置
def get_arco_theme():
    """获取Arco Design主题配置"""
    return {
        'figure.facecolor': ARCO_WHITE,
        'axes.facecolor': ARCO_WHITE,
        'axes.edgecolor': ARCO_GRAY_3,
        'axes.labelcolor': ARCO_TEXT_COLOR_SECONDARY,
        'text.color': ARCO_TEXT_COLOR,
        'xtick.color': ARCO_TEXT_COLOR_SECONDARY,
        'ytick.color': ARCO_TEXT_COLOR_SECONDARY,
        'grid.color': ARCO_GRAY_2,
        'legend.facecolor': ARCO_WHITE,
        'legend.edgecolor': ARCO_GRAY_3,
        'patch.edgecolor': ARCO_WHITE,
        'lines.color': ARCO_PRIMARY,
        'font.family': ['WenQuanYi Zen Hei'],
        'font.sans-serif': ['WenQuanYi Zen Hei', 'DejaVu Sans', 'sans-serif']
    }

def get_arco_dark_theme():
    """获取Arco Design暗色主题配置"""
    return {
        'figure.facecolor': ARCO_GRAY_8,
        'axes.facecolor': ARCO_GRAY_8,
        'axes.edgecolor': ARCO_GRAY_6,
        'axes.labelcolor': ARCO_GRAY_4,
        'text.color': ARCO_WHITE,
        'xtick.color': ARCO_GRAY_4,
        'ytick.color': ARCO_GRAY_4,
        'grid.color': ARCO_GRAY_7,
        'legend.facecolor': ARCO_GRAY_7,
        'legend.edgecolor': ARCO_GRAY_6,
        'patch.edgecolor': ARCO_GRAY_8,
        'lines.color': ARCO_PRIMARY,
        'font.family': ['WenQuanYi Zen Hei'],
        'font.sans-serif': ['WenQuanYi Zen Hei', 'DejaVu Sans', 'sans-serif']
    }

def get_minimal_theme():
    """获取极简主题配置"""
    return {
        'figure.facecolor': ARCO_WHITE,
        'axes.facecolor': ARCO_WHITE,
        'axes.edgecolor': ARCO_GRAY_3,
        'axes.labelcolor': ARCO_TEXT_COLOR,
        'text.color': ARCO_TEXT_COLOR,
        'xtick.color': ARCO_TEXT_COLOR,
        'ytick.color': ARCO_TEXT_COLOR,
        'grid.color': ARCO_GRAY_2,
        'legend.facecolor': 'none',
        'legend.edgecolor': 'none',
        'patch.edgecolor': ARCO_WHITE,
        'lines.color': ARCO_PRIMARY,
        'font.family': ['WenQuanYi Zen Hei'],
        'font.sans-serif': ['WenQuanYi Zen Hei', 'DejaVu Sans', 'sans-serif']
    }

def get_theme(theme_name='arco'):
    """获取指定主题配置
    
    Args:
        theme_name: 主题名称 ('arco', 'dark', 'minimal')
    
    Returns:
        主题配置字典
    """
    if theme_name == 'dark':
        return get_arco_dark_theme()
    elif theme_name == 'minimal':
        return get_minimal_theme()
    else:
        return get_arco_theme()
