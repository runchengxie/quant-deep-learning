# CPU-default development environments

## Approved behavior

The uv development environment uses CPU PyTorch by default, including ordinary `uv run` and `uv sync`. Linux CUDA training remains an explicit, mutually exclusive selection in a separate environment. The GPU group preserves the existing PyPI graph and configures CUDA on Linux, not Windows or macOS. Other accelerators are outside this profile's validation. Keep `torch` mandatory in published package metadata and preserve Python 3.10+ support. Do not change model behavior, research protocols or production configuration.

## Approaches

An opt-in CPU extra preserves the old default but allows a later ordinary sync to reinstall CUDA. The approved approach instead uses default CPU and explicit GPU dependency groups with per-group sources. Existing GPU resolution remains the starting point; unrelated dependency upgrades are out of scope.

## Configuration and documentation

Use uv dependency groups `cpu` and `gpu`, default `cpu`, and declare the groups conflicting. CPU selection uses the official CPU index on supported Linux and Windows platforms; macOS keeps its supported PyPI build. GPU selection preserves the existing PyPI dependency contract. The commands must carry the selected group and an explicit separate environment for GPU work. Document that a bare run uses CPU again.

## Acceptance

- Exporting the default locked environment selects CPU torch and no CUDA/Triton packages.
- Exporting the explicit GPU environment selects the existing GPU dependency graph.
- Enabling both groups fails with a conflict.
- A repeated ordinary locked CPU run does not replace CPU torch with a CUDA build.
- Preserve mandatory published torch metadata and Python 3.10+ compatibility; check 3.10 resolution and actual CPU execution when available.
- Run all repository quality gates and a fresh independent review before integration. GPU package selection is checked without claiming GPU hardware execution.
