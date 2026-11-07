from __future__ import annotations

import json
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from ticknet.research.alpha_signal_adapter import (
    ALPHA_SIGNAL_COLUMNS,
    build_alpha_signal_table,
    export_alpha_signal_artifact,
    verify_alpha_signal_artifact,
)
from ticknet.research.prediction_contract import attach_formal_prediction_metadata
from ticknet.research.registry import file_sha256


def _formal_table() -> pa.Table:
    return pa.table(
        {
            "symbol": ["BBB", "AAA", "CCC", "DDD"],
            "trading_date": ["2026-01-05"] * 4,
            "label_date": ["2026-01-06"] * 4,
            "return_end_date": ["2026-01-07"] * 4,
            "target_return": [0.01, 0.02, -0.01, 0.03],
            "score": [0.5, 0.9, 0.1, 0.9],
            "can_buy": [True, True, False, True],
            "can_sell": [True, True, True, True],
            "in_universe": [True, True, True, False],
        }
    )


def test_build_alpha_signal_table_uses_prediction_date_and_deterministic_rank() -> None:
    signals = build_alpha_signal_table(
        _formal_table(),
        model_version="eventstream-v1",
        feature_set_id="l2-clean-v1",
    )

    assert signals.column_names == list(ALPHA_SIGNAL_COLUMNS)
    assert signals["signal_date"].to_pylist() == ["20260105"] * 4
    assert signals["symbol"].to_pylist() == ["AAA", "DDD", "BBB", "CCC"]
    assert signals["rank"].to_pylist() == [1, 2, 3, 4]
    assert signals["eligible_for_backtest"].to_pylist() == [True, False, True, False]
    assert signals["eligible_for_live"].to_pylist() == [False] * 4
    assert signals["model_version"].to_pylist() == ["eventstream-v1"] * 4


def test_build_alpha_signal_table_rejects_missing_formal_fields() -> None:
    table = _formal_table().drop(["label_date"])

    with pytest.raises(ValueError, match="label_date"):
        build_alpha_signal_table(table)


@pytest.mark.parametrize("score", [float("nan"), float("inf"), -float("inf")])
def test_builder_rejects_nonfinite_score(score: float) -> None:
    table = _formal_table().set_column(5, "score", pa.array([score, 0.9, 0.1, 0.9]))
    with pytest.raises(ValueError, match="finite"):
        build_alpha_signal_table(table)


def test_builder_rejects_duplicate_stock_day() -> None:
    with pytest.raises(ValueError, match="duplicate"):
        build_alpha_signal_table(pa.concat_tables([_formal_table(), _formal_table().slice(0, 1)]))


def _export(tmp_path: Path) -> tuple[Path, Path, dict]:
    source, output = tmp_path / "predictions.parquet", tmp_path / "signals.parquet"
    table = pa.table(
        {
            "symbol": ["AAA", "BBB", "CCC"],
            "trading_date": ["2026-01-05"] * 3,
            "label_date": ["2026-01-06"] * 3,
            "return_end_date": ["2026-01-07"] * 3,
            "target_return": [0.1, -0.1, 0.0],
            "score": [0.5, 0.9, 1.0],
            "can_buy": [True, False, True],
            "can_sell": [True] * 3,
            "in_universe": [True, True, False],
        }
    )
    pq.write_table(
        attach_formal_prediction_metadata(table, dataset_fingerprint="synthetic-v1"), source
    )
    receipt = export_alpha_signal_artifact(
        source,
        output,
        expected_universe_size=2,
        model_version="model-v1",
        feature_set_id="input-v1",
    )
    return source, output, receipt


def _verify(source: Path, output: Path, **overrides: str) -> dict:
    expected = {
        "expected_source_sha256": file_sha256(source),
        "expected_model_version": "model-v1",
        "expected_feature_set_id": "input-v1",
        "expected_dataset_fingerprint": "synthetic-v1",
    }
    return verify_alpha_signal_artifact(output, **(expected | overrides))


