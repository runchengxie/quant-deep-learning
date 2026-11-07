"""Synthetic signals through a real Go queue and its installed Python adapter."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from importlib.metadata import distribution
from pathlib import Path
from typing import Any

import pandas as pd
import pytest
from backtest_runtime.contracts import BacktestJobRequest
from backtest_runtime.results import read_job_result
from test_signal_acceptance import signal_positions

from ticknet.research.registry import file_sha256

RUNTIME_COMMIT = "c9493008ad41da4391db38542528a4ccbe385b73"


def _call(root: Path, *args: str, success: bool = True) -> dict[str, Any]:
    configured = os.environ.get("BACKTEST_GO_EXECUTABLE")
    assert configured, "Set BACKTEST_GO_EXECUTABLE to the pinned Go runtime binary"
    executable = Path(configured)
    assert executable.is_absolute()
    assert executable.is_file()
    completed = subprocess.run(
        [
            str(executable),
            "--database",
            str(root / "jobs.sqlite"),
            "--artifact-root",
            str(root / "artifacts"),
            "--result-root",
            str(root / "results"),
            "--python-executable",
            sys.executable,
            "--error-format",
            "json",
            *args,
        ],
        capture_output=True,
        text=True,
        timeout=90,
        check=False,
    )
    assert (completed.returncode == 0) is success, (completed.stdout, completed.stderr)
    output = completed.stdout if success else completed.stderr
    return json.loads(output) if output.strip() else {}


def _request(root: Path) -> BacktestJobRequest:
    positions, pricing, periods = signal_positions(root)
    payload = json.loads(Path(__file__).with_name("request-v1.json").read_text())
    artifacts = root / "artifacts" / "sha256"
    artifacts.mkdir(parents=True)
    for key, frame in zip(
        ("positions_ref", "pricing_ref", "periods_ref"),
        (positions, pricing, periods),
        strict=True,
    ):
        temporary = root / f"{key}.parquet"
        frame.to_parquet(temporary, index=False)
        digest = file_sha256(temporary)
        temporary.replace(artifacts / digest)
        payload["inputs"][key] = f"artifact://sha256/{digest}"
    return BacktestJobRequest.from_mapping(payload)


def test_signals_through_go_queue_and_verified_result(tmp_path: Path) -> None:
    provenance = json.loads(
        distribution("quant-backtest-runtime").read_text("direct_url.json") or "{}"
    )
    assert provenance["vcs_info"]["commit_id"] == RUNTIME_COMMIT
    assert provenance["url"] == "https://github.com/runchengxie/quant-backtest-runtime.git"
    capabilities = _call(tmp_path, "capabilities")
    assert capabilities["implementation"] == "go"
    assert capabilities["source_revision"] == RUNTIME_COMMIT
    request = _request(tmp_path)
    path = tmp_path / "request.json"
    path.write_text(json.dumps(request.to_mapping()))
    plan = _call(tmp_path, "plan", str(path))
    assert not (tmp_path / "jobs.sqlite").exists()
    assert plan["request_sha256"] == request.request_sha256
    receipt = _call(
        tmp_path, "submit", "--queue", str(path), "--expected-plan-sha256", plan["plan_sha256"]
    )
    assert _call(tmp_path, "submit", "--queue", str(path))["job_id"] == receipt["job_id"]
    assert _call(tmp_path, "inspect", receipt["job_id"])["status"] == "SUBMITTED"
    _call(tmp_path, "serve", "--once", "--concurrency", "1")
    status = _call(tmp_path, "inspect", receipt["job_id"])
    assert status["status"] == "SUCCEEDED", status
    manifest = read_job_result(
        tmp_path / "results",
        job_id=receipt["job_id"],
        manifest_sha256=status["result_sha256"],
        request_sha256=request.request_sha256,
    )
    assert _call(tmp_path, "result", receipt["job_id"]) == manifest
    assert manifest["schema_version"] == "ticknet.backtest_job_result.v1"
    published = tmp_path / "results" / receipt["job_id"]
    assert pd.read_parquet(published / "performance.parquet")[
        "net_return"
    ].tolist() == pytest.approx([0.1])
    assert pd.read_parquet(published / "positions.parquet")["symbol"].tolist() == ["AAA"]
    assert pd.read_parquet(published / "orders.parquet").empty
    assert pd.read_parquet(published / "fills.parquet").empty
    with (published / "performance.parquet").open("ab") as output:
        output.write(b"tamper")
    with pytest.raises(ValueError, match="checksum mismatch"):
        read_job_result(
            tmp_path / "results",
            job_id=receipt["job_id"],
            manifest_sha256=status["result_sha256"],
            request_sha256=request.request_sha256,
        )


def test_changed_input_fails_before_job_state(tmp_path: Path) -> None:
    request = _request(tmp_path)
    path = tmp_path / "request.json"
    path.write_text(json.dumps(request.to_mapping()))
    ref = request.inputs["positions_ref"]
    assert ref is not None
    artifact = tmp_path / "artifacts" / "sha256" / ref.rsplit("/", 1)[-1]
    with artifact.open("ab") as output:
        output.write(b"tamper")
    error = _call(tmp_path, "submit", "--queue", str(path), success=False)
    assert error["code"] == "INTEGRITY_FAILURE"
    assert not (tmp_path / "jobs.sqlite").exists()
