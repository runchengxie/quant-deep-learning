# End-to-End Quantitative Learning: Candidate Roadmap

Recorded: 2026-11-22. These are research hypotheses and documentation tasks, not new experimental results or a replacement for the [AgentX M0–M9 roadmap](topk-agentx-research-roadmap.md). See the [landscape](end-to-end-quant-landscape.md) and [source ledger](../references/end-to-end-quant-papers.md).

The current [project status](../project-status.md) and milestone entry gates determine execution order. Finish the existing daily task-weight decision before considering a small cost-aware ranking study. Do not expand capacity, start RL, or read locked 2026 data because an item appears here.

## Candidate register

Priority indicates the order in which to develop proposals after existing work, not authorization or readiness to run. All rows are untested local hypotheses. Owner: project owner and research maintainers; experiment owner and resource budget must be assigned before promotion to Ready.

| ID / priority | Hypothesis and matched comparator | Entry condition / state | Evidence needed and stop condition |
|---|---|---|---|
| E2E-01 / P0 | Cost-aware Top-K loss improves net active return over pointwise and ordinary pairwise loss | Proposed; attach to M6, after its M4/M5 evidence gate and task-weight decision | Same features/dates/evaluator; stop if turnover savings consume gross gain or multi-window gains fail |
| E2E-02 / P0 | A small weight head over frozen embeddings improves a matched Top-K portfolio | Proposed; requires a frozen cache, feasible weight/holdings contract and evaluator parity | Compare Top-K, score-based constrained allocation and learned weights; stop on infeasibility, concentration or unstable net gains |
| E2E-03 / P1 | Multi-day representations add persistent information | Existing plan; reuse M7 rather than a duplicate experiment | Compare daily factors, same-day embedding and TCN/GRU sequences; apply M7 purge/embargo and stop gates |
| E2E-04 / P1 | Past-only regime conditioning improves worst-window stability | Research hypothesis; needs training-only regime definition | Fixed encoder with/without conditioning; stop if gains rely on hindsight regimes or one window |
| E2E-05 / P1 | Dated cross-stock relationships add information beyond sector/risk controls | Data preparation; requires historical classifications/edges | No graph, static graph and dynamic graph at matched budget; stop if exposures or coverage explain gains |
| E2E-06 / P2 | A sequential policy improves decisions beyond supervised weight learning | Backlog; requires E2E-02 baseline and audited transition/fill/cost model | No-trade/equal-weight/Top-K/weight-head controls; stop if gains disappear under plausible cost/fill stress |
| E2E-07 / P2 | Pretrained time-series representations add return information | Literature watch; requires pretraining cutoff/overlap audit and license | Frozen encoder vs linear/tree/MLP at matched input; stop on leakage or absent multi-window increment |
| E2E-08 / P2 | News/filings add information beyond market features | Data preparation; publication/availability timestamps and revisions required | Price-only/text-only/fusion, including missing-text controls; stop if timing/coverage explain gains |
| E2E-09 / P2 | A representation transfers from A shares to U.S. stocks | Backlog; independently audited/licensed U.S. dataset required | Local-only vs transfer with equal target-market information; stop on negative transfer or dependence on one regime |

E2E-06 includes cost-aware and offline RL as candidates, not a commitment to PPO/SAC/TD3. Historical market replay with an on-policy learner is not automatically offline RL: a true offline-RL proposal must specify the logged state/action/reward distribution, behavior-policy support and out-of-distribution action controls. Sharpe is a path statistic; a proposal must justify any step reward or differentiable surrogate rather than assigning the same window Sharpe to each action.

## First portfolio-learning proposal

E2E-02 asks whether the objective contributes value with the input information fixed. Freeze one existing encoder per seed; do not average embedding coordinates across independently trained seed spaces. Begin with a small head and no encoder fine-tuning. Target weights must include current drifted holdings and explicit cash/universe handling. A softmax alone does not enforce turnover, tradability, capacity or concentration limits.

Use the same stock-day intersection, executable return definition, entry/exit times, benchmark, gross exposure and historical eligibility for all comparators. Reuse the [M1 evaluator contract](topk-agentx-m1-portfolio-evaluator.md); if it cannot evaluate arbitrary weights, specify and validate that extension first instead of claiming current support. Training surrogates for turnover/cost must be compared with realized evaluator outputs. No numerical acceptance threshold is established by this note: pre-register one before model selection.

## Promotion checklist

- [ ] E2E-01: link the task-weight decision and M6 gate evidence; specify pointwise/pairwise/cost ablations.
- [ ] E2E-02: audit arbitrary-weight evaluation support, drifted holdings, cash, no-fill and constraint handling.
- [ ] E2E-02: write a bounded CPU/single-device head-only proposal with a measured feasibility pilot, maximum runtime/memory, seeds and stop rule.
- [ ] E2E-03: attach any proposal to M7 and its frozen-cache and horizon gates.
- [ ] E2E-04/05: inventory dated regime inputs, sector classifications and relationships without reading locked periods.
- [ ] E2E-06/07/08/09: resolve source/data provenance and admission prerequisites before creating executable experiments.
- [ ] Literature: resolve the source-ledger queue, recording unavailable or contradicted claims explicitly.

For every candidate promoted to Ready, record hypothesis, owner, baseline revision, dataset fingerprint, input availability, split/label protocol, locked-data permissions, primary metric and minimum improvement, risk/capacity guardrails, cost scenarios, compute/storage budget and falsification condition. Formal runs use the existing ExperimentSpec/Registry. Create an implementation issue only when the relevant gates are satisfied; this documentation change creates no issues or runs.

## Evaluation and decisions

Use rolling chronological development windows, training-only normalization, and purging/embargo for overlapping labels. Pre-register a small search budget and retain failed candidates to control selection bias. Choose models and cost settings on validation data; use development OOS only under the existing protocol and never tune repeatedly on the locked period.

Report IC/Rank IC, NDCG/Top-K diagnostics, annualized gross/net/active return, Sharpe with stated annualization and risk-free convention, drawdown, tail risk, one-way turnover, fill/eligibility failures, liquidity/capacity and exposures. Include paired seed/window comparisons, worst windows and uncertainty that accounts for overlapping returns. A single high Sharpe, successful training or synthetic test is insufficient.

States: Literature Review → Research Hypothesis → Proposed → Ready → In Progress → Evaluated → Accepted / Rejected (or Deferred). Only an evaluation record changes a hypothesis into local evidence. Record date, experiment IDs, source revisions, artifacts, decision and next action in the existing registry/log; summarize confirmed status changes in the project status page. This candidate library keeps the rationale and links, avoiding a second status ledger.
