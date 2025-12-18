"""
主程序入口
功能：整合分析器和可视化器，提供命令行界面
"""
import argparse
import json
import sys
import os
from datetime import datetime
from analyzer import GitAnalyzer
from visualizer import GitVisualizer
import matplotlib.pyplot as plt
from pylab import mpl
import warnings

# 忽略所有警告
warnings.filterwarnings('ignore')

# 设置显示中文字体
mpl.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams['axes.unicode_minus'] = False  # 解决中文字体下坐标轴负数的负号显示问题

def analyze_repository(repo_path, output_dir='results', top_authors=10):
    """
    分析指定的Git仓库
    """
    print("=" * 60)
    print("Git仓库分析工具")
    print("=" * 60)

    # 检查仓库路径
    if not os.path.exists(repo_path):
        print(f"错误：路径不存在 - {repo_path}")
        return False

    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        # 1. 初始化分析器
        print(f"正在分析仓库: {repo_path}")
        analyzer = GitAnalyzer(repo_path)
        print(f"仓库加载成功，共发现 {len(analyzer.commits)} 次提交")

        # 2. 获取各种分析结果
        print("\n[1/5] 正在收集基础统计信息...")
        basic_stats = analyzer.get_basic_stats()

        print("[2/5] 正在分析作者贡献...")
        author_ranking = analyzer.get_author_ranking(top_n=top_authors)

        print("[3/5] 正在分析提交频率...")
        commit_frequency = analyzer.get_commit_frequency(by='month')

        print("[4/5] 正在获取最近提交...")
        recent_commits = analyzer.get_recent_commits(limit=10)

        print("[5/5] 正在分析文件变更...")
        file_stats = analyzer.get_file_changes_stats(limit=500)

        # 3. 在控制台显示结果
        print("分析结果")

        print("\n基础统计:")
        for key, value in basic_stats.items():
            print(f"  {key}: {value}")

        print(f"\n作者排名 (前{min(top_authors, len(author_ranking))}名):")
        for i, author in enumerate(author_ranking, 1):
            print(f"  {i:2d}. {author['作者']:20} {author['提交次数']:4d} 次 ({author['占比']:.1f}%)")

        print(f"\n提交频率 (按月统计，共{len(commit_frequency)}个月):")
        if commit_frequency:
            # 显示最近几个月的提交情况
            recent_months = list(commit_frequency.items())[-6:]  # 最近6个月
            for month, count in recent_months:
                print(f"  {month}: {count} 次")

        print(f"\n最近提交 (前{len(recent_commits)}次):")
        for commit in recent_commits:
            print(f"  [{commit['时间']}] {commit['作者']}: {commit['消息']}")

        print(f"\n文件变更统计:")
        print(f"分析提交数: {file_stats.get('分析提交数', 0)}")
        print(f"涉及文件总数: {file_stats.get('涉及文件总数', 0)}")
        if file_stats.get('最常变更文件'):
            print(f"最常变更文件 (前5个):")
            for i, file_info in enumerate(file_stats['最常变更文件'][:5], 1):
                print(f"    {i}. {file_info['文件']}: {file_info['变更次数']} 次")

        # 4. 生成可视化图表
        print("\n🎨 正在生成可视化图表...")
        visualizer = GitVisualizer(output_dir)

        if author_ranking:
            visualizer.plot_author_ranking(author_ranking)

        if commit_frequency:
            visualizer.plot_commit_frequency(commit_frequency)

        visualizer.plot_combined_report(basic_stats, author_ranking, commit_frequency)

        # 5. 保存分析结果为JSON文件
        print("\n正在保存分析结果...")
        result_data = {
            '分析信息': {
                '仓库路径': os.path.abspath(repo_path),
                '分析时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                '分析工具': 'Git提交分析器 v1.0'
            },
            '基础统计': basic_stats,
            '作者排名': author_ranking,
            '提交频率': commit_frequency,
            '最近提交': recent_commits,
            '文件变更统计': file_stats
        }

        json_path = os.path.join(output_dir, 'analysis_result.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, indent=2, ensure_ascii=False)

        print(f"分析结果已保存: {json_path}")

        # 6. 生成简单的文本报告
        txt_report_path = os.path.join(output_dir, 'report.txt')
        with open(txt_report_path, 'w', encoding='utf-8') as f:
            f.write("Git仓库分析报告\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"仓库路径: {os.path.abspath(repo_path)}\n")
            f.write(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("1. 基础统计\n")
            f.write("-" * 30 + "\n")
            for key, value in basic_stats.items():
                f.write(f"{key}: {value}\n")

            f.write("\n2. 作者贡献排名\n")
            f.write("-" * 30 + "\n")
            for i, author in enumerate(author_ranking, 1):
                f.write(f"{i}. {author['作者']}: {author['提交次数']}次 ({author['占比']:.1f}%)\n")

            f.write("\n3. 最近提交\n")
            f.write("-" * 30 + "\n")
            for commit in recent_commits:
                f.write(f"[{commit['时间']}] {commit['作者']}: {commit['消息']}\n")

        print(f"文本报告已保存: {txt_report_path}")

        print("\n" + "=" * 60)
        print("分析完成！")
        print(f"所有结果已保存到: {os.path.abspath(output_dir)}")

        return True

    except Exception as e:
        print(f"\n分析过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Git提交分析器 - 分析Git仓库的提交历史和作者贡献',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 分析当前目录的Git仓库
  python main.py .

  # 分析指定仓库，指定输出目录
  python main.py /path/to/repo --output my_results

  # 显示前15名作者
  python main.py /path/to/repo --top 15

  # 使用交互模式
  python main.py --interactive
        """
    )

    parser.add_argument(
        'repo_path',
        nargs='?',
        default=None,
        help='Git仓库路径（如果不提供，则使用交互模式）'
    )

    parser.add_argument(
        '--output', '-o',
        default='analysis_results',
        help='输出目录（默认: analysis_results）'
    )

    parser.add_argument(
        '--top', '-t',
        type=int,
        default=10,
        help='显示前N名作者（默认: 10）'
    )

    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='使用交互模式'
    )

    args = parser.parse_args()

    # 交互模式
    if args.interactive or args.repo_path is None:
        print("欢迎使用Git提交分析器（交互模式）")
        print("-" * 40)

        # 获取仓库路径
        repo_path = input("请输入Git仓库路径（留空则使用当前目录）: ").strip()
        if not repo_path:
            repo_path = 'D:/Python/git_analyzer_project'

        # 获取输出目录
        output_dir = input(f"请输入输出目录（默认: {args.output}）: ").strip()
        if not output_dir:
            output_dir = args.output

        # 获取显示作者数量
        try:
            top_authors = int(input(f"显示前多少名作者（默认: {args.top}）: ").strip() or args.top)
        except ValueError:
            top_authors = args.top
            print(f"输入无效，使用默认值: {top_authors}")
    else:
        # 命令行参数模式
        repo_path = args.repo_path
        output_dir = args.output
        top_authors = args.top

    # 执行分析
    success = analyze_repository(repo_path, output_dir, top_authors)

    # 退出码
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
