# Signal acceptance implementation plan

> **For agentic workers:** Use superpowers:executing-plans; execute with TDD.

**Goal:** Verify synthetic DL signal export against an installed immutable platform consumer and native position replay.

**Architecture:** Keep the standalone producer independent. Add an additive versioned digest manifest and an identity-checking verifier. A separate Python 3.12 integration project pins the actual platform and shared contracts packages; it reads exported Parquet, explicitly filters eligibility, builds next-session positions and runs native replay.

**Tech Stack:** Python, PyArrow, pytest, uv, optional quant-platform.

**Spec:** User-approved synthetic producer-to-consumer scope, recorded in [repository boundaries](../../architecture/repository-boundaries.md).

## Global constraints

- No real data, training, runtime jobs, publication, or production changes.
- Preserve default Python >=3.10 and standalone dependencies.
- Existing export result remains compatible; manifest is additive.
- Reject duplicate keys, nonfinite predictions, and artifact/source/model/input identity mismatch.

## Review focus

- Prediction date must remain separate from next-session execution date.
- Ineligible high scores must never become positions.
- Hash verification must use externally expected source and model/input identities.
- Tampered artifact or sidecar must fail before consumer use.
- Installed provenance must match the immutable provider commit.

## Task 1: Producer receipt and validation

Files: `src/ticknet/research/alpha_signal_adapter.py`, `tests/test_alpha_signal_adapter.py`.

- [x] Write failing tests for direct-builder duplicate/nonfinite rejection and export/verification identity and tamper checks.
- [x] Run focused pytest and confirm missing behavior fails.
- [x] Implement additive manifest and fail-closed verifier with externally supplied expected source SHA-256, model version, feature set and dataset fingerprint.
- [x] Run focused tests and full repository gates.

## Task 2: Installed consumer acceptance

Files: `integration/signal-acceptance/{pyproject.toml,uv.lock,ty.toml,test_signal_acceptance.py}`, `docs/architecture/signal-acceptance.md`, documentation index and boundary guide.

- [x] Add separate locked optional project and synthetic test using actual installed APIs.
- [x] Verify provider provenance, canonical read, eligibility filtering, next-session entry, deterministic selection and numerical replay return.
- [x] Verify signal and source tamper plus identity mismatch failures.
- [x] Record exact commands, provider revision and limitations; commit for parent review.

## Execution record

- RED: direct-builder nonfinite and duplicate cases failed (4 failures); receipt API was absent; source overwrite cases failed (2 failures).
- GREEN: focused producer and documentation suite passed (36 tests), and installed platform native replay passed (1 test, no skips).
- Ruling: keep receipt functions in the existing adapter and tests in its existing test module to preserve the file-count ratchet; no baseline budgets changed.
- Ruling: constrain only the optional diagnostic to pandas 2 and NumPy <2.4 after real replay exposed provider/pandas deprecations with pandas 3.1 and NumPy 2.5; warnings remain errors.
- Validation logs and task environments are external to this repository. Final full-suite and CI results are reported with the reviewed revision.
- Final review: fixed deterministic source overwrite through existing hard links for either output or sidecar; both regression cases failed before file-identity guards were added. Also corrected two optional integration test annotations exposed by the separate type check.
- Final review scope: production publication, model profitability, concurrent output writers, adversarial replacement of both receipt and artifact, and other provider revisions remain outside this synthetic diagnostic. Standalone additions preserve Python 3.10 syntax; this task does not claim a Python 3.10 runtime test.