def test_export_persists_bound_identity(tmp_path: Path) -> None:
    source, output, receipt = _export(tmp_path)
    manifest = _verify(source, output)
    assert receipt["manifest_path"] == str(output.with_suffix(".manifest.json").resolve())
    assert manifest["contract"] == "ticknet.alpha-signal-manifest.v1"
    assert manifest["signal_sha256"] == file_sha256(output)
    assert manifest["source_prediction_sha256"] == file_sha256(source)
    assert manifest["signal_date_semantics"] == "trading_date"
    assert manifest["model_version"] == "model-v1"
    assert manifest["feature_set_id"] == "input-v1"
    assert manifest["dataset_fingerprint"] == "synthetic-v1"


@pytest.mark.parametrize(
    "field",
    [
        "expected_source_sha256",
        "expected_model_version",
        "expected_feature_set_id",
        "expected_dataset_fingerprint",
    ],
)
def test_verifier_rejects_wrong_expected_identity(tmp_path: Path, field: str) -> None:
    source, output, _ = _export(tmp_path)
    with pytest.raises(ValueError, match="identity"):
        _verify(source, output, **{field: "wrong"})


def test_verifier_rejects_changed_signal_bytes(tmp_path: Path) -> None:
    source, output, _ = _export(tmp_path)
    output.write_bytes(output.read_bytes() + b"tamper")
    with pytest.raises(ValueError, match="digest"):
        _verify(source, output)


def test_verifier_rejects_changed_manifest_identity(tmp_path: Path) -> None:
    source, output, _ = _export(tmp_path)
    manifest_path = output.with_suffix(".manifest.json")
    manifest = json.loads(manifest_path.read_text())
    manifest["model_version"] = "other"
    manifest_path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="identity"):
        _verify(source, output)


@pytest.mark.parametrize("source_is_manifest", [False, True])
def test_export_rejects_overwriting_source(tmp_path: Path, source_is_manifest: bool) -> None:
    source, _output, _ = _export(tmp_path)
    target = source.with_suffix(".parquet")
    if source_is_manifest:
        target = tmp_path / "other.parquet"
        source.rename(target.with_suffix(".manifest.json"))
        source = target.with_suffix(".manifest.json")
    before = source.read_bytes()
    with pytest.raises(ValueError, match="overwrite"):
        export_alpha_signal_artifact(source, target, expected_universe_size=2)
    assert source.read_bytes() == before


@pytest.mark.parametrize("alias_is_manifest", [False, True])
def test_export_rejects_hard_link_to_source(tmp_path: Path, alias_is_manifest: bool) -> None:
    source, _output, _ = _export(tmp_path)
    target = tmp_path / "linked.parquet"
    alias = target.with_suffix(".manifest.json") if alias_is_manifest else target
    alias.hardlink_to(source)
    before = source.read_bytes()
    with pytest.raises(ValueError, match="overwrite"):
        export_alpha_signal_artifact(source, target, expected_universe_size=2)
    assert source.read_bytes() == before
    if alias_is_manifest:
        assert not target.exists()


def test_unknown_prediction_version_is_rejected_before_signal_publication(tmp_path: Path) -> None:
    source, output = tmp_path / "predictions.parquet", tmp_path / "signals.parquet"
    table = attach_formal_prediction_metadata(_formal_table(), dataset_fingerprint="synthetic")
    metadata = dict(table.schema.metadata or {})
    metadata[b"ticknet.prediction_schema_version"] = b"ticknet.research.predictions.v2"
    pq.write_table(table.replace_schema_metadata(metadata), source)
    source_hash = file_sha256(source)
    with pytest.raises(ValueError, match="schema version"):
        export_alpha_signal_artifact(
            source,
            output,
            expected_universe_size=3,
            model_version="synthetic",
            feature_set_id="synthetic",
        )
    assert not output.exists()
    assert not output.with_suffix(".manifest.json").exists()
    assert file_sha256(source) == source_hash
