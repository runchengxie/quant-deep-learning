from __future__ import annotations

import importlib
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DECLARATION = re.compile(r'^(ticknet-[\w-]+)\s*=\s*"([\w.]+:[\w]+)"$', re.MULTILINE)
CLI_SCRIPTS = sorted(
    SCRIPT_DECLARATION.findall((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
)
assert CLI_SCRIPTS


@pytest.mark.parametrize("category", ["FutureWarning", "ResourceWarning"])
def test_project_pytest_configuration_rejects_unexpected_warnings(
    tmp_path: Path, category: str
) -> None:
    source = tmp_path / "test_unexpected_warning.py"
    source.write_text(
        "import warnings\ndef test_warning():\n"
        f"    warnings.warn('synthetic warning', {category})\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-c",
            str(ROOT / "pyproject.toml"),
            "--noconftest",
            "-q",
            str(source),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1, result.stdout + result.stderr
    assert f"{category}: synthetic warning" in result.stdout


@pytest.mark.parametrize(("name", "target"), CLI_SCRIPTS)
def test_declared_cli_entrypoint_shows_help(
    name: str,
    target: str,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module_name, function_name = target.split(":", 1)
    function = getattr(importlib.import_module(module_name), function_name)
    monkeypatch.setattr(sys, "argv", [name, "--help"])

    with pytest.raises(SystemExit) as raised:
        function()

    assert raised.value.code == 0
    captured = capsys.readouterr()
    assert "usage:" in captured.out.lower()
