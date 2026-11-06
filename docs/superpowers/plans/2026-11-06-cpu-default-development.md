# CPU-default development implementation plan

> **For agentic workers:** Use superpowers:executing-plans for inline execution. Steps use checkbox syntax.

**Goal:** Make ordinary uv development CPU-only while retaining an explicit GPU environment.

**Architecture:** Mutually exclusive CPU/GPU dependency groups select torch sources; published torch remains mandatory. Behavioral tests exercise real offline uv exports. Existing model code is unchanged.

**Tech Stack:** Python 3.10+, uv 0.13.7, pytest, TOML, English/Chinese Markdown.

**Spec:** [Approved design](../specs/2026-11-06-cpu-default-development-design.md).

## Global constraints

- Default uv selection is CPU; explicit GPU selection must not share its environment.
- Keep mandatory torch and Python 3.10+ metadata; avoid unrelated upgrades.
- Preserve research and production boundaries. Store private validation records outside Git.

## Review focus

- Ordinary uv run must not undo CPU selection: inspect a fresh repeated sync dry-run.
- Conflicting selections must fail before installation: test real uv exports.
- Python 3.10 needs its compatible torch branch: inspect the universal lock and validate with its interpreter.
- macOS must not be forced onto unavailable CPU-index wheels: preserve platform fallback.
- GPU users must consistently select GPU and a separate environment: document sync and run commands together.

### Task 1: Environment selection and documentation

**Files:** `pyproject.toml`, `uv.lock`, `tests/test_documentation.py`, `README.md`, `README.zh-CN.md`, `docs/operations/development-guide.md`.

**Interfaces:** default CPU exports; explicit `--no-group cpu --group gpu` exports; conflicting CPU/GPU exports reject. No model API changes.

- [x] Write real uv-export tests for default CPU, explicit GPU, conflict rejection and mandatory wheel metadata.
- [x] Run the default CPU regression against main and observe its CUDA dependencies (RED).
- [x] Add minimal per-group source configuration and regenerate the lock without unrelated upgrades.
- [x] Run behavioral tests (GREEN), inspect Python 3.10 and platform branches.
- [x] Document supported CPU/GPU commands in aligned quick starts and the development guide.
- [ ] Install the default CPU environment; run all required Python and web checks. Inspect repeated locked sync and GPU selection dry-runs.
- [ ] Commit using the public contributors/noreply identity; run an independent whole-branch review and address material findings.

### Task 2: Delivery and task cleanup

**Files:** private maintenance receipts only; GitHub PR and current target branch.

- [ ] Verify actual push destination and outgoing commits, push to the user's repository and open a PR.
- [ ] Validate current target/combined result, wait for required checks, then merge under the standing integration authorization.
- [ ] Verify main and task-related Pages deployment, clean only this task's remote/local branch and worktree, and retire this task's temporary environments/caches while retaining records.

## Execution record

This is the implementation plan, not the delivery status record. The approved design is implemented inline; the PR records completed validation and integration. The private ledger records source revisions, actual commands/results and rulings.
