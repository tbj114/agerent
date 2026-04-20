# Arco Design 配色主题

# 主色调
ARCO_PRIMARY = '#165DFF'
ARCO_SUCCESS = '#00B42A'
ARCO_WARNING = '#FF7D00'
ARCO_ERROR = '#F53F3F'
ARCO_INFO = '#86909C'

# 中性色
ARCO_BLACK = '#000000'
ARCO_GRAY_1 = '#F2F3F5'
ARCO_GRAY_2 = '#E5E6EB'
ARCO_GRAY_3 = '#C9CDD4'
ARCO_GRAY_4 = '#86909C'
ARCO_GRAY_5 = '#4E5969'
ARCO_GRAY_6 = '#272E3B'
ARCO_WHITE = '#FFFFFF'

# 渐变色
ARCO_GRADIENTS = {
    'primary': f'linear-gradient(135deg, {ARCO_PRIMARY}, #6993FF)',
    'success': f'linear-gradient(135deg, {ARCO_SUCCESS}, #73D13D)',
    'warning': f'linear-gradient(135deg, {ARCO_WARNING}, #FFB940)',
    'error': f'linear-gradient(135deg, {ARCO_ERROR}, #FF7875)',
    'info': f'linear-gradient(135deg, {ARCO_INFO}, #B7C0CC)'
}

# 配色方案
ARCO_COLORS = [
    ARCO_PRIMARY,      # 主色
    ARCO_SUCCESS,      # 成功色
    ARCO_WARNING,      # 警告色
    ARCO_ERROR,        # 错误色
    '#722ED1',         # 紫色
    '#13C2C2',         # 青色
    '#FAAD14',         # 黄色
    '#EB2F96',         # 粉色
    '#52C41A',         # 绿色
    '#FA8C16'          # 橙色
]

# 暗色主题
ARCO_DARK = {
    'background': ARCO_GRAY_6,
    'text': ARCO_WHITE,
    'grid': ARCO_GRAY_5,
    'axis': ARCO_GRAY_4,
    'colors': ARCO_COLORS
}

# 亮色主题
ARCO_LIGHT = {
    'background': ARCO_WHITE,
    'text': ARCO_GRAY_6,
    'grid': ARCO_GRAY_2,
    'axis': ARCO_GRAY_5,
    'colors': ARCO_COLORS
}

# 自定义 colormap
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# 创建 Arco 蓝色渐变 colormap
def create_arco_blue_cmap():
    colors = [
        '#E6F7FF',  # 浅蓝
        '#BAE7FF',  # 浅蓝色
        '#91D5FF',  # 中蓝色
        '#69C0FF',  # 蓝色
        '#40A9FF',  # 深蓝色
        '#1677FF',  # 主蓝色
        '#096DD9'   # 最深蓝
    ]
    return mcolors.LinearSegmentedColormap.from_list('arco_blue', colors)

# 创建 Arco 渐变 colormap
def create_arco_gradient_cmap():
    colors = [
        '#E6F7FF',  # 浅蓝
        '#BAE7FF',  # 浅蓝色
        '#91D5FF',  # 中蓝色
        '#69C0FF',  # 蓝色
        '#40A9FF',  # 深蓝色
        '#1677FF',  # 主蓝色
        '#722ED1',  # 紫色
        '#EB2F96',  # 粉色
        '#F53F3F',  # 红色
        '#FA8C16',  # 橙色
        '#FAAD14'   # 黄色
    ]
    return mcolors.LinearSegmentedColormap.from_list('arco_gradient', colors)

# 注册 colormap
plt.register_cmap(name='arco_blue', cmap=create_arco_blue_cmap())
plt.register_cmap(name='arco_gradient', cmap=create_arco_gradient_cmap())

# 主题配置
themes = {
    'arco': {
        'figure.facecolor': ARCO_WHITE,
        'axes.facecolor': ARCO_WHITE,
        'axes.edgecolor': ARCO_GRAY_3,
        'axes.grid': True,
        'axes.grid.axis': 'y',
        'axes.labelsize': 12,
        'axes.labelcolor': ARCO_GRAY_5,
        'axes.titlesize': 16,
        'axes.titlecolor': ARCO_GRAY_6,
        'grid.color': ARCO_GRAY_2,
        'grid.linestyle': '-',
        'grid.linewidth': 0.5,
        'xtick.color': ARCO_GRAY_5,
        'ytick.color': ARCO_GRAY_5,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'text.color': ARCO_GRAY_6,
        'font.family': ['sans-serif'],
        'font.sans-serif': ['Arial', 'DejaVu Sans', 'sans-serif'],
        'legend.frameon': True,
        'legend.framealpha': 0.9,
        'legend.facecolor': ARCO_WHITE,
        'legend.edgecolor': ARCO_GRAY_3,
        'legend.fontsize': 10,
        'legend.loc': 'best'
    },
    'arco_dark': {
        'figure.facecolor': ARCO_GRAY_6,
        'axes.facecolor': ARCO_GRAY_6,
        'axes.edgecolor': ARCO_GRAY_5,
        'axes.grid': True,
        'axes.grid.axis': 'y',
        'axes.labelsize': 12,
        'axes.labelcolor': ARCO_GRAY_3,
        'axes.titlesize': 16,
        'axes.titlecolor': ARCO_WHITE,
        'grid.color': ARCO_GRAY_5,
        'grid.linestyle': '-',
        'grid.linewidth': 0.5,
        'xtick.color': ARCO_GRAY_3,
        'ytick.color': ARCO_GRAY_3,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'text.color': ARCO_WHITE,
        'font.family': ['sans-serif'],
        'font.sans-serif': ['Arial', 'DejaVu Sans', 'sans-serif'],
        'legend.frameon': True,
        'legend.framealpha': 0.9,
        'legend.facecolor': ARCO_GRAY_5,
        'legend.edgecolor': ARCO_GRAY_4,
        'legend.fontsize': 10,
        'legend.loc': 'best'
    },
    'minimal': {
        'figure.facecolor': ARCO_WHITE,
        'axes.facecolor': ARCO_WHITE,
        'axes.edgecolor': 'none',
        'axes.grid': False,
        'axes.labelsize': 12,
        'axes.labelcolor': ARCO_GRAY_5,
        'axes.titlesize': 16,
        'axes.titlecolor': ARCO_GRAY_6,
        'xtick.color': ARCO_GRAY_5,
        'ytick.color': ARCO_GRAY_5,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'text.color': ARCO_GRAY_6,
        'font.family': ['sans-serif'],
        'font.sans-serif': ['Arial', 'DejaVu Sans', 'sans-serif'],
        'legend.frameon': False,
        'legend.fontsize': 10,
        'legend.loc': 'best'
    }
}

# 应用主题
def apply_theme(theme_name='arco'):
    if theme_name in themes:
        plt.style.use('default')
        for key, value in themes[theme_name].items():
            plt.rcParams[key] = value
        return True
    return False
