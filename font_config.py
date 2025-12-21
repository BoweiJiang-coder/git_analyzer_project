# font_config.py
"""
统一的字体配置文件
解决Windows系统下matplotlib中文字体显示和负号警告问题
"""
import os
import platform
import warnings
import matplotlib
from matplotlib import font_manager


def configure_fonts():
    """
    配置matplotlib字体，确保中文显示正常且避免负号警告
    """
    # 过滤掉所有matplotlib相关的警告
    warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')

    # 关键设置：使用ASCII减号而不是Unicode负号
    matplotlib.rcParams['axes.unicode_minus'] = False

    # 不使用TeX引擎渲染
    matplotlib.rcParams['text.usetex'] = False

    system = platform.system()

    if system == 'Windows':
        print("检测到Windows系统，配置中文字体...")

        # Windows系统字体配置
        windows_font_paths = [
            # 微软雅黑（最常用）
            r'C:\Windows\Fonts\msyh.ttc',
            r'C:\Windows\Fonts\msyhbd.ttc',

            # 黑体
            r'C:\Windows\Fonts\simhei.ttf',

            # 宋体
            r'C:\Windows\Fonts\simsun.ttc',
            r'C:\Windows\Fonts\simsunb.ttf',

            # 仿宋
            r'C:\Windows\Fonts\simfang.ttf',

            # 楷体
            r'C:\Windows\Fonts\simkai.ttf',
        ]

        # 添加字体到matplotlib
        fonts_added = []
        for font_path in windows_font_paths:
            if os.path.exists(font_path):
                try:
                    font_manager.fontManager.addfont(font_path)
                    font_name = font_manager.FontProperties(fname=font_path).get_name()
                    fonts_added.append(font_name)
                    print(f"✓ 添加字体: {font_name}")
                except Exception:
                    pass

        # 设置字体优先级顺序
        if fonts_added:
            # 优先使用我们添加的中文字体，然后是一些可靠的英文字体
            font_list = fonts_added + ['DejaVu Sans', 'Arial', 'sans-serif']
        else:
            # 如果找不到字体文件，尝试使用已知的字体名称
            font_list = ['Microsoft YaHei', 'SimHei', 'SimSun',
                         'DejaVu Sans', 'Arial', 'sans-serif']

        matplotlib.rcParams['font.sans-serif'] = font_list
        print(f"主程序字体设置: {font_list[:3]}...")

    elif system == 'Darwin':  # macOS
        print("检测到macOS系统，配置中文字体...")
        font_list = ['PingFang SC', 'Hiragino Sans GB',
                     'DejaVu Sans', 'Arial', 'sans-serif']
        matplotlib.rcParams['font.sans-serif'] = font_list

    else:  # Linux
        print("检测到Linux系统，配置中文字体...")
        font_list = ['WenQuanYi Micro Hei', 'DejaVu Sans',
                     'Liberation Sans', 'sans-serif']
        matplotlib.rcParams['font.sans-serif'] = font_list

    # 设置字体族
    matplotlib.rcParams['font.family'] = 'sans-serif'

    # 设置图形保存参数
    matplotlib.rcParams['figure.dpi'] = 100
    matplotlib.rcParams['savefig.dpi'] = 300
    matplotlib.rcParams['savefig.bbox'] = 'tight'
    matplotlib.rcParams['savefig.pad_inches'] = 0.1

    print("字体配置完成 ✓")


def check_font_configuration():
    """
    检查当前字体配置
    """
    print("\n当前字体配置:")
    print(f"  字体族: {matplotlib.rcParams['font.family']}")
    print(f"  字体列表: {matplotlib.rcParams['font.sans-serif'][:5]}")
    print(f"  Unicode负号: {matplotlib.rcParams['axes.unicode_minus']}")
    print(f"  使用TeX: {matplotlib.rcParams['text.usetex']}")

    # 检查字体是否可用
    available_fonts = [f.name for f in font_manager.fontManager.ttflist]
    print(f"\n可用字体数量: {len(available_fonts)}")

    # 检查当前设置的前几个字体是否在可用字体中
    for font in matplotlib.rcParams['font.sans-serif'][:5]:
        found = any(font in f for f in available_fonts)
        print(f"  字体 '{font}' 可用: {'✓' if found else '✗'}")