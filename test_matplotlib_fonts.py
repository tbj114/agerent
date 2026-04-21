import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

# 打印 matplotlib 字体搜索路径
print("Matplotlib font search paths:")
for path in fm.findSystemFonts()[:10]:  # 只打印前10个路径
    print(f"  - {path}")

# 打印可用的中文字体
print("\nAvailable Chinese fonts:")
for font in fm.fontManager.ttflist:
    if 'WenQuanYi' in font.name or 'wqy' in font.name.lower() or 'zenhei' in font.name.lower():
        print(f"  - {font.name} ({font.fname})")

# 测试当前字体设置
print("\nCurrent font settings:")
print(f"  Default font family: {plt.rcParams['font.family']}")
print(f"  Font size: {plt.rcParams['font.size']}")

# 测试中文显示
plt.figure(figsize=(8, 4))
plt.title('测试中文显示')
plt.xlabel('横坐标')
plt.ylabel('纵坐标')
plt.text(0.5, 0.5, '你好，世界！', fontsize=16, ha='center')
plt.savefig('test_chinese_display.png', bbox_inches='tight')
print("\nTest plot saved as 'test_chinese_display.png'")
