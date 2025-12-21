import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import json
import warnings
import matplotlib
from matplotlib import font_manager


class EvolutionVisualizer:
    def __init__(self, output_dir='analysis_results'):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 设置绘图风格
        sns.set_theme(style="whitegrid")

        # 配置Windows中文字体
        self._configure_windows_fonts()

    def _configure_windows_fonts(self):
        """配置Windows系统专用中文字体"""
        # 禁用警告
        warnings.filterwarnings('ignore', category=UserWarning)

        # 关键设置：使用ASCII减号而不是Unicode负号
        matplotlib.rcParams['axes.unicode_minus'] = False

        # 尝试直接添加字体文件
        windows_font_paths = [
            r'C:\Windows\Fonts\msyh.ttc',  # 微软雅黑
            r'C:\Windows\Fonts\simhei.ttf',  # 黑体
            r'C:\Windows\Fonts\simsun.ttc',  # 宋体
        ]

        fonts_added = []
        for font_path in windows_font_paths:
            if os.path.exists(font_path):
                try:
                    font_manager.fontManager.addfont(font_path)
                    font_name = font_manager.FontProperties(fname=font_path).get_name()
                    fonts_added.append(font_name)
                    print(f"EvolutionVisualizer: 添加字体 {font_name}")
                except Exception as e:
                    continue

        # 设置字体
        if fonts_added:
            # 使用我们添加的字体
            matplotlib.rcParams['font.sans-serif'] = fonts_added + ['DejaVu Sans', 'Arial']
        else:
            # 回退方案
            matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial', 'DejaVu Sans']

        matplotlib.rcParams['font.family'] = 'sans-serif'
        print(f"EvolutionVisualizer字体设置: {matplotlib.rcParams['font.sans-serif'][:3]}...")

    def _set_font_for_plot(self):
        """在每个绘图函数开始时设置字体"""
        # 确保使用ASCII减号
        plt.rcParams['axes.unicode_minus'] = False

        # 确保使用中文字体
        if 'Microsoft YaHei' not in plt.rcParams['font.sans-serif']:
            plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial', 'DejaVu Sans']

    def plot_complexity_evolution(self, complexity_data):
        """绘制代码复杂度演化趋势"""
        # 设置字体
        self._set_font_for_plot()

        if not complexity_data or (isinstance(complexity_data, dict) and 'error' in complexity_data):
            return

        df = pd.DataFrame(complexity_data)
        if df.empty:
            return

        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')

        plt.figure(figsize=(12, 6))
        sns.lineplot(data=df, x='date', y='avg_complexity', marker='o', label='平均圈复杂度')
        plt.fill_between(df['date'], df['avg_complexity'], alpha=0.2)

        plt.title('代码复杂度演化趋势', fontsize=15)
        plt.xlabel('日期')
        plt.ylabel('平均复杂度 (Cyclomatic)')

        # 优化 X 轴标签显示，防止遮挡
        if len(df) > 15:
            plt.gca().xaxis.set_major_locator(plt.MaxNLocator(10))

        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'evolution_complexity.png'), dpi=300)
        plt.close()
        print("✓ 已保存 complexity_evolution.png")

    def plot_bug_patterns(self, bug_data):
        """绘制 Bug 修复模式分析"""
        # 设置字体
        self._set_font_for_plot()

        if not bug_data:
            return

        # 1. 月度 Bug 修复趋势
        months = list(bug_data['bug_fixes_by_month'].keys())
        counts = list(bug_data['bug_fixes_by_month'].values())

        if months:
            plt.figure(figsize=(12, 6))
            sns.barplot(x=months, y=counts, palette="viridis")
            plt.title('月度 Bug 修复提交分布', fontsize=15)
            plt.xlabel('月份')
            plt.ylabel('修复提交数')

            # 优化 X 轴标签显示，防止遮挡
            if len(months) > 15:
                step = max(1, len(months) // 10)
                for i, label in enumerate(plt.gca().get_xticklabels()):
                    if i % step != 0:
                        label.set_visible(False)

            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, 'evolution_bugs_monthly.png'), dpi=300)
            plt.close()
            print("✓ 已保存 evolution_bugs_monthly.png")

        # 2. Bug 密集文件排行
        buggy_files = bug_data.get('most_buggy_files', [])[:10]
        if buggy_files:
            files = [f['file'].split('/')[-1] for f in buggy_files]
            fixes = [f['bug_fixes'] for f in buggy_files]

            plt.figure(figsize=(10, 6))
            sns.barplot(x=fixes, y=files, palette="magma")
            plt.title('Bug 最密集的文件 Top 10', fontsize=15)
            plt.xlabel('修复次数')
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, 'evolution_buggy_files.png'), dpi=300)
            plt.close()
            print("✓ 已保存 evolution_buggy_files.png")

    def plot_code_churn(self, churn_data):
        """绘制代码变动率（Churn）分析"""
        # 设置字体
        self._set_font_for_plot()

        if not churn_data or not churn_data.get('churn_timeline'):
            return

        df = pd.DataFrame(churn_data['churn_timeline'])
        if df.empty:
            return

        df['date'] = pd.to_datetime(df['date'])

        # 计算总变动量用于寻找最高点
        df['total_churn'] = df['additions'] + df['deletions']

        plt.figure(figsize=(12, 8))
        plt.stackplot(df['date'], df['additions'], df['deletions'],
                      labels=['新增行数', '删除行数'], alpha=0.6, colors=['#2ecc71', '#e74c3c'])

        plt.title('代码变动率 (Code Churn) 演化', fontsize=15)
        plt.xlabel('日期')
        plt.ylabel('代码行数变动')

        # 优化 X 轴标签显示，防止遮挡
        if len(df) > 15:
            plt.gca().xaxis.set_major_locator(plt.MaxNLocator(10))

        # 自动标注最高峰值
        if not df.empty:
            max_val = df['total_churn'].max()
            if max_val > 0:
                max_idx = df['total_churn'].idxmax()
                peak_date = df.loc[max_idx, 'date']

                plt.annotate(f'最高峰值: {int(max_val)}',
                             xy=(peak_date, max_val),
                             xytext=(0, 40),
                             textcoords='offset points',
                             ha='center',
                             va='bottom',
                             arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
                             bbox=dict(boxstyle="round,pad=0.5", fc="yellow", ec="orange", alpha=0.9))

        plt.legend(loc='upper left')
        plt.xticks(rotation=45)
        plt.grid(True, which="both", ls="-", alpha=0.2)

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'evolution_code_churn.png'), dpi=300)
        plt.close()
        print("✓ 已保存 evolution_code_churn.png")

    def plot_contributor_growth(self, contributor_data):
        """绘制贡献者增长曲线"""
        # 设置字体
        self._set_font_for_plot()

        if not contributor_data or not contributor_data.get('contributor_evolution'):
            return

        df = pd.DataFrame(contributor_data['contributor_evolution'])
        if df.empty:
            return

        plt.figure(figsize=(12, 6))

        # 累计贡献者折线图
        plt.plot(df['month'], df['cumulative_contributors'],
                 marker='s', color='blue', linewidth=2, label='累计贡献者')

        # 每月新增贡献者条形图
        plt.bar(df['month'], df['new_contributors'],
                alpha=0.5, color='lightblue', label='每月新增')

        plt.title('贡献者社区演化增长', fontsize=15)
        plt.xlabel('月份')
        plt.ylabel('人数')
        plt.legend()

        # 优化 X 轴标签显示
        if len(df) > 15:
            step = max(1, len(df) // 10)
            plt.xticks(range(len(df)),
                       [df.iloc[i]['month'] if i % step == 0 else '' for i in range(len(df))])
        else:
            plt.xticks(range(len(df)), df['month'])

        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'evolution_contributors.png'), dpi=300)
        plt.close()
        print("✓ 已保存 evolution_contributors.png")

    def save_summary_report(self, full_report):
        """保存结构化 JSON 报告"""
        report_path = os.path.join(self.output_dir, 'evolution_summary.json')

        def serializer(obj):
            if hasattr(obj, 'isoformat'):
                return obj.isoformat()
            return str(obj)

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(full_report, f, indent=4, ensure_ascii=False, default=serializer)
        print(f"✓ 演化分析摘要已保存至: {report_path}")