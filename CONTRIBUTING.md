# Contributing to pypilot-cli

Thanks for your interest in PyPilot. It is a free, open-source project maintained
by [Abdullah Masood](https://github.com/Abdullah-Masood-05), and bug reports, ideas
and pull requests are all welcome.

By taking part you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## What this package is

`pypilot-cli` is a thin wrapper. It contains no environment logic. When you run
`pypilot` (or call `pypilot.run()`), it finds the native `pypilot` engine, or
downloads it from the [engine repo's releases](https://github.com/pypilot-dev/pypilot/releases),
and runs it with your arguments.

## How this project is organized

PyPilot is split into a few repositories:

| Part | What it does |
|---|---|
| **This repo**, `pypilot-pip` | The `pypilot-cli` package on PyPI: finding or downloading the engine, and launching it |
| [`pypilot`](https://github.com/pypilot-dev/pypilot) | The Rust engine (the `pypilot` CLI and language server) and the Zed extension. The environment logic, GPU/CUDA tables and diagnostics live here |
| [`pypilot-vscode`](https://github.com/pypilot-dev/pypilot-vscode) | The VS Code extension: status bar, commands, tasks, report panel, and downloading the engine |

Problems with *what PyPilot decides* (which Python version, which CUDA build, which
imports are flagged) belong in the engine repo, and problems with the VS Code
extension belong in `pypilot-vscode`. Problems with installing through pip, or with
finding, downloading or launching the engine, belong here. If you are not sure, open
the issue here and it will be moved.

What is in this repo:

| Path | What it is |
|---|---|
| `src/pypilot/binary.py` | Platform detection, the engine cache, version checks, download and extraction |
| `src/pypilot/cli.py` | The `pypilot` console script: runs the engine and passes its exit code through |
| `src/pypilot/__init__.py` | The package version and `pypilot.run()` for use from Python |
| `tests/test_cli.py` | The tests |
| `.github/workflows/` | `ci.yml` (test matrix) and `publish.yml` (PyPI release) |

## License

This package is licensed under [AGPL-3.0-or-later](LICENSE). By contributing you
agree that your contributions are licensed under the same license.

## Reporting a bug

Open an [issue](https://github.com/pypilot-dev/pypilot-pip/issues/new?template=bug_report.md)
and include:

- What you did, what you expected, and what happened instead.
- The output of `pip show pypilot-cli` and `pypilot --version`, your Python
  version, your OS, and how you installed it (pip, pipx or `uv tool`).
- The exact error from the download or launch step. Failures print
  `Error: failed to locate or download PyPilot native engine: ...` and the download
  prints `PyPilot: downloading native engine from <url> ...`, so include both lines.
- Whether you are behind a proxy or offline, if the download failed.

The engine is looked up in this order: the cache, then `~/.cargo/bin`, then `PATH`,
then a fresh download. The cache is `%LOCALAPPDATA%\pypilot\bin\pypilot.exe` on
Windows (falling back to `~\.cache\pypilot\bin` if `LOCALAPPDATA` is unset), and
`$XDG_CACHE_HOME/pypilot/bin/pypilot` on Linux and macOS (falling back to
`~/.cache/pypilot/bin/pypilot`). A cached engine older than the one this package
ships is replaced. If you suspect a broken download, delete that file and run
`pypilot --version` again.

If the problem is about an environment (the output of `pypilot doctor`, a wrong
Python or CUDA choice), report it in the
[engine repo](https://github.com/pypilot-dev/pypilot/issues/new?template=bug_report.md).

For security problems, please do not open a public issue. Contact the maintainer
through the GitHub profile linked above.

## Suggesting a feature

Open a [feature request](https://github.com/pypilot-dev/pypilot-pip/issues/new?template=feature_request.md).
Describe the problem first, then the change you have in mind. Ideas about what the
engine does belong in the [engine repo](https://github.com/pypilot-dev/pypilot).

## Setting up for development

You need [uv](https://docs.astral.sh/uv/). The supported Pythons are 3.8 to 3.15.

```bash
git clone https://github.com/pypilot-dev/pypilot-pip.git
cd pypilot-pip
uv sync
```

| Command | What it does |
|---|---|
| `uv run python -m pytest -W error` | Run the tests, with warnings as errors (what CI runs) |
| `uv run --python 3.8 python -m pytest -W error` | The same on a specific Python version |
| `uv build` | Build the sdist and wheel into `dist/` |
| `uvx twine check dist/*` | Check the built package's metadata |

CI runs the tests on Python 3.8 to 3.15 on Linux, and on 3.8 and 3.15 on Windows and
macOS, because archive handling differs between platforms. Warnings are errors so
that a deprecation which a new Python release turns into a behaviour change fails
there first.

**The tests need network access.** Some of them call the real `ensure_binary()` and
`pypilot --version`, so they download the real engine from GitHub on the first run
(and cache it, see above).

## Code notes

- **Standard library only.** The package has no runtime dependencies
  (`dependencies = []`), and that should stay true. Dev tools live in the `dev`
  dependency group.
- **Python 3.8 must keep working.** Use `from __future__ import annotations`, and
  avoid syntax and standard-library features newer than 3.8 (for example,
  `typing.List` rather than `list[...]` in runtime-evaluated code).
- **Windows, macOS and Linux behave differently.** `install_binary` copies directly
  on Windows and renames over the old file elsewhere, and `extract_archive` handles
  both `.zip` and `.tar.gz`. Explain why in comments when you touch these, and try
  the change on a platform other than your own if you can.
- **Keep it thin.** If a change adds behaviour about Python environments, it
  probably belongs in the engine.

## Sending a pull request

1. Open an issue first for anything larger than a small fix, so we can agree on the
   approach before you spend time on it.
2. Fork the repo and create a branch from `master`.
3. Keep the change focused. Match the style of the surrounding code, and explain *why*
   in comments rather than restating what the code does. Add or update a test in
   `tests/test_cli.py` for a behaviour change.
4. Make small, logical commits with clear messages (for example `fix(binary): ...`
   or `test: ...`). Use LF line endings.
5. Run `uv run python -m pytest -W error`.
6. Open the pull request, describe what changed and why, and link the issue. Mention
   anything you could not test (for example, a platform or Python version you do not
   have).

The maintainer reviews pull requests as time allows, so a short wait is normal.

## Releases

Releases are cut by the maintainer. Contributors do not need to bump versions or
create tags. Pushing a tag `vX.Y.Z` runs the publish workflow, which tests, builds
and publishes to PyPI through trusted publishing. `DEFAULT_TAG` in
`src/pypilot/binary.py` names the engine release this package ships, so a new pip
release is made only after that engine release exists. PyPI never allows a version
number to be reused.
