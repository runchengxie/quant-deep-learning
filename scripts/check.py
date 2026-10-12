"""Run the manual local Python quality checks."""

from __future__ import annotations

import subprocess
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def _project_python() -> Path:
    candidates = (
        REPOSITORY_ROOT / ".venv" / "Scripts" / "python.exe",
        REPOSITORY_ROOT / ".venv" / "bin" / "python",
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise SystemExit("Missing project virtual environment. Run: uv sync --locked --extra dev")


def main() -> None:
    python = _project_python()
    checks = (
        ("Ruff lint", [python, "-m", "ruff", "check", "."]),
        ("Ruff formatting", [python, "-m", "ruff", "format", "--check", "."]),
        ("ty type checks", [python, "-m", "ty", "check"]),
        (
            "pytest and coverage",
            [python, "-m", "pytest", "--cov", "--cov-report=term-missing"],
        ),
        ("Synthetic smoke checks", [python, "scripts/smoke_test.py"]),
    )

    for label, command in checks:
        print(f"\n==> {label}", flush=True)
        completed = subprocess.run(command, cwd=REPOSITORY_ROOT, check=False)
        if completed.returncode:
            raise SystemExit(completed.returncode)

    print("\nAll manual Python quality checks passed.")


if __name__ == "__main__":
    main()
