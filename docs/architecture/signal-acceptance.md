# Synthetic signal handoff acceptance

The optional acceptance checks DL export against the installed platform reader, portfolio selection, native position replay, and a Go runtime queue with its installed Python adapter. It is an engineering diagnostic using invented predictions and prices. The queue test executes a real worker against task-only SQLite/artifact/result paths. It does not train a model, establish profitability, or publish live signals.

The standalone package still supports Python 3.10 without platform dependencies. The separate integration project requires Python 3.12 and pins `quant-platform` and `research-contracts` to commit `282afca4c4ca210d46eed096a943972662fede99`. It also pins `quant-backtest-runtime` to `c9493008ad41da4391db38542528a4ccbe385b73`. Tests check installed `direct_url.json` provenance and the Go binary's source revision before exercising those APIs.

Build the pinned Go executable from a separate runtime checkout, with Go 1.27.3.
Keep the binary outside either source tree. From that checkout, after verifying
`git rev-parse HEAD` equals the runtime pin:

```bash
go build -trimpath -mod=readonly \
  -ldflags "-X github.com/runchengxie/quant-backtest-runtime/internal/app.SourceRevision=c9493008ad41da4391db38542528a4ccbe385b73" \
  -o /absolute/external/backtest-job ./cmd/backtest-job
```

Then from this repository root:

```bash
BACKTEST_GO_EXECUTABLE=/absolute/external/backtest-job \
uv run --project integration/signal-acceptance --locked pytest -c integration/signal-acceptance/pyproject.toml integration/signal-acceptance -q
```

Use a separate `UV_PROJECT_ENVIRONMENT` when an existing environment must remain unchanged. The separate `signal-acceptance` CI job builds that exact Go source and runs all acceptance tests without skips on pull requests and main pushes. Its lock constrains pandas to version 2 and NumPy below 2.4: pandas 3.1 warns on the pinned provider's `inplace` operations, and NumPy 2.5 warns on pandas 2 timedelta conversion. Warnings remain errors; these constraints apply only to this diagnostic. The integration lock selects CPU PyTorch; this does not change training configuration or the standalone lock.

## What is checked

The source is a formal prediction artifact with explicit dataset metadata. Export produces only the eleven canonical signal columns; future label dates and returns remain in the source. `signal_date` remains the information date. Friday signals enter on the next priced session, Monday, and replay exits Tuesday. Two higher-scoring ineligible names are filtered before Top-K selection; tied eligible names select deterministically. An open price of 100 followed by 110 produces a 0.10 return with zero costs. Orders and fills remain empty because this is position-level replay.

The default unit suite checks duplicate stock-days, nonfinite predictions, source-overwrite prevention, model/input/dataset/source identity mismatch, and changed signal bytes or manifest identity. Existing formal-artifact validation also checks source date ordering and metadata before export.

Declared prediction versions are checked before export: `ticknet.prediction_schema_version`
may be absent for historical artifacts, or contain UTF-8 `ticknet.research.predictions.v1`.
Unknown, blank or malformed declarations fail before writing signals or their sidecar.
This guard does not add a checkpoint protocol or change the existing unversioned writer.

## Runtime acceptance scope

The queue consumes a schema-v1 diagnostic request with content-addressed positions,
prices and periods produced by the same eligibility/next-session selection path.
Planning leaves the task database absent; queued submission is idempotent; the
one-slot scheduler executes the installed Python compatibility adapter and publishes
`ticknet.backtest_job_result.v1`. The test checks request/result hashes, selected
symbol, 0.10 return and empty orders/fills. Changed input bytes fail before creating
job state; changed published bytes fail result verification.

This certifies the tested v1 compatibility path at the exact three provider pins.
It does not certify native Rust v5-v7 execution, a full model/checkpoint protocol,
a research-clock-aware v2 job, real-data results, production deployment, or semantic
parity between independent DL and private research models. The runtime receives
positions, not model Python modules or raw prediction artifacts. Receipt validation
and eligibility filtering remain producer-side handoff steps.

## Receipt and trust boundary

`export_alpha_signal_artifact` keeps its existing return fields and adds `manifest_path`. The sidecar `<output-stem>.manifest.json` uses `ticknet.alpha-signal-manifest.v1`, binding signal bytes, source prediction SHA-256, dataset fingerprint, model version, feature-set identifier, row count, and date semantics. Export retains its previous replace-existing-output behavior, but refuses to overwrite its source with either the signal or sidecar. Callers must choose an isolated output location; concurrent writers to one output are unsupported.

Before invoking a consumer, call `verify_alpha_signal_artifact` with `expected_source_sha256`, `expected_model_version`, `expected_feature_set_id`, and `expected_dataset_fingerprint` from a trusted run record. It checks the receipt, signal digest, row count, embedded model/input columns and dataset metadata. Source-byte verification requires the caller to compute the expected digest from the source it intends to use.

These hashes provide integrity checks, not signatures or proof that arbitrary model names are truthful. An actor able to replace both data and receipt can regenerate their hashes; retain the exported signal digest in a trusted external record when authenticity matters. The acceptance does not establish a universal model/checkpoint manifest or automatic compatibility with other provider revisions.

The platform reader validates the signal schema but does not apply eligibility. The acceptance explicitly filters `eligible_for_backtest` before portfolio construction. Consumers must preserve that step. Live eligibility remains false by default; this diagnostic never enables it.
