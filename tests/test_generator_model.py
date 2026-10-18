"""Synthetic model integration and optional local capacity100m checkpoint smoke tests."""

from __future__ import annotations

import os
from pathlib import Path

import pytest
import torch

from ticknet.eventstream.model import L2FoundationModel, ModelConfig
from ticknet.simulator.generator import GenerationContext, OrderGenerator
from ticknet.simulator.replay import BackgroundOrder

CHECKPOINT = (
    "artifacts/eventstream-h5-recent-fold/training/seed0/"
    "eventstream-top400-h5-capacity100m-recent.seed0.last.pt"
)


@pytest.fixture
def real_checkpoint() -> Path:
    configured = os.environ.get("TICKNET_GENERATOR_CHECKPOINT")
    path = Path(configured or CHECKPOINT)
    if not path.is_file():
        if configured:
            pytest.fail(f"Configured generator checkpoint is not a file: {path}")
        pytest.skip(
            "Optional local capacity100m checkpoint unavailable; set TICKNET_GENERATOR_CHECKPOINT"
        )
    return path


@pytest.fixture
def synthetic_model(tmp_path) -> L2FoundationModel:
    torch.manual_seed(17)
    config = ModelConfig(d_model=32, n_layers=1, n_heads=4, d_ff=64, max_seq=32)
    original = L2FoundationModel(config).eval()
    checkpoint = tmp_path / "synthetic.pt"
    torch.save({"model": original.state_dict()}, checkpoint)
    restored = L2FoundationModel(config).eval()
    restored.load_state_dict(torch.load(checkpoint, weights_only=True)["model"], strict=True)
    batch = _dummy_batch()
    with torch.no_grad():
        torch.testing.assert_close(restored(*batch)["reg"], original(*batch)["reg"], rtol=0, atol=0)
    return restored


def test_synthetic_checkpoint_forward(synthetic_model):
    with torch.no_grad():
        output = synthetic_model(*_dummy_batch())
    assert output["reg"].shape == (1, 8, 3)
    assert torch.isfinite(output["reg"]).all()


def test_synthetic_checkpoint_generates_orders(synthetic_model):
    _assert_model_orders(synthetic_model)


def _dummy_batch(seq_len: int = 8) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """Create legal synthetic inputs without claiming a realistic market distribution."""
    x = torch.randn(1, seq_len, 80, dtype=torch.float32)
    sid = torch.randint(0, 3, (1, seq_len))
    oid = torch.randint(0, 6, (1, seq_len))
    return x, sid, oid


def test_load_real_checkpoint_and_forward(real_checkpoint):
    sd = torch.load(real_checkpoint, map_location="cpu", weights_only=False)
    model = L2FoundationModel(ModelConfig(**_cfg_from_state(sd["model"])))
    model.load_state_dict(sd["model"], strict=True)
    model.eval()

    x, sid, oid = _dummy_batch()
    with torch.no_grad():
        out = model(x, sid, oid)
    assert "reg" in out
    assert out["reg"].shape == (1, 8, 3)


def test_generator_model_mode_produces_orders(real_checkpoint):
    sd = torch.load(real_checkpoint, map_location="cpu", weights_only=False)
    model = L2FoundationModel(ModelConfig(**_cfg_from_state(sd["model"])))
    model.load_state_dict(sd["model"], strict=True)
    model.eval()

    _assert_model_orders(model)


def _assert_model_orders(model):
    gen = OrderGenerator(model=model, stub=False)
    ctx = GenerationContext(
        initial_bid=(1000, 500),
        initial_ask=(1001, 300),
        history=[],
        n_orders=2,
        features=torch.randn(1, 8, 80, dtype=torch.float32),
        stream_ids=torch.randint(0, 3, (1, 8)),
        order_ids=torch.randint(0, 6, (1, 8)),
    )
    orders = gen.generate(ctx)
    assert len(orders) == 2
    for o in orders:
        assert isinstance(o, BackgroundOrder)
        assert o.volume > 0


def _cfg_from_state(state: dict) -> dict:
    """Infer the historical capacity100m layout, whose attention head dimension is 64."""
    n_layers = sum(1 for k in state if k.startswith("blocks.") and k.endswith("norm1.weight"))
    d_model = state["feat_proj.0.weight"].shape[0]
    n_heads = d_model // 64  # The optional real-checkpoint test targets capacity100m only.
    return {
        "d_model": d_model,
        "n_layers": n_layers,
        "n_heads": n_heads,
        "d_ff": d_model * 4,
        "max_seq": 512,
    }
