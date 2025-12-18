import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import json

class EvolutionVisualizer:
    def __init__(self, output_dir='analysis_results'):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 设置绘图风格
        sns.set_theme(style="whitegrid")
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

    def plot_complexity_evolution(self, complexity_data):
        """绘制代码复杂度演化趋势"""
        if not complexity_data or (isinstance(complexity_data, dict) and 'error' in complexity_data):
            return

        df = pd.DataFrame(complexity_data)
        if df.empty: return
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')

        plt.figure(figsize=(12, 6))
        sns.lineplot(data=df, x='date', y='avg_complexity', marker='o', label='平均圈复杂度')
        plt.fill_between(df['date'], df['avg_complexity'], alpha=0.2)
        
        plt.title('代码复杂度演化趋势', fontsize=15)
        plt.xlabel('日期')
        plt.ylabel('平均复杂度 (Cyclomatic)')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'evolution_complexity.png'), dpi=300)
        plt.close()

    def plot_bug_patterns(self, bug_data):
        """绘制 Bug 修复模式分析"""
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
            plt.xticks(rotation=45)
            
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, 'evolution_bugs_monthly.png'), dpi=300)
            plt.close()

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

    def plot_code_churn(self, churn_data):
        """绘制代码变动率（Churn）分析"""
        if not churn_data or not churn_data.get('churn_timeline'):
            return

        df = pd.DataFrame(churn_data['churn_timeline'])
        if df.empty: return
        df['date'] = pd.to_datetime(df['date'])
        
        plt.figure(figsize=(12, 6))
        plt.stackplot(df['date'], df['additions'], df['deletions'], 
                      labels=['新增行数', '删除行数'], alpha=0.6, colors=['#2ecc71', '#e74c3c'])
        
        plt.title('代码变动率 (Code Churn) 演化', fontsize=15)
        plt.xlabel('日期')
        plt.ylabel('代码行数变动')
        plt.legend(loc='upper left')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'evolution_code_churn.png'), dpi=300)
        plt.close()

    def plot_contributor_growth(self, contributor_data):
        """绘制贡献者增长曲线"""
        if not contributor_data or not contributor_data.get('contributor_evolution'):
            return

        df = pd.DataFrame(contributor_data['contributor_evolution'])
        if df.empty: return
        
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=df, x='month', y='cumulative_contributors', marker='s', color='blue', label='累计贡献者')
        sns.barplot(data=df, x='month', y='new_contributors', color='lightblue', alpha=0.5, label='每月新增')
        
        plt.title('贡献者社区演化增长', fontsize=15)
        plt.xlabel('月份')
        plt.ylabel('人数')
        plt.legend()
        
        # 优化 X 轴标签显示
        if len(df) > 15:
            for i, label in enumerate(plt.gca().get_xticklabels()):
                if i % max(1, (len(df) // 10)) != 0:
                    label.set_visible(False)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'evolution_contributors.png'), dpi=300)
        plt.close()

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
