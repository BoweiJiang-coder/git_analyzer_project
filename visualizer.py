import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# 字体配置：尝试加载中文字体，失败则回退到默认
try:
    # 优先尝试 Windows 下常用的 SimHei
    font_path = os.path.join(matplotlib.get_data_path(), "fonts/ttf", "simhei.ttf")
    if os.path.exists(font_path):
        fm.fontManager.addfont(font_path)
        plt.rcParams['font.sans-serif'] = [fm.FontProperties(fname=font_path).get_name()]
    else:
        # Mac/Linux 常见中文备选
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'Microsoft YaHei', 'DejaVu Sans']
except Exception:
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']

plt.rcParams['axes.unicode_minus'] = False


class GitVisualizer:
    def __init__(self, output_dir='output'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def _save_plot(self, filename):
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        print(f"Generated: {filepath}")

    def plot_author_ranking(self, author_ranking, save=True):
        if not author_ranking:
            return None

        authors = [item['作者'] for item in author_ranking]
        commits = [item['提交次数'] for item in author_ranking]

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

        # Bar chart
        bars = ax1.bar(range(len(authors)), commits, color='skyblue', edgecolor='black')
        ax1.set_ylabel('提交次数')
        ax1.set_title('贡献排名')
        ax1.set_xticks(range(len(authors)))
        ax1.set_xticklabels(authors, rotation=45, ha='right')

        for bar, count in zip(bars, commits):
            ax1.text(bar.get_x() + bar.get_width() / 2., bar.get_height(),
                     f'{count}', ha='center', va='bottom')

        # Pie chart
        ax2.pie(commits, labels=authors, autopct='%1.1f%%', startangle=90)
        ax2.set_title('贡献占比')
        ax2.axis('equal')

        plt.tight_layout()
        if save:
            self._save_plot('author_ranking.png')
        return fig

    def plot_commit_frequency(self, frequency_data, save=True):
        if not frequency_data:
            return None

        dates = list(frequency_data.keys())
        counts = list(frequency_data.values())

        fig, ax = plt.subplots(figsize=(14, 6))
        
        ax.plot(range(len(dates)), counts, marker='o', linestyle='-',
                color='green', linewidth=2, markersize=5)
        ax.fill_between(range(len(dates)), counts, alpha=0.3, color='green')

        ax.set_ylabel('提交次数')
        ax.set_title('提交频率趋势')

        # 稀疏化 x 轴标签，避免重叠
        ticks = range(len(dates))
        labels = dates
        if len(dates) > 20:
            step = max(1, len(dates) // 15)
            labels = [d if i % step == 0 else '' for i, d in enumerate(dates)]
        
        ax.set_xticks(ticks)
        ax.set_xticklabels(labels, rotation=45, ha='right')
        ax.grid(True, alpha=0.3, linestyle='--')

        plt.tight_layout()
        if save:
            self._save_plot('commit_frequency.png')
        return fig

    def plot_combined_report(self, basic_stats, author_ranking, frequency_data, save=True):
        fig = plt.figure(figsize=(16, 12))

        # 1. 文本信息面板
        ax1 = plt.subplot2grid((3, 3), (0, 0), colspan=3)
        ax1.axis('off')
        
        info_text = (
            "仓库分析报告\n\n"
            f"总提交数: {basic_stats.get('总提交数', 0)}\n"
            f"作者数: {basic_stats.get('作者数', 0)}\n"
            f"活跃周期: {basic_stats.get('首次提交时间', '-')} 至 {basic_stats.get('最近提交时间', '-')}\n"
            f"活跃天数: {basic_stats.get('活跃天数', 0)}"
        )
        
        ax1.text(0.1, 0.5, info_text, fontsize=12, verticalalignment='center',
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        ax1.set_title('基本概况', fontsize=14, fontweight='bold')

        # 2. Top 8 作者柱状图
        if author_ranking:
            ax2 = plt.subplot2grid((3, 3), (1, 0), colspan=2)
            top_authors = author_ranking[:8]
            authors = [x['作者'] for x in top_authors]
            commits = [x['提交次数'] for x in top_authors]

            bars = ax2.bar(range(len(authors)), commits, color='lightcoral', edgecolor='black')
            ax2.set_title('核心贡献者 (Top 8)')
            ax2.set_xticks(range(len(authors)))
            ax2.set_xticklabels(authors, rotation=45, ha='right')
            
            for bar, count in zip(bars, commits):
                ax2.text(bar.get_x() + bar.get_width() / 2., bar.get_height(),
                         str(count), ha='center', va='bottom')

        # 3. 贡献分布饼图
        if author_ranking:
            ax3 = plt.subplot2grid((3, 3), (1, 2))
            top_n = 6
            pie_data = author_ranking[:top_n]
            
            labels = [x['作者'] for x in pie_data]
            sizes = [x['提交次数'] for x in pie_data]

            if len(author_ranking) > top_n:
                others_count = sum(x['提交次数'] for x in author_ranking[top_n:])
                labels.append('其他')
                sizes.append(others_count)

            ax3.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax3.set_title('贡献分布')

        # 4. 趋势图
        if frequency_data:
            ax4 = plt.subplot2grid((3, 3), (2, 0), colspan=3)
            dates = list(frequency_data.keys())
            counts = list(frequency_data.values())

            ax4.plot(range(len(dates)), counts, marker='o', color='blue', linewidth=2, markersize=4)
            ax4.fill_between(range(len(dates)), counts, alpha=0.2, color='blue')
            ax4.set_title('活跃度趋势')
            ax4.grid(True, alpha=0.3, linestyle='--')

            # 简化 x 轴显示
            step = max(1, len(dates) // 10) if len(dates) > 15 else 1
            visible_dates = [d if i % step == 0 else '' for i, d in enumerate(dates)]
            ax4.set_xticks(range(len(dates)))
            ax4.set_xticklabels(visible_dates, rotation=45, ha='right')

        plt.suptitle('Git 仓库分析大盘', fontsize=16, fontweight='bold')
        plt.tight_layout()

        if save:
            self._save_plot('combined_report.png')
        return fig


if __name__ == "__main__":
    # Mock data for quick testing
    mock_authors = [
        {'作者': f'User_{i}', '提交次数': 50 - i*5, '占比': 10.0} for i in range(8)
    ]
    mock_freq = {f'2024-0{i}': i*10 for i in range(1, 10)}
    mock_stats = {
        '总提交数': 500, '作者数': 8, 
        '首次提交时间': '2024-01', '最近提交时间': '2024-09', '活跃天数': 200
    }

    viz = GitVisualizer('test_output')
    viz.plot_author_ranking(mock_authors)
    viz.plot_commit_frequency(mock_freq)
    viz.plot_combined_report(mock_stats, mock_authors, mock_freq)