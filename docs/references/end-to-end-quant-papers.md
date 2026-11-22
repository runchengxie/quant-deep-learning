# End-to-End Quantitative Learning: Source Ledger

Checked: 2026-11-22. This is a selective reading queue derived from an owner-supplied discussion. The conversation is provenance for the questions, not a bibliographic or empirical authority. See the [landscape](../research/end-to-end-quant-landscape.md) and [candidate roadmap](../research/end-to-end-research-roadmap.md).

Verification levels: **metadata** confirms a bibliographic record; **abstract** also checks the stated method/scope against the primary abstract; **full reading** checks methods, sample and reported results; **reproduced** requires linked local real-data evidence. These levels do not measure investment merit. No new source below is marked fully read or reproduced by this update.

## Checked anchors

### GKX-2020

Shihao Gu, Bryan Kelly and Dacheng Xiu. *Empirical Asset Pricing via Machine Learning*. Review of Financial Studies 33(5), 2223–2273 (2020). [DOI: 10.1093/rfs/hhaa009](https://doi.org/10.1093/rfs/hhaa009). Level: metadata and publisher abstract/search record; publisher full page unavailable in this check.

Scope: comparative machine learning for empirical asset pricing. Use as the U.S. return-prediction baseline reference, not direct portfolio-policy evidence. Full reading remains needed before importing sample counts, network-depth rankings or numerical investment results. No author-code URL verified in this update.

### MASTER-2024

Tong Li, Zhaoyang Liu, Yanyan Shen, Xue Wang, Haokun Chen and Sen Huang. *MASTER: Market-Guided Stock Transformer for Stock Price Forecasting*. AAAI 2024; preprint submitted 2023. [Primary abstract](https://arxiv.org/abs/2312.15235), [DOI: 10.1609/aaai.v38i1.27767](https://doi.org/10.1609/aaai.v38i1.27767). Level: abstract.

Market information guides feature selection, with alternating intra-stock and inter-stock aggregation for cross-time correlations. This supports studying cross-stock attention, not a claim of guaranteed tradable alpha or explicit graph superiority. Exact universes, costs and implementation parity await full reading. No code URL verified here.

### AlphaStock-2019

Jingyuan Wang, Yang Zhang, Ke Tang, Junjie Wu and Zhang Xiong. *AlphaStock: A Buying-Winners-and-Selling-Losers Investment Strategy using Interpretable Deep Reinforcement Attention Networks*. KDD 2019. [Primary abstract](https://arxiv.org/abs/1908.02646), [DOI: 10.1145/3292500.3330647](https://doi.org/10.1145/3292500.3330647). Level: abstract.

The authors combine Sharpe-oriented RL and cross-asset attention and report experiments on U.S. and Chinese markets. This is author-reported historical evidence; exact costs, splits and executable shorting assumptions remain to be read. No code URL verified here.

### FinRL-Meta-2022

Xiao-Yang Liu et al. *FinRL-Meta: Market Environments and Benchmarks for Data-Driven Financial Reinforcement Learning*. NeurIPS 2022 Datasets and Benchmarks. [Primary abstract and full author list](https://arxiv.org/abs/2211.03107), [official library](https://github.com/AI4Finance-Foundation/FinRL-Meta). Level: abstract.

An environment/benchmark infrastructure reference that explicitly identifies low signal-to-noise, survivorship bias and backtest overfitting as challenges. It is not proof that any RL algorithm beats this project's baselines. A future comparison must pin the library revision and actual environment/data contract.

### DiffOpt-2019

Akshay Agrawal, Brandon Amos, Shane Barratt, Stephen Boyd, Steven Diamond and J. Zico Kolter. *Differentiable Convex Optimization Layers*. NeurIPS 2019. [Author-hosted record and paper](https://web.stanford.edu/~boyd/papers/diff_cvxpy.html), [preprint](https://arxiv.org/abs/1910.12430). Level: abstract/author record.

Technical basis for differentiating through constrained optimization. It provides an alternative to an unconstrained weight head; it does not establish stock-selection profitability. Portfolio-specific solver behavior and gradient/cost approximations need separate validation.

### DeepLOB-2019

Zihao Zhang, Stefan Zohren and Stephen Roberts. *DeepLOB: Deep Convolutional Neural Networks for Limit Order Books*. IEEE Transactions on Signal Processing 67(11), 2019. [Primary abstract, arXiv v6](https://arxiv.org/abs/1808.03668), [DOI: 10.1109/TSP.2019.2907260](https://doi.org/10.1109/TSP.2019.2907260). Level for this update: abstract; prior detailed reading is preserved in [existing notes](deeplob-paper-notes.md).

CNN/LSTM order-book forecasting with benchmark and London Stock Exchange experiments. Keep its scope separate from next-day A-share evidence. Use the [reproduction audit](../reproduction-audit.md) for actual local implementation and experiment status.

## Tools, not empirical results

[Microsoft Qlib](https://github.com/microsoft/qlib) is an official open-source research platform and a source of comparison implementations. Its repository was checked on the date above. A future experiment must pin a commit, feature definition, universe, split and tuning budget; importing a benchmark table does not establish a fair comparison. No dependency is added by this review.

## Unverified leads from the discussion

Retain these as retrieval tasks. A failed fetch or absent search match does not prove a paper is false. Resolve title/authors/date from a primary record, then read the actual sample, target, baselines, costs and limitations before promoting claims. Do not repeat the discussion's numbers as findings.

| Lead / supplied identifier | Unverified part / next action |
|---|---|
| *Can Deep Reinforcement Learning Beat 1/N?*, [10.1016/j.frl.2025.106866](https://doi.org/10.1016/j.frl.2025.106866) | Publisher redirect inaccessible; verify title/authors and the claimed seven datasets, 300+ OOS years and 0.1% cost result |
| Chinese direct-weight study, [10.12011/SETP2023-1784](https://doi.org/10.12011/SETP2023-1784) | DOI page inaccessible; verify authors, year, original title, Chinese-market scope and friction findings |
| Transformer vs simple networks, [10.1016/j.frl.2025.108783](https://doi.org/10.1016/j.frl.2025.108783) | Verify 1957–2021 sample, 920 features, horizons and MSE versus net returns |
| Chinese latent-factor model, [10.1016/j.frl.2025.108519](https://doi.org/10.1016/j.frl.2025.108519) | Retrieve primary metadata and actual experiment scope |
| LOBFrame guide, [10.1080/14697688.2025.2522911](https://doi.org/10.1080/14697688.2025.2522911) | Verify NASDAQ data, code provenance and executable-signal evaluation |
| A-share price formation, [10.1016/j.pacfin.2025.103029](https://doi.org/10.1016/j.pacfin.2025.103029) | Verify publication date, sample and engineered-vs-raw feature claim |
| Equity LLM survey, [supplied PMC record](https://pmc.ncbi.nlm.nih.gov/articles/PMC12421730/) | Verify 84-study count, inclusion criteria and evidence limits |
| Multimodal survey, [10.1016/j.inffus.2026.104249](https://doi.org/10.1016/j.inffus.2026.104249) | Verify primary metadata and conclusions |
| Return-forecasting foundation-model preprint, [arXiv:2606.27100](https://arxiv.org/abs/2606.27100) | Verify title, version, five-stock sample and random-walk comparison |
| *Time Series Foundation Models for Financial Forecasting*; *Foundation Models Do Not Beat Simple Volatility Benchmarks* | No stable identifiers supplied; locate primary records before repeating 19-instrument or ~5,000-stock/HAR-RV claims |
| 2026 OFR forecasting benchmark; Financial Innovation A-share comparison; Discover Computing review | Titles/authors/identifiers missing; locate records before using dates, sample counts or conclusions |
| 2026 equity-RL review; ACM digital-asset portfolio review; 2024 Chinese interpretable portfolio study; 2024 execution-probability study | Bibliographic details incomplete; verify the claimed 156/119-study counts and methods independently |

## Reading record template

For each promoted source, retain stable ID, full citation, version and retrieval date, primary URL/DOI, author code URL and pinned revision if used, market/universe/sample dates, frequency/target, point-in-time controls, splits/purge/embargo, baselines and tuning budget, trading rules/costs, reported metrics, uncertainty, limitations, precise page/table locator, local experiment links and next question. Mark unavailable information explicitly. Bibliographic verification, author-reported results and local reproduction remain separate fields.
