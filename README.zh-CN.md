# Quant Deep Learning

[English README](README.md)

Quant Deep Learning 是面向结构化市场数据的独立深度学习研究项目。项目从 DeepLOB 复现起步，目前重点研究利用 A 股盘口快照、分钟数据和 L2 事件流进行次日横截面预测。

本项目维护模型输入表示、训练、推理、评估和研究记录，可以不安装 `quant-platform` 或 `quant-research` 独立运行。上游 `quant-market-data-platform` 提供数据，下游 `quant-backtest-runtime` 消费发布的产物，双方无需导入本项目的 Python 模块。详见[仓库边界](docs/architecture/repository-boundaries.md)。

## 研究方向

- 原始盘口模型使用预测时点可获得的十档快照。
- 分钟模型研究计算成本较低的价量聚合输入。
- 事件流模型用因果序列模型编码委托、成交和快照事件。
- 研究工具记录实验身份、成本评估、预测审计和锁定数据的访问边界。
- 筹码分层研究提供 CPU HGB 实验路径，使用滞后的筹码年龄摘要，并与分钟特征做配对比较。[来源与契约](docs/research/chip-age-hgb.md) 区分合成数据工程检查、真实训练和券商方法复现。项目不会未经许可转发券商报告。

各方向的证据阶段不同。带日期的结果、局限和研究问题以[项目状态](docs/project-status.md) 为准。

## 研究边界

FI-2010 DeepLOB 论文复现在 `ticknet.fi2010` 中独立维护，不能证明次日选股有效。`ticknet.nextday` 和 `ticknet.eventstream` 的结果与 FI-2010 复现分开记录。

主线按交易日切分数据，在时间外样本评估横截面排序，并检查换手和交易成本。Rank IC 为正不等于信号具备交易价值。只有文档证据支持时，才能宣称完成复现或验证。

## 快速开始

`pyproject.toml` 声明支持 Python 3.10 及以上版本。当前公开 CI 使用 Python 3.12，未在 CI 中验证其他版本。合成数据检查无需私有行情、GPU 或 `quant-platform`。

```bash
uv sync --locked --extra dev
uv run python scripts/check.py
```

脚本运行 Ruff、格式检查、`ty`、pytest 覆盖率和合成 DeepLOB/FI-2010 冒烟检查。CI 是必需门禁，无需安装 Git hook。完整检查范围见[开发指南](docs/operations/development-guide.md)。

Windows PowerShell 可用 `.\.venv\Scripts\Activate.ps1` 激活环境。修改 `pyproject.toml` 的命令入口后，重新以 editable 模式安装项目，更新环境中的启动脚本。

## 文档

- [交互概念示例](https://runchengxie.github.io/quant-deep-learning/concepts/) 用合成数据解释市场事件。
- [研究展示站](https://runchengxie.github.io/quant-deep-learning/) 提供样本范围、图表、局限和技术记录链接。
- [技术文档](https://runchengxie.github.io/quant-deep-learning/documentation/) 与[公开记录搜索](https://runchengxie.github.io/quant-deep-learning/search/)。
- [项目状态](docs/project-status.md)、[模型目录](docs/model-catalog.md)、[横截面预测协议](docs/nextday/cross-sectional-prediction.md)。
- [事件流指南](docs/nextday/eventstream.md)、[数据边界](docs/architecture/data-boundary.md)、[仓库边界](docs/architecture/repository-boundaries.md)。
- [文档索引](docs/documentation-index.md) 与独立 FI-2010 方向的[复现审计](docs/reproduction-audit.md)。

## 目录

```text
src/ticknet/             共享训练工具与兼容模型
src/ticknet/nextday/     次日标签、数据集、分钟模型与原始盘口模型
src/ticknet/eventstream/ L2 打包、因果 Transformer 与预测导出
src/ticknet/research/    提案、执行、审计、注册表与研究智能体
scripts/                 人工运行的数据准备与本地检查入口
tests/                   不依赖私有行情的自动化检查
configs/                 本地与 Colab 配置
docs/                    项目状态、技术指南、路线图与研究记录
docs/references/         论文与阅读笔记
src/ticknet/fi2010/      FI-2010 DeepLOB 复现
docs/archive/           历史工作流文本，现行代码位于 src 和 scripts
```

为兼容保留 Python 导入命名空间 `ticknet`。当前职责见[仓库边界](docs/architecture/repository-boundaries.md)，协作规则见 [AGENTS.md](AGENTS.md)。
