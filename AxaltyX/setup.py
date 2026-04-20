
from setuptools import setup, find_packages
import os

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read() if os.path.exists('README.md') else ''

setup(
    name='axaltyx',
    version='1.0.0',
    author='TBJ114',
    description='专业级桌面统计软件，功能对标SPSS标准版',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    python_requires='&gt;=3.11',
    install_requires=[
        'PyQt6&gt;=6.5',
        'numpy&gt;=1.24',
        'scipy&gt;=1.10',
        'pandas&gt;=2.0',
        'scikit-learn&gt;=1.3',
        'statsmodels&gt;=0.14',
        'lifelines&gt;=0.27',
        'matplotlib&gt;=3.7',
        'plotly&gt;=5.15',
        'pyecharts&gt;=2.0',
        'openpyxl&gt;=3.1',
        'pyreadstat&gt;=1.2',
        'jieba&gt;=0.42',
    ],
    extras_require={
        'ml': ['torch&gt;=2.0'],
        'dev': [
            'pytest&gt;=7.4',
            'pytest-qt&gt;=4.2',
            'black&gt;=23.0',
            'ruff&gt;=0.1',
            'mypy&gt;=1.5',
        ],
    },
    entry_points={
        'console_scripts': [
            'axaltyx=axaltyx_gui.app:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
)

