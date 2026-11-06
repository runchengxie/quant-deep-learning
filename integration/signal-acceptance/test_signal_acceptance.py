"""Synthetic producer -> installed platform -> native replay (no runtime worker)."""

from __future__ import annotations

import json
from importlib.metadata import distribution
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pytest
from alpha_research.signal_artifact import read_signal_artifact
from portfolio_backtester.portfolio_positions import build_positions_by_rebalance
from portfolio_backtester.position_backtest import PositionBacktestConfig
from portfolio_backtester.position_replay import (
    build_position_replay_periods,
    run_native_position_replay,
)

from ticknet.research.alpha_signal_adapter import (
    export_alpha_signal_artifact,
    verify_alpha_signal_artifact,
)
from ticknet.research.prediction_contract import attach_formal_prediction_metadata
from ticknet.research.registry import file_sha256

PLATFORM_COMMIT = "282afca4c4ca210d46eed096a943972662fede99"


def test_export_to_installed_platform_native_replay(tmp_path: Path) -> None:
    for package in ("quant-platform", "research-contracts"):
        provenance = json.loads(distribution(package).read_text("direct_url.json") or "{}")
        assert provenance["vcs_info"]["commit_id"] == PLATFORM_COMMIT
        assert provenance["url"] == "https://github.com/runchengxie/quant-platform.git"

    source, output = tmp_path / "predictions.parquet", tmp_path / "signals.parquet"
    table = pa.table(
        {
            "symbol": ["AAA", "BBB", "CCC", "DDD"],
            "trading_date": ["2026-01-09"] * 4,
            "label_date": ["2026-01-12"] * 4,
            "return_end_date": ["2026-01-13"] * 4,
            "target_return": [0.1, -0.1, 0.0, 0.0],
            "score": [0.5, 0.5, 1.0, 2.0],
            "can_buy": [True, True, False, True],
            "can_sell": [True] * 4,
            "in_universe": [True, True, True, False],
        }
    )
    pq.write_table(
        attach_formal_prediction_metadata(table, dataset_fingerprint="synthetic-v1"), source
    )
    export_alpha_signal_artifact(
        source,
        output,
        expected_universe_size=3,
        model_version="synthetic-model-v1",
        feature_set_id="synthetic-input-v1",
    )
    manifest = verify_alpha_signal_artifact(
        output,
        expected_source_sha256=file_sha256(source),
        expected_model_version="synthetic-model-v1",
        expected_feature_set_id="synthetic-input-v1",
        expected_dataset_fingerprint="synthetic-v1",
    )
    assert manifest["rows"] == 4
    signals = read_signal_artifact(output)
    assert set(signals["signal_date"]) == {"20260109"}
    assert not signals["eligible_for_live"].any()
    assert not {"target_return", "label_date", "return_end_date"} & set(signals.columns)
    # The platform reader validates the wire schema; this handoff owns eligibility.
    eligible = signals.loc[signals["eligible_for_backtest"]].copy()
    eligible["trade_date"] = pd.to_datetime(eligible["signal_date"], format="%Y%m%d")
    pricing = pd.DataFrame(
        [
            (day, symbol, price)
            for day, price in [("2026-01-09", 1.0), ("2026-01-12", 100.0), ("2026-01-13", 110.0)]
            for symbol in ["AAA", "BBB", "CCC", "DDD"]
        ],
        columns=["trade_date", "symbol", "open"],
    )
    pricing["trade_date"] = pd.to_datetime(pricing["trade_date"])
    positions = build_positions_by_rebalance(
        eligible,
        pred_col="signal_backtest",
        price_col="open",
        top_k=1,
        rebalance_dates=[pd.Timestamp("2026-01-09")],
        shift_days=1,
        pricing_data=pricing,
    )
    assert positions["symbol"].tolist() == ["AAA"]
    assert positions["entry_date"].tolist() == ["20260112"]
    assert positions["rebalance_date"].tolist() == ["20260109"]
    periods = build_position_replay_periods(positions, pricing)
    assert periods["exit_date"].tolist() == [pd.Timestamp("2026-01-13")]
    result = run_native_position_replay(
        positions, pricing, periods, config=PositionBacktestConfig(price_col="open")
    )
    result.validate()
    assert result.performance["net_return"].tolist() == pytest.approx([0.1])
    assert result.orders.empty
    assert result.fills.empty
