# End-to-End Quantitative Learning: Research Landscape

Recorded and source-checked: 2026-11-22. This is a selective research map, not an exhaustive survey of publications through that date. It records the questions raised in the owner's research discussion without treating the supplied conversation as a source of empirical evidence.

The useful near-term question is whether changing the learning objective improves executable, after-cost portfolios with the same information. More model capacity, attention layers, or a positive prediction IC do not establish this. The [project status](../project-status.md), reviewed on 2026-10-07, remains authoritative for local results; this note does not refresh that review or report new experiments.

Read the [candidate roadmap](end-to-end-research-roadmap.md) for priorities and entry gates and the [source ledger](../references/end-to-end-quant-papers.md) for verification depth and unresolved citations.

## What “end-to-end” means

| Level | Learned input → output | What must still be evaluated |
|---|---|---|
| Prediction | Market features → return, direction, or cross-sectional score | A separate portfolio rule and its trading costs |
| Portfolio | Features and holdings → target weights | Feasibility, turnover, risk and realized execution |
| Trading policy | State and holdings → trades or orders | Fill assumptions, liquidity, impact and sequential risk |
| Full investment process | Available multimodal information → executable decisions | Every data timestamp, constraint and execution boundary |

These are task definitions, not a maturity ranking. A system may be modular in deployment and still train several stages jointly. A differentiable constrained optimizer can sit inside a learned portfolio pipeline; direct unconstrained weight prediction is not the only approach. Reinforcement learning (RL) is one training method, not a synonym for end-to-end learning.

## Research routes

| Route | Current evidence anchor | Connection to this project | Main open question |
|---|---|---|---|
| Supervised return/rank prediction | [Gu, Kelly and Xiu](../references/end-to-end-quant-papers.md#gkx-2020); [MASTER](../references/end-to-end-quant-papers.md#master-2024) | HGB/LambdaMART, minute and event-stream models | Does extra structure improve net portfolios across windows? |
| Direct portfolio learning | [Differentiable optimization layers](../references/end-to-end-quant-papers.md#diffopt-2019) establish a technical mechanism, not stock alpha | Small weight head or constrained layer over frozen features | Does a portfolio objective beat a matched score-to-Top-K pipeline? |
| Sequential portfolio RL | [AlphaStock](../references/end-to-end-quant-papers.md#alphastock-2019); [FinRL-Meta](../references/end-to-end-quant-papers.md#finrl-meta-2022) | Deferred policy research after evaluator gates | Is the apparent gain robust to costs and simulator errors? |
| Cross-stock and regime learning | MASTER uses market-guided intra/inter-stock attention | Conditional prediction or dated relationship features | Incremental information or repackaged sector/risk exposure? |
| Multimodal learning | Literature/data preparation candidate; no verified local result | Point-in-time news/filing encoders added to a fixed baseline | Does text add information after timing and coverage controls? |
| Time-series foundation models | Literature watch; claimed recent comparisons remain unverified here | Frozen encoder before any fine-tuning | Increment over linear/tree/small-network baselines on returns? |
| LOB prediction and execution | [DeepLOB](../references/end-to-end-quant-papers.md#deeplob-2019) | Separate FI-2010 reproduction and A-share L2 research | Can predictive accuracy support feasible fills and net trading? |

MASTER is a Transformer with cross-stock aggregation; it should not be presented as evidence that an explicit GNN is superior. General time-series forecasting architectures such as PatchTST and iTransformer are candidates, not demonstrated stock-selection improvements in this repository. Likewise, volatility, price-level and return forecasting are different targets and cannot share a model leaderboard.

## Markets and transfer limits

A-share research is the primary experimental scope. Protocols must represent dated universe membership, delistings, point-in-time financial releases, suspensions, trading eligibility, price limits, applicable settlement/shorting rules, fees and capacity. The exact venue, instrument and historical rule version belong in the experiment contract; this note does not establish a universal fee or rule schedule.

U.S. equities are a possible external validation market, not an existing local capability. Long-history asset-pricing studies and LOB studies use different samples, frequencies and assumptions. Corporate actions, historical constituents, delisted names, data licenses, trading calendars and borrow costs need their own audit before transfer claims.

European equities have a verified LOB example in DeepLOB's London Stock Exchange experiments. FX, futures and digital assets remain optional comparison domains: financing/carry, contract rolls and margin, or venue-specific continuous trading require separate protocols. Their results would not validate A-share stock selection.

## Local evidence and ownership

The [AgentX roadmap](topk-agentx-research-roadmap.md) and [trading diagnostics](eventstream-signal-trading-diagnostics.md) already document the gap between ranking information and net active returns. They also retain negative findings and paused capacity expansion. This is the motivation for objective and holding-policy research, not proof that direct weight learning or RL will solve it.

M6 neural ranking and M7 multi-day embeddings retain their existing entry gates. Daily task weighting remains ahead of a new cost-aware objective in the current work order. This topic library neither starts a training run nor opens locked 2026 data.

Under the [repository boundary](../architecture/repository-boundaries.md), this repository owns learned representations, model training, policy research and evidence. Upstream data remains with the market-data provider; general execution, replay and runtime services remain downstream. Joint training does not require moving those implementations here.

## Interpretation limits

No formal maturity scores, industry adoption estimates or live-profitability claims are established by this review. The source ledger distinguishes checked abstracts/metadata from full reading and reproduction. Unchecked 2025–2026 numerical claims from the discussion remain leads, including the SAC-versus-1/N result and recent foundation-model benchmarks. They must not support experiment acceptance decisions until their samples, methods and numbers are verified.
