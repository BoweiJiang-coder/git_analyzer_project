"""
可视化模块
功能：将分析结果可视化为图表
"""
import matplotlib.pyplot as plt
import matplotlib
import os

try:
    matplotlib.font_manager.fontManager.addfont(os.path.join(
        matplotlib.get_data_path(), "fonts/ttf", "simhei.ttf"
    ))
    font_name = matplotlib.font_manager.FontProperties(
        fname=os.path.join(
            matplotlib.get_data_path(), "fonts/ttf", "simhei.ttf"
        )
    ).get_name()
    plt.rcParams['font.sans-serif'] = [font_name]
except:
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']

plt.rcParams['axes.unicode_minus'] = False


class GitVisualizer:
    def __init__(self, output_dir='output'):
        self.output_dir = output_dir

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def plot_author_ranking(self, author_ranking, save=True):
        if not author_ranking:
            print("没有作者数据可绘制")
            return None

        authors = [item['作者'] for item in author_ranking]
        commits = [item['提交次数'] for item in author_ranking]
        percentages = [item['占比'] for item in author_ranking]

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

        bars = ax1.bar(range(len(authors)), commits, color='skyblue', edgecolor='black')
        ax1.set_xlabel('作者')
        ax1.set_ylabel('提交次数')
        ax1.set_title('作者贡献排名（提交次数）')
        ax1.set_xticks(range(len(authors)))
        ax1.set_xticklabels(authors, rotation=45, ha='right')

        for bar, count in zip(bars, commits):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width() / 2., height,
                     f'{count}', ha='center', va='bottom')

        ax2.pie(commits, labels=authors, autopct='%1.1f%%', startangle=90)
        ax2.set_title('作者贡献占比')
        ax2.axis('equal')

        plt.tight_layout()

        if save:
            filepath = os.path.join(self.output_dir, 'author_ranking.png')
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            print(f"图表已保存: {filepath}")

        return fig

    def plot_commit_frequency(self, frequency_data, save=True):
        if not frequency_data:
            print("没有提交频率数据可绘制")
            return None

        dates = list(frequency_data.keys())
        counts = list(frequency_data.values())

        fig, ax = plt.subplots(figsize=(14, 6))

        line, = ax.plot(range(len(dates)), counts, marker='o', linestyle='-',
                        color='green', linewidth=2, markersize=5)

        ax.fill_between(range(len(dates)), counts, alpha=0.3, color='green')

        ax.set_xlabel('时间')
        ax.set_ylabel('提交次数')
        ax.set_title('提交频率趋势')

        if len(dates) > 20:
            step = max(1, len(dates) // 15)
            visible_dates = [dates[i] if i % step == 0 else '' for i in range(len(dates))]
            ax.set_xticks(range(len(dates)))
            ax.set_xticklabels(visible_dates, rotation=45, ha='right')
        else:
            ax.set_xticks(range(len(dates)))
            ax.set_xticklabels(dates, rotation=45, ha='right')

        ax.grid(True, alpha=0.3, linestyle='--')

        plt.tight_layout()

        if save:
            filepath = os.path.join(self.output_dir, 'commit_frequency.png')
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            print(f"图表已保存: {filepath}")

        return fig

    def plot_combined_report(self, basic_stats, author_ranking, frequency_data, save=True):
        fig = plt.figure(figsize=(16, 12))

        ax1 = plt.subplot2grid((3, 3), (0, 0), colspan=3)
        ax1.axis('off')

        info_text = "仓库分析报告\n\n"
        info_text += f"总提交数: {basic_stats.get('总提交数', 0)}\n"
        info_text += f"作者数: {basic_stats.get('作者数', 0)}\n"
        info_text += f"首次提交: {basic_stats.get('首次提交时间', 'N/A')}\n"
        info_text += f"最近提交: {basic_stats.get('最近提交时间', 'N/A')}\n"
        info_text += f"活跃天数: {basic_stats.get('活跃天数', 0)}\n"

        ax1.text(0.1, 0.5, info_text, fontsize=12, verticalalignment='center',
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        ax1.set_title('仓库基本信息', fontsize=14, fontweight='bold')

        if author_ranking:
            ax2 = plt.subplot2grid((3, 3), (1, 0), colspan=2)
            authors = [item['作者'] for item in author_ranking[:8]]
            commits = [item['提交次数'] for item in author_ranking[:8]]

            bars = ax2.bar(range(len(authors)), commits, color='lightcoral', edgecolor='black')
            ax2.set_xlabel('作者')
            ax2.set_ylabel('提交次数')
            ax2.set_title('作者贡献排名（前8名）')
            ax2.set_xticks(range(len(authors)))
            ax2.set_xticklabels(authors, rotation=45, ha='right')

            for bar, count in zip(bars, commits):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width() / 2., height,
                         f'{count}', ha='center', va='bottom')

        if author_ranking:
            ax3 = plt.subplot2grid((3, 3), (1, 2))
            authors = [item['作者'] for item in author_ranking[:6]]
            commits = [item['提交次数'] for item in author_ranking[:6]]

            if len(author_ranking) > 6:
                authors.append('其他')
                other_commits = sum(item['提交次数'] for item in author_ranking[6:])
                commits.append(other_commits)

            ax3.pie(commits, labels=authors, autopct='%1.1f%%', startangle=90)
            ax3.set_title('作者贡献占比')
            ax3.axis('equal')

        if frequency_data:
            ax4 = plt.subplot2grid((3, 3), (2, 0), colspan=3)
            dates = list(frequency_data.keys())
            counts = list(frequency_data.values())

            ax4.plot(range(len(dates)), counts, marker='o', linestyle='-',
                     color='blue', linewidth=2, markersize=4)
            ax4.fill_between(range(len(dates)), counts, alpha=0.2, color='blue')

            ax4.set_xlabel('时间')
            ax4.set_ylabel('提交次数')
            ax4.set_title('提交频率趋势')
            ax4.grid(True, alpha=0.3, linestyle='--')

            if len(dates) > 15:
                step = max(1, len(dates) // 10)
                visible_dates = [dates[i] if i % step == 0 else '' for i in range(len(dates))]
                ax4.set_xticks(range(len(dates)))
                ax4.set_xticklabels(visible_dates, rotation=45, ha='right')
            else:
                ax4.set_xticks(range(len(dates)))
                ax4.set_xticklabels(dates, rotation=45, ha='right')

        plt.suptitle('Git仓库分析报告', fontsize=16, fontweight='bold')
        plt.tight_layout()

        if save:
            filepath = os.path.join(self.output_dir, 'combined_report.png')
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            print(f"综合报告图已保存: {filepath}")

        return fig


def test_visualizer():
    test_authors = [
        {'作者': '张三', '提交次数': 45, '占比': 45.0},
        {'作者': '李四', '提交次数': 30, '占比': 30.0},
        {'作者': '王五', '提交次数': 15, '占比': 15.0},
        {'作者': '赵六', '提交次数': 10, '占比': 10.0},
    ]

    test_frequency = {
        '2024-01': 5, '2024-02': 8, '2024-03': 12,
        '2024-04': 15, '2024-05': 20, '2024-06': 18,
        '2024-07': 10, '2024-08': 7, '2024-09': 5,
    }

    test_stats = {
        '总提交数': 100,
        '作者数': 4,
        '首次提交时间': '2024-01-01',
        '最近提交时间': '2024-09-30',
        '活跃天数': 273
    }

    visualizer = GitVisualizer('test_output')
    visualizer.plot_author_ranking(test_authors)
    visualizer.plot_commit_frequency(test_frequency)
    visualizer.plot_combined_report(test_stats, test_authors, test_frequency)

    print("可视化测试完成，请查看 test_output 目录")


if __name__ == "__main__":
    test_visualizer()