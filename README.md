# Git仓库演化分析工具

> 开源软件基础课程大作业项目 | 一个用于深度分析Git仓库演化规律和团队协作情况的Python工具

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/)
[![GitPython](https://img.shields.io/badge/GitPython-✓-green.svg)](https://gitpython.readthedocs.io/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-✓-orange.svg)](https://matplotlib.org/)
[![LibCST](https://img.shields.io/badge/LibCST-✓-purple.svg)](https://libcst.readthedocs.io/)
[![License](https://img.shields.io/badge/license-Academic-blue.svg)](LICENSE)

## 📋 项目简介

本工具是一个基于Python的Git仓库深度分析平台，不仅提供基础的提交统计功能，还能进行多维度的演化规律分析，可视化展示代码质量、团队协作、项目发展等关键指标。该项目是《开源软件基础》课程的大作业，完全使用课程讲授的开源软件工具/类库实现。

**核心价值**：
- 为项目管理者提供团队协作的量化洞察
- 帮助开发者理解项目演化规律和技术债积累
- 可视化展示开源项目的活跃度、质量趋势与贡献分布
- 识别高风险代码区域和Bug热点文件

## 🚀 功能特性

### 📊 基础统计分析
- **基础统计**：总提交数、作者数、时间跨度、活跃天数
- **作者分析**：贡献排名、提交占比、活跃作者识别
- **提交频率**：按日/月/年统计的提交趋势分析
- **文件分析**：最常变更文件、文件变更热度

### 🔍 深度演化分析
- **代码复杂度演化**：跟踪代码圈复杂度随时间的变化趋势
- **Bug修复模式**：识别Bug修复提交，分析修复频率和热点文件
- **代码变动率(Churn)**：衡量代码稳定性和重构频率
- **开发速度分析**：统计周/月开发节奏和活跃度变化
- **贡献者演化**：跟踪贡献者新增、流失和活跃度变化

### 📈 高级可视化
- **作者贡献排名图**：柱状图展示Top-N贡献者
- **提交频率趋势图**：折线图展示项目活跃度变化
- **综合报告图**：多图表整合的完整分析报告
- **演化趋势图**：代码复杂度、Bug修复、代码变动的演化趋势
- **贡献者增长曲线**：社区贡献者数量增长趋势

### ⚡ 技术特性
- **命令行交互**：支持参数模式和交互式模式
- **智能采样**：大仓库自动采样分析，平衡速度与精度
- **错误处理**：完善的异常处理和用户提示
- **多格式输出**：支持PNG图片、JSON、结构化报告多种格式
- **跨平台**：支持Windows、macOS、Linux系统
- **智能字体配置**：自动检测操作系统并配置中文字体，避免乱码问题 ✅

## 🛠️ 快速开始

### 环境要求
- Python 3.6 或更高版本
- Git 命令行工具（已安装并配置）
- 推荐使用虚拟环境

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/BoweiJiang-coder/git_analyzer_project.git
   cd git_analyzer_project
   ```

2. **安装基础依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **安装可选依赖**（如需深度演化分析）
   ```bash
   pip install libcst radon lizard
   ```

### 使用方式

#### 方式一：命令行模式
```bash
# 分析当前目录的Git仓库
python main.py .

# 分析指定仓库，指定输出目录
python main.py /path/to/repo --output my_results

# 显示前15名作者
python main.py /path/to/repo --top 15

# 使用交互模式
python main.py --interactive
```

#### 方式二：交互模式
```bash
python main.py --interactive
```
或直接运行：
```bash
python main.py
```

## 📁 项目结构

```
git_analyzer_project/
├── main.py                    # 主程序入口
├── analyzer.py               # 基础Git仓库分析模块
├── visualizer.py            # 基础可视化模块
├── evolution_analyzer.py    # 深度演化分析模块
├── evolution_visualizer.py  # 演化分析可视化模块
├── font_config.py           # 智能字体配置文件
├── README.md                # 项目说明文档
├── requirements.txt         # 依赖列表
└── analysis_results/        # 输出目录（自动生成）
    ├── combined_report.png           # 综合报告图
    ├── evolution_complexity.png      # 代码复杂度演化图
    ├── evolution_bugs_monthly.png    # Bug修复月度分布
    ├── evolution_buggy_files.png     # Bug密集文件排行
    ├── evolution_code_churn.png      # 代码变动率演化图
    ├── evolution_contributors.png    # 贡献者增长曲线
    └── evolution_summary.json        # 结构化分析报告
```

## 🔧 模块说明

### analyzer.py
- **功能**：Git仓库基础统计分析
- **核心类**：`GitAnalyzer`
- **主要方法**：
  - `get_basic_stats()`: 获取仓库基础统计
  - `get_author_ranking()`: 作者贡献排名
  - `get_commit_frequency()`: 提交频率统计
  - `get_file_changes_stats()`: 文件变更统计

### visualizer.py
- **功能**：基础可视化图表生成
- **核心类**：`GitVisualizer`
- **主要方法**：
  - `plot_author_ranking()`: 绘制作者贡献排名图
  - `plot_commit_frequency()`: 绘制提交频率趋势图
  - `plot_combined_report()`: 生成综合报告图

### evolution_analyzer.py
- **功能**：深度演化规律分析
- **核心类**：`EvolutionAnalyzer`
- **主要方法**：
  - `analyze_code_complexity_evolution()`: 分析代码复杂度演化
  - `analyze_bug_fix_patterns()`: 分析Bug修复模式
  - `analyze_code_churn()`: 分析代码变动率
  - `analyze_development_velocity()`: 分析开发速度
  - `analyze_contributor_evolution()`: 分析贡献者演化
  - `generate_full_report()`: 生成完整演化分析报告

### evolution_visualizer.py
- **功能**：演化分析可视化
- **核心类**：`EvolutionVisualizer`
- **主要方法**：
  - `plot_complexity_evolution()`: 绘制代码复杂度演化趋势
  - `plot_bug_patterns()`: 绘制Bug修复模式分析
  - `plot_code_churn()`: 绘制代码变动率分析
  - `plot_contributor_growth()`: 绘制贡献者增长曲线
  - `save_summary_report()`: 保存结构化JSON报告

### font_config.py
- **功能**：智能字体配置模块
- **核心函数**：`configure_fonts()`
- **特性**：
  - 自动检测操作系统类型（Windows/macOS/Linux）
  - 自动加载系统中文字体文件
  - 解决matplotlib中文字体显示问题
  - 避免Unicode负号警告

## 📊 输出示例

### 1. 综合报告图 (`combined_report.png`)

包含：
- 仓库基本信息（提交数、作者数、活跃天数）
- 作者贡献排名（前8名）
- 作者贡献占比饼图
- 提交频率趋势图

### 2. 演化分析图表
- **代码复杂度演化**：显示项目代码质量变化趋势
- **Bug修复分布**：识别Bug修复的热点时间段
- **代码变动率**：展示代码变更幅度和趋势
- **贡献者增长**：展示社区发展的健康程度

### 3. 结构化报告 (`evolution_summary.json`)
```json
{
  "metadata": {
    "repo_path": "/path/to/repo",
    "analysis_date": "2024-01-15 14:30:00",
    "total_commits": 1250
  },
  "bug_fix_analysis": {
    "total_bug_fixes": 85,
    "bug_fix_rate": 6.8,
    "top_bug_fixers": [
      {
        "author": "张三",
        "fixes": 25
      },
      {
        "author": "李四",
        "fixes": 18
      }
    ],
    "most_buggy_files": [
      {
        "file": "src/main.py",
        "bug_fixes": 12
      },
      {
        "file": "src/utils.py",
        "bug_fixes": 8
      }
    ],
    "recent_bug_fixes": [
      {
        "hash": "a1b2c3d4",
        "author": "王五",
        "date": "2024-01-15 10:30:00",
        "message": "修复空指针异常"
      }
    ],
    "bug_fixes_by_month": {
      "2024-01": 5,
      "2024-02": 8,
      "2024-03": 12
    }
  },
  "code_churn": {
    "total_additions": 12500,
    "total_deletions": 8400,
    "churn_timeline": [
      {
        "date": "2024-01-15",
        "additions": 150,
        "deletions": 80,
        "net_change": 70,
        "files_changed": 5
      }
    ],
    "high_churn_files": [
      {
        "file": "src/main.py",
        "total_churn": 450,
        "additions": 300,
        "deletions": 150,
        "change_count": 12
      }
    ]
  },
  "contributor_evolution": {
    "total_contributors": 42,
    "contributor_evolution": [
      {
        "month": "2024-01",
        "total_contributors": 5,
        "new_contributors": 2,
        "cumulative_contributors": 5
      }
    ],
    "contributor_stats": [
      {
        "author": "张三",
        "total_commits": 150,
        "first_commit": "2023-12-01",
        "last_commit": "2024-01-15",
        "active_days": 46,
        "commits_per_day": 3.26
      }
    ]
  }
}
```

## ⚙️ 配置选项

### 命令行参数
| 参数 | 简写 | 描述 | 默认值 |
|------|------|------|--------|
| `--output` | `-o` | 输出目录 | `analysis_results` |
| `--top` | `-t` | 显示前N名作者 | `10` |
| `--interactive` | `-i` | 使用交互模式 | `False` |

### 交互模式
交互模式提供友好的用户界面：
1. 输入Git仓库路径（支持相对/绝对路径）
2. 指定输出目录
3. 显示前N名作者
4. 自动进行完整分析

## 🐛 常见问题

### Q1: 缺少代码分析库怎么办？
A: 如果不需要深度演化分析功能，可以跳过安装`libcst`、`radon`、`lizard`等库。基础统计分析功能不受影响。

### Q2: 分析大型仓库速度慢？
A: 工具内置智能采样机制，对于超过1000次提交的仓库会自动采样分析。可以通过调整`sample_commits`参数控制采样密度。

### Q3: 图表中的中文字体无法显示？
A: 我们已内置智能字体配置系统，支持：
   - **Windows系统**：自动使用微软雅黑、黑体等系统字体
   - **macOS系统**：自动使用苹方字体
   - **Linux系统**：自动使用文泉驿微米黑
   
   如果仍有显示问题，请确保：
   1. 系统已安装相应中文字体
   2. 使用最新版本的matplotlib库
   3. 运行 `python -c "import matplotlib; print(matplotlib.rcParams['font.sans-serif'])"` 检查字体配置

### Q4: GitPython报错"不是有效的Git仓库"？
A: 请确认指定的路径是有效的Git仓库根目录（包含`.git`文件夹）。

### Q5: 出现"Font 'default' does not have a glyph for '\u2212'"警告？
A: 这个问题已在最新版本中解决。我们强制使用ASCII减号而不是Unicode负号。如果仍有问题，请更新到最新版本。

## ⚠️ 已知问题与限制

### 字体相关
1. **某些Linux发行版**：可能需要手动安装中文字体包
   ```bash
   # Ubuntu/Debian
   sudo apt install fonts-wqy-microhei
   
   # Fedora/RHEL
   sudo dnf install wqy-microhei-fonts
   ```

2. **Docker环境**：容器内可能缺少中文字体，需要挂载字体文件

### 性能相关
1. **大型仓库分析**：深度演化分析可能较耗时，建议使用采样功能
2. **内存使用**：分析极大仓库时可能占用较多内存

## 📝 开发指南

### 扩展新的分析维度
1. 在`evolution_analyzer.py`中添加新的分析方法
2. 在`evolution_visualizer.py`中添加对应的可视化方法
3. 在`main.py`中集成新功能

### 添加新的可视化类型
1. 继承或修改`EvolutionVisualizer`类
2. 遵循现有的图表风格和输出格式
3. 确保图表清晰易懂，支持中文字体

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 🆘 技术支持

### 字体配置问题
如果遇到中文字体无法显示的问题，请按照以下步骤排查：

1. **检查字体配置**：
   ```bash
   python -c "import matplotlib; print('字体列表:', matplotlib.rcParams['font.sans-serif']); print('负号设置:', matplotlib.rcParams['axes.unicode_minus'])"
   ```

2. **手动配置字体**（可选）：
   编辑 `font_config.py` 文件，修改字体路径或添加系统可用字体

3. **重新安装matplotlib**：
   ```bash
   pip install --upgrade matplotlib
   ```

### 报告问题
遇到其他问题？请：
1. 在GitHub Issues中报告问题
2. 提供操作系统信息、Python版本和错误日志
3. 如果可能，提供测试仓库的链接

## 📄 许可证

本项目基于 Academic License 发布，仅用于学习和研究目的。

## 🙏 致谢

- 感谢《开源软件基础》课程提供的学习机会
- 感谢所有开源软件库的贡献者
- 特别感谢GitPython、Matplotlib、LibCST等优秀开源项目
- 感谢Windows字体系统提供的稳定中文字体支持

---

**更新日志**：
- 2025-12-21: 彻底解决Windows系统中文字体显示问题和负号警告问题
- 2025-12-20: 添加智能字体配置系统，支持跨平台中文字体自动检测
- 2025-12-15: 初始版本发布，支持基础Git仓库分析和深度演化分析

**提示**: 本工具旨在帮助开发者更好地理解项目演化规律，不应用于商业用途或侵犯他人隐私。使用前请确保你有权分析目标Git仓库。