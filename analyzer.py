"""
Git仓库分析模块
功能：读取Git仓库信息，进行统计分析
"""
import git
from collections import Counter, defaultdict
import os


class GitAnalyzer:
    def __init__(self, repo_path):
        if not os.path.exists(repo_path):
            raise FileNotFoundError(f"路径不存在: {repo_path}")

        try:
            self.repo = git.Repo(repo_path)
        except git.InvalidGitRepositoryError:
            raise ValueError(f"不是有效的Git仓库: {repo_path}")

        # 获取所有提交（按时间倒序，最新的在前面）
        self.commits = list(self.repo.iter_commits())

    def get_basic_stats(self):
        total_commits = len(self.commits)

        # 获取作者信息
        authors = set()
        first_commit = None
        last_commit = None

        for commit in self.commits:
            authors.add(commit.author.name)

        # 获取时间范围（第一个和最后一个提交）
        if self.commits:
            # 由于commits列表是按时间倒序的，所以第一个是最新的
            last_commit = self.commits[0].authored_datetime
            first_commit = self.commits[-1].authored_datetime
            days_active = (last_commit - first_commit).days
        else:
            days_active = 0

        return {
            '总提交数': total_commits,
            '作者数': len(authors),
            '首次提交时间': str(first_commit) if first_commit else "无",
            '最近提交时间': str(last_commit) if last_commit else "无",
            '活跃天数': days_active if days_active > 0 else 0
        }

    def get_author_ranking(self, top_n=10):
        if not self.commits:
            return []

        # 统计每个作者的提交次数
        author_counts = Counter()
        for commit in self.commits:
            author_counts[commit.author.name] += 1

        # 转换为列表并排序
        ranking = []
        total_commits = len(self.commits)

        for author, count in author_counts.most_common(top_n):
            percentage = (count / total_commits * 100) if total_commits > 0 else 0
            ranking.append({
                '作者': author,
                '提交次数': count,
                '占比': round(percentage, 2)
            })

        return ranking

    def get_commit_frequency(self, by='month'):
        if not self.commits:
            return {}

        frequency = defaultdict(int)

        for commit in self.commits:
            commit_date = commit.authored_datetime

            if by == 'day':
                key = commit_date.strftime('%Y-%m-%d')
            elif by == 'month':
                key = commit_date.strftime('%Y-%m')
            elif by == 'year':
                key = commit_date.strftime('%Y')
            else:
                key = commit_date.strftime('%Y-%m')

            frequency[key] += 1

        # 按时间排序
        sorted_frequency = dict(sorted(frequency.items()))
        return sorted_frequency

    def get_recent_commits(self, limit=10):
        recent_commits = []

        for i, commit in enumerate(self.commits[:limit]):
            recent_commits.append({
                '序号': i + 1,
                '哈希': commit.hexsha[:8],
                '作者': commit.author.name,
                '时间': commit.authored_datetime.strftime('%Y-%m-%d %H:%M'),
                '消息': commit.message.strip().split('\n')[0][:100]  
            })

        return recent_commits

    def get_file_changes_stats(self, limit=1000):
        if not self.commits:
            return {'文件总数': 0, '变更文件列表': []}

        file_changes = Counter()
        analyzed_commits = min(limit, len(self.commits))

        for commit in self.commits[:analyzed_commits]:
            # 统计本次提交中涉及的文件
            try:
                # 获取与上一个提交的差异
                if commit.parents:
                    diff = commit.parents[0].diff(commit)
                    for diff_item in diff:
                        if diff_item.a_path:
                            file_changes[diff_item.a_path] += 1
                        elif diff_item.b_path:
                            file_changes[diff_item.b_path] += 1
            except:
                # 如果出错，跳过这个提交
                continue

        # 获取变更最频繁的文件
        top_files = file_changes.most_common(20)

        return {
            '分析提交数': analyzed_commits,
            '涉及文件总数': len(file_changes),
            '最常变更文件': [{'文件': file, '变更次数': count} for file, count in top_files]
        }


def test_analyzer():
    try:
        # 使用当前目录测试（需要确保当前目录是Git仓库）
        analyzer = GitAnalyzer('.')

        print("基础统计:")
        basic_stats = analyzer.get_basic_stats()
        for key, value in basic_stats.items():
            print(f"{key}: {value}")

        print("\n作者排名:")
        authors = analyzer.get_author_ranking(5)
        for i, author in enumerate(authors, 1):
            print(f"{i}. {author['作者']}: {author['提交次数']}次 ({author['占比']}%)")

        print("\n最近提交:")
        recent = analyzer.get_recent_commits(5)
        for commit in recent:
            print(f"{commit['序号']}. [{commit['时间']}] {commit['作者']}: {commit['消息']}")

    except Exception as e:
        print(f"测试失败: {e}")
        print("请确保当前目录是一个Git仓库")


if __name__ == "__main__":
    test_analyzer()