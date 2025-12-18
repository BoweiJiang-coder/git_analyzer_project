"""
主程序入口
功能：整合分析器和可视化器，提供命令行界面
"""
import argparse
import sys
import os
from analyzer import GitAnalyzer
from visualizer import GitVisualizer
import matplotlib.pyplot as plt
from pylab import mpl
import warnings
import pysnooper
from evolution_analyzer import EvolutionAnalyzer
from evolution_visualizer import EvolutionVisualizer

# 忽略所有警告
warnings.filterwarnings('ignore')

# 设置显示中文字体
mpl.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams['axes.unicode_minus'] = False  # 解决中文字体下坐标轴负数的负号显示问题

# 使用 pysnooper 装饰主分析函数，方便观察演化分析的内部过程
@pysnooper.snoop()
def run_full_analysis(repo_path, output_dir):
    print(f"开始分析仓库: {repo_path}")
    
    # 1. 基础分析
    analyzer = GitAnalyzer(repo_path)
    basic_stats = analyzer.get_basic_stats()
    author_ranking = analyzer.get_author_ranking()
    frequency_data = analyzer.get_commit_frequency()
    
    # 2. 深度演化分析
    evo_analyzer = EvolutionAnalyzer(repo_path)
    full_report = evo_analyzer.generate_full_report()
    
    # 3. 可视化
    print("\n正在生成可视化图表...")
    # 基础可视化
    viz = GitVisualizer(output_dir)
    viz.plot_combined_report(basic_stats, author_ranking, frequency_data)
    
    # 增强版演化可视化
    env_viz = EvolutionVisualizer(output_dir)
    env_viz.plot_complexity_evolution(full_report.get('complexity_evolution'))
    env_viz.plot_bug_patterns(full_report.get('bug_fix_analysis'))
    env_viz.plot_code_churn(full_report.get('code_churn'))
    env_viz.plot_contributor_growth(full_report.get('contributor_evolution'))
    
    # 4. 保存结果
    env_viz.save_summary_report(full_report)
    
    print(f"\n恭喜！所有分析已完成，结果保存在: {output_dir}")

def analyze_repository(repo_path, output_dir='analysis_results', top_authors=10):
    """
    分析指定的Git仓库，包含基础统计和深度演化分析
    """
    print("=" * 60)
    print("🚀 Git仓库深度演化分析工具")
    print("=" * 60)

    if not os.path.exists(repo_path):
        print(f"错误：路径不存在 - {repo_path}")
        return False

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        # 1. 基础分析
        print(f"\n[1/3] 正在进行基础统计分析...")
        analyzer = GitAnalyzer(repo_path)
        basic_stats = analyzer.get_basic_stats()
        author_ranking = analyzer.get_author_ranking(top_n=top_authors)
        commit_frequency = analyzer.get_commit_frequency(by='month')
        
        # 基础可视化
        viz = GitVisualizer(output_dir)
        viz.plot_combined_report(basic_stats, author_ranking, commit_frequency)

        # 2. 深度演化分析 (使用 libcst, radon, lizard)
        print(f"\n[2/3] 正在进行深度演化分析 (这可能需要一点时间)...")
        evo_analyzer = EvolutionAnalyzer(repo_path)
        # 采样分析以平衡速度和精度
        full_report = evo_analyzer.generate_full_report()

        # 3. 增强版可视化
        print(f"\n[3/3] 正在生成增强版演化图表...")
        env_viz = EvolutionVisualizer(output_dir)
        
        if full_report.get('complexity_evolution'):
            env_viz.plot_complexity_evolution(full_report['complexity_evolution'])
        
        env_viz.plot_bug_patterns(full_report.get('bug_fix_analysis'))
        env_viz.plot_code_churn(full_report.get('code_churn'))
        env_viz.plot_contributor_growth(full_report.get('contributor_evolution'))
        
        # 保存结构化报告
        env_viz.save_summary_report(full_report)

        print("\n" + "=" * 60)
        print("✅ 分析完成！")
        print(f"📊 基础报告: {os.path.join(output_dir, 'combined_report.png')}")
        print(f"📈 演化图表已保存至: {output_dir}")
        print(f"📄 完整数据摘要: {os.path.join(output_dir, 'evolution_summary.json')}")
        print("=" * 60)

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
