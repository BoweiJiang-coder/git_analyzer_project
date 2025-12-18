"""
软件演化分析模块
功能：深度分析开源软件的演化规律和特点
使用 libcst, radon, lizard 等库进行静态代码分析
"""
import git
import os
from collections import Counter, defaultdict
from datetime import datetime

# 代码分析库
try:
    import libcst as cst
    from radon.complexity import cc_visit
    from radon.metrics import mi_visit, h_visit
    import lizard
    HAS_CODE_ANALYSIS = True
except ImportError as e:
    print(f"警告: 代码分析库导入失败: {e}")
    HAS_CODE_ANALYSIS = False

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional


class EvolutionAnalyzer:
    """软件演化分析器 - 深度分析开源软件的演化特征"""
    
    def __init__(self, repo_path):
        """初始化分析器"""
        if not os.path.exists(repo_path):
            raise FileNotFoundError(f"路径不存在: {repo_path}")
        
        try:
            self.repo = git.Repo(repo_path)
        except git.InvalidGitRepositoryError:
            raise ValueError(f"不是有效的Git仓库: {repo_path}")
        
        self.repo_path = repo_path
        self.commits = list(self.repo.iter_commits())
        print(f"✓ 加载仓库成功，共 {len(self.commits)} 次提交")
    
    def analyze_code_complexity_evolution(self, file_extensions=['.py'], sample_commits=50):
        """
        分析代码复杂度演化
        返回：复杂度随时间的变化趋势
        """
        print("\n[演化分析] 正在分析代码复杂度演化...")
        
        if not HAS_CODE_ANALYSIS:
            return {'error': '代码分析库未安装'}
        
        complexity_timeline = []
        
        # 采样提交以提高性能
        total_commits = len(self.commits)
        if total_commits > sample_commits:
            step = total_commits // sample_commits
            sampled_commits = self.commits[::step]
        else:
            sampled_commits = self.commits
        
        for idx, commit in enumerate(sampled_commits):
            try:
                commit_date = commit.authored_datetime
                
                # 分析该提交的代码文件
                complexity_metrics = self._analyze_commit_complexity(commit, file_extensions)
                
                if complexity_metrics:
                    complexity_timeline.append({
                        'commit_hash': commit.hexsha[:8],
                        'date': commit_date.strftime('%Y-%m-%d'),
                        'timestamp': commit_date,
                        **complexity_metrics
                    })
                
                if (idx + 1) % 10 == 0:
                    print(f"  已分析 {idx + 1}/{len(sampled_commits)} 个提交...")
                    
            except Exception as e:
                continue
        
        print(f"✓ 复杂度演化分析完成，共分析 {len(complexity_timeline)} 个时间点")
        return complexity_timeline
    
    def _analyze_commit_complexity(self, commit, file_extensions):
        """分析单个提交的代码复杂度"""
        total_complexity = 0
        total_loc = 0
        total_functions = 0
        file_count = 0
        
        try:
            # 获取该提交的所有文件
            for item in commit.tree.traverse():
                if item.type == 'blob':
                    file_path = item.path
                    
                    # 只分析指定扩展名的文件
                    if not any(file_path.endswith(ext) for ext in file_extensions):
                        continue
                    
                    try:
                        # 获取文件内容
                        file_content = item.data_stream.read().decode('utf-8', errors='ignore')
                        
                        # 使用 lizard 分析复杂度
                        analysis = lizard.analyze_file.analyze_source_code(
                            file_path, file_content
                        )
                        
                        for func in analysis.function_list:
                            total_complexity += func.cyclomatic_complexity
                            total_functions += 1
                        
                        total_loc += analysis.nloc
                        file_count += 1
                        
                    except Exception:
                        continue
            
            if file_count > 0:
                return {
                    'avg_complexity': round(total_complexity / max(total_functions, 1), 2),
                    'total_loc': total_loc,
                    'file_count': file_count,
                    'function_count': total_functions,
                    'complexity_per_loc': round(total_complexity / max(total_loc, 1) * 100, 2)
                }
        except Exception:
            pass
        
        return None
    
    def analyze_bug_fix_patterns(self):
        """
        分析Bug修复模式
        识别包含bug修复关键词的提交
        """
        print("\n[演化分析] 正在分析Bug修复模式...")
        
        bug_keywords = ['fix', 'bug', 'error', 'issue', 'patch', 'correct', 
                        '修复', '错误', 'hotfix', 'bugfix']
        
        bug_fixes = []
        bug_fix_by_month = defaultdict(int)
        bug_authors = Counter()
        bug_files = Counter()
        
        for commit in self.commits:
            message = commit.message.lower()
            
            # 检查是否包含bug修复关键词
            if any(keyword in message for keyword in bug_keywords):
                commit_date = commit.authored_datetime
                month_key = commit_date.strftime('%Y-%m')
                
                bug_fix_by_month[month_key] += 1
                bug_authors[commit.author.name] += 1
                
                # 获取修改的文件
                try:
                    if commit.parents:
                        diff = commit.parents[0].diff(commit)
                        for diff_item in diff:
                            if diff_item.a_path:
                                bug_files[diff_item.a_path] += 1
                except Exception:
                    pass
                
                bug_fixes.append({
                    'hash': commit.hexsha[:8],
                    'author': commit.author.name,
                    'date': commit_date.strftime('%Y-%m-%d %H:%M'),
                    'message': commit.message.strip().split('\n')[0][:100]
                })
        
        # 统计分析
        total_commits = len(self.commits)
        bug_fix_rate = (len(bug_fixes) / total_commits * 100) if total_commits > 0 else 0
        
        result = {
            'total_bug_fixes': len(bug_fixes),
            'bug_fix_rate': round(bug_fix_rate, 2),
            'bug_fixes_by_month': dict(sorted(bug_fix_by_month.items())),
            'top_bug_fixers': [
                {'author': author, 'fixes': count}
                for author, count in bug_authors.most_common(10)
            ],
            'most_buggy_files': [
                {'file': file, 'bug_fixes': count}
                for file, count in bug_files.most_common(10)
            ],
            'recent_bug_fixes': bug_fixes[:20]
        }
        
        print(f"✓ Bug修复分析完成，发现 {len(bug_fixes)} 次bug修复提交 ({bug_fix_rate:.1f}%)")
        return result
    
    def analyze_code_churn(self, sample_commits=100):
        """
        分析代码变动率（Code Churn）
        衡量代码的稳定性和重构频率
        """
        print("\n[演化分析] 正在分析代码变动率...")
        
        churn_data = []
        file_churn = defaultdict(lambda: {'additions': 0, 'deletions': 0, 'changes': 0})
        
        # 采样分析
        total_commits = len(self.commits)
        if total_commits > sample_commits:
            step = total_commits // sample_commits
            sampled_commits = self.commits[::step]
        else:
            sampled_commits = self.commits
        
        for commit in sampled_commits:
            try:
                if not commit.parents:
                    continue
                
                commit_date = commit.authored_datetime
                total_additions = 0
                total_deletions = 0
                files_changed = 0
                
                diff = commit.parents[0].diff(commit, create_patch=True)
                
                for diff_item in diff:
                    try:
                        if diff_item.diff:
                            diff_text = diff_item.diff.decode('utf-8', errors='ignore')
                            additions = diff_text.count('\n+') - 1
                            deletions = diff_text.count('\n-') - 1
                            
                            total_additions += additions
                            total_deletions += deletions
                            files_changed += 1
                            
                            # 记录文件级别的变动
                            file_path = diff_item.a_path or diff_item.b_path
                            if file_path:
                                file_churn[file_path]['additions'] += additions
                                file_churn[file_path]['deletions'] += deletions
                                file_churn[file_path]['changes'] += 1
                    except Exception:
                        continue
                
                if files_changed > 0:
                    churn_data.append({
                        'date': commit_date.strftime('%Y-%m-%d'),
                        'timestamp': commit_date,
                        'additions': total_additions,
                        'deletions': total_deletions,
                        'net_change': total_additions - total_deletions,
                        'files_changed': files_changed,
                        'churn_rate': total_additions + total_deletions
                    })
                
            except Exception:
                continue
        
        # 分析高变动文件
        high_churn_files = sorted(
            [
                {
                    'file': file,
                    'total_churn': data['additions'] + data['deletions'],
                    'additions': data['additions'],
                    'deletions': data['deletions'],
                    'change_count': data['changes']
                }
                for file, data in file_churn.items()
            ],
            key=lambda x: x['total_churn'],
            reverse=True
        )[:20]
        
        result = {
            'churn_timeline': churn_data,
            'high_churn_files': high_churn_files,
            'total_additions': sum(d['additions'] for d in churn_data),
            'total_deletions': sum(d['deletions'] for d in churn_data),
        }
        
        print(f"✓ 代码变动率分析完成，分析了 {len(churn_data)} 个提交")
        return result
    
    def analyze_development_velocity(self):
        """
        分析开发速度和节奏
        按时间段统计提交频率、代码量变化等
        """
        print("\n[演化分析] 正在分析开发速度...")
        
        # 按周统计
        weekly_stats = defaultdict(lambda: {
            'commits': 0, 'authors': set(), 'weekday': []
        })
        
        # 按月统计
        monthly_stats = defaultdict(lambda: {
            'commits': 0, 'authors': set(), 'active_days': set()
        })
        
        for commit in self.commits:
            commit_date = commit.authored_datetime
            
            # 周统计
            week_key = commit_date.strftime('%Y-W%U')
            weekly_stats[week_key]['commits'] += 1
            weekly_stats[week_key]['authors'].add(commit.author.name)
            weekly_stats[week_key]['weekday'].append(commit_date.weekday())
            
            # 月统计
            month_key = commit_date.strftime('%Y-%m')
            monthly_stats[month_key]['commits'] += 1
            monthly_stats[month_key]['authors'].add(commit.author.name)
            monthly_stats[month_key]['active_days'].add(commit_date.date())
        
        # 转换为列表
        weekly_velocity = [
            {
                'week': week,
                'commits': data['commits'],
                'active_authors': len(data['authors']),
                'avg_commits_per_author': round(data['commits'] / len(data['authors']), 2)
            }
            for week, data in sorted(weekly_stats.items())
        ]
        
        monthly_velocity = [
            {
                'month': month,
                'commits': data['commits'],
                'active_authors': len(data['authors']),
                'active_days': len(data['active_days']),
                'commits_per_day': round(data['commits'] / len(data['active_days']), 2)
            }
            for month, data in sorted(monthly_stats.items())
        ]
        
        result = {
            'weekly_velocity': weekly_velocity,
            'monthly_velocity': monthly_velocity,
        }
        
        print(f"✓ 开发速度分析完成")
        return result
    
    def analyze_contributor_evolution(self):
        """
        分析贡献者演化
        新增、流失、活跃度变化
        """
        print("\n[演化分析] 正在分析贡献者演化...")
        
        # 按月统计贡献者
        monthly_contributors = defaultdict(set)
        contributor_dates = defaultdict(list)
        
        for commit in self.commits:
            author = commit.author.name
            commit_date = commit.authored_datetime
            month_key = commit_date.strftime('%Y-%m')
            
            monthly_contributors[month_key].add(author)
            contributor_dates[author].append(commit_date)
        
        # 分析贡献者生命周期
        contributor_stats = []
        for author, dates in contributor_dates.items():
            # 确保日期排序
            sorted_dates = sorted(dates)
            first = sorted_dates[0]
            last = sorted_dates[-1]
            
            # 计算活跃天数，至少为 1 天
            duration_days = (last.date() - first.date()).days + 1
            
            contributor_stats.append({
                'author': author,
                'total_commits': len(dates),
                'first_commit': first.strftime('%Y-%m-%d'),
                'last_commit': last.strftime('%Y-%m-%d'),
                'active_days': duration_days,
                'commits_per_day': round(len(dates) / max(duration_days, 1), 3)
            })
        
        # 按月统计新增和流失
        # 注意：self.commits 是倒序的，所以需要反转月份顺序来统计增长
        sorted_months = sorted(monthly_contributors.keys())
        evolution = []
        all_contributors = set()
        
        for month in sorted_months:
            current_contributors = monthly_contributors[month]
            new_contributors = current_contributors - all_contributors
            
            evolution.append({
                'month': month,
                'total_contributors': len(current_contributors),
                'new_contributors': len(new_contributors),
                'cumulative_contributors': len(all_contributors | current_contributors)
            })
            
            all_contributors.update(current_contributors)
        
        result = {
            'contributor_evolution': evolution,
            'contributor_stats': sorted(contributor_stats, 
                                       key=lambda x: x['total_commits'], 
                                       reverse=True)[:20],
            'total_contributors': len(all_contributors)
        }
        
        print(f"✓ 贡献者演化分析完成，共 {len(all_contributors)} 名贡献者")
        return result
    
    def generate_full_report(self):
        """
        生成完整的演化分析报告
        """
        print("\n" + "="*60)
        print("开始生成完整演化分析报告")
        print("="*60)
        
        report = {
            'metadata': {
                'repo_path': self.repo_path,
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'total_commits': len(self.commits),
            }
        }
        
        # 1. Bug修复模式分析
        report['bug_fix_analysis'] = self.analyze_bug_fix_patterns()
        
        # 2. 代码变动率分析
        report['code_churn'] = self.analyze_code_churn(sample_commits=100)
        
        # 3. 开发速度分析
        report['development_velocity'] = self.analyze_development_velocity()
        
        # 4. 贡献者演化分析
        report['contributor_evolution'] = self.analyze_contributor_evolution()
        
        # 5. 代码复杂度演化（可选，耗时较长）
        try:
            report['complexity_evolution'] = self.analyze_code_complexity_evolution(
                file_extensions=['.py'], 
                sample_commits=30
            )
        except Exception as e:
            print(f"复杂度分析跳过: {e}")
            report['complexity_evolution'] = None
        
        print("\n" + "="*60)
        print("✓ 完整演化分析报告生成完成！")
        print("="*60)
        
        return report


if __name__ == "__main__":
    # 测试代码
    print("演化分析模块测试")
    test_repo = "../requests"  # 使用requests仓库作为测试
    
    if os.path.exists(test_repo):
        analyzer = EvolutionAnalyzer(test_repo)
        report = analyzer.generate_full_report()
        print(f"\n报告包含 {len(report)} 个分析维度")
    else:
        print(f"测试仓库不存在: {test_repo}")
