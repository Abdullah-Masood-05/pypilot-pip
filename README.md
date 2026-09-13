# PyPilot (CLI & Python Package)

[![PyPI version](https://img.shields.io/pypi/v/pypilot-cli.svg)](https://pypi.org/project/pypilot-cli/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](LICENSE)
[![Rust](https://img.shields.io/badge/Engine-Rust-orange.svg)](https://github.com/Abdullah-Masood-05/pypilot)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://python.org)

**PyPilot** is a deterministic Python environment doctor, dependency solver, and toolchain manager. Powered by a high-speed compiled **Rust engine**, PyPilot calculates dependency intersections directly from PyPI wheel metadata, resolves hardware and CUDA build compatibility, and sets up working virtual environments without external AI or API keys.

---

## ⚡ High-Speed Native Rust Architecture

PyPilot combines the ease of installation via `pip` with the raw execution speed and low memory footprint of compiled Rust:
- **Instant startup**: Binary execution starts in single-digit milliseconds.
- **Zero Python overhead**: CLI commands delegate directly to the native `pypilot` binary.
- **Automatic platform management**: Transparently downloads and caches the verified native engine matching your operating system (Linux `x86_64`, macOS `Apple Silicon` / `Intel`, Windows `x64`), or respects a system-installed Rust binary on your `$PATH`.

---

## 📥 Installation

Install via `pip`:
```bash
pip install pypilot-cli
```

Or install as an isolated global tool with `uv`:
```bash
uv tool install pypilot-cli
```

Or via `pipx`:
```bash
pipx install pypilot-cli
```

---

## 📖 CLI Reference & Commands

PyPilot provides a complete suite of environment doctor and bootstrap tools:

### 1. `pypilot doctor`
Analyzes your current workspace, virtual environment, and dependency manifests (`requirements.txt`, `pyproject.toml`, `environment.yml`). Displays a read-only health check without modifying any files.
```bash
pypilot doctor
# Target a specific workspace folder:
pypilot doctor --path /path/to/project
```

### 2. `pypilot setup`
Bootstraps a deterministic virtual environment. Automatically detects existing system tools:
- Uses system `uv` if present on `$PATH`.
- Supports **pip-compatible mode** (`uv venv` + `uv pip`) to accelerate installations without forcing a `pyproject.toml` migration.
- Falls back cleanly to standard `python -m venv` + `pip` if `uv` is not installed.
```bash
pypilot setup
```

### 3. `pypilot check <package>`
Verifies whether a specific package and its wheels support your project's current Python interpreter version and operating system.
```bash
pypilot check mediapipe
pypilot check torch
pypilot check tensorflow
```

### 4. `pypilot install <package>`
Installs a package into your virtual environment and records it in your manifest (`requirements.txt` or `pyproject.toml`), preserving version constraints.
```bash
pypilot install requests
pypilot install numpy
```

### 5. `pypilot fix python`
Recomputes dependency version intersection and rebuilds the virtual environment on a Python version supported by all dependencies.
```bash
pypilot fix python
```

### 6. `pypilot fix cuda`
Scans system NVIDIA driver version and CUDA runtime, then re-pins PyTorch or TensorFlow wheels to the exact hardware-matched CUDA build.
```bash
pypilot fix cuda
```

### 7. `pypilot update-data`
Forces an immediate update of bundled hardware driver, CUDA compatibility matrices, and package wheel metadata.
```bash
pypilot update-data
```

### 8. `pypilot migrate-conda`
Translates legacy Anaconda / Miniconda `environment.yml` configuration files into a standard modern `pyproject.toml`.
```bash
pypilot migrate-conda
```

### 9. `pypilot lsp`
Runs PyPilot as a Language Server Protocol (LSP) server over `stdio`. Used natively by editor extensions ([Zed](https://zed.dev) and [VS Code](https://marketplace.visualstudio.com/items?itemName=AbdullahMasood-005.pypilot-vscode)) for live import diagnostics and automated environment actions.
```bash
pypilot lsp
```

---

## 🐍 Python Programmatic API

PyPilot can also be imported and used directly inside Python code:

```python
import pypilot

# Run any PyPilot command programmatically
result = pypilot.run(["doctor"], capture_output=True)
print(result.stdout)

# Locate or ensure native engine is available
bin_path = pypilot.ensure_binary()
print(f"Native engine located at: {bin_path}")
```

---

## ⚙️ Configuration

PyPilot respects workspace settings in `.pypilot.toml` or your editor configuration:
- `package_manager`: `"auto"` (default), `"uv"`, `"uv-pip"`, or `"pip"`.
- `notifications`: `"all"`, `"problems-only"`, or `"off"`.

---

## 📄 License

PyPilot is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0-or-later)**. See the [LICENSE](LICENSE) file for the full license text.
