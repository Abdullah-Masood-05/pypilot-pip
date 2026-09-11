"""
pypilot.binary — Locate or download the platform-matching native `pypilot` helper binary.
"""

from __future__ import annotations

import os
import platform
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
import zipfile
from pathlib import Path

GITHUB_REPO = "Abdullah-Masood-05/pypilot"
DEFAULT_TAG = "v1.0.2"
MIN_VERSION = (1, 0, 2)


def get_platform_slug() -> tuple[str, str]:
    """
    Returns (slug, extension), e.g. ("windows-x64", "zip") or ("linux-x64", "tar.gz").
    """
    system = platform.system().lower()
    machine = platform.machine().lower()

    if system == "linux":
        if machine in ("x86_64", "amd64"):
            return "linux-x64", "tar.gz"
        raise RuntimeError(f"Unsupported Linux architecture for PyPilot: {machine}")
    elif system == "darwin":
        if machine in ("arm64", "aarch64"):
            return "darwin-arm64", "tar.gz"
        elif machine in ("x86_64", "amd64"):
            return "darwin-x64", "tar.gz"
        raise RuntimeError(f"Unsupported macOS architecture for PyPilot: {machine}")
    elif system == "windows":
        if machine in ("x86_64", "amd64"):
            return "windows-x64", "zip"
        raise RuntimeError(f"Unsupported Windows architecture for PyPilot: {machine}")
    else:
        raise RuntimeError(f"Unsupported operating system for PyPilot: {system}")


def get_cache_dir() -> Path:
    """Returns directory for storing cached PyPilot binaries."""
    if sys.platform == "win32":
        base = os.environ.get("LOCALAPPDATA")
        if base:
            cache = Path(base) / "pypilot" / "bin"
        else:
            cache = Path.home() / ".cache" / "pypilot" / "bin"
    else:
        base = os.environ.get("XDG_CACHE_HOME")
        if base:
            cache = Path(base) / "pypilot" / "bin"
        else:
            cache = Path.home() / ".cache" / "pypilot" / "bin"
    cache.mkdir(parents=True, exist_ok=True)
    return cache


def binary_name() -> str:
    return "pypilot.exe" if sys.platform == "win32" else "pypilot"


def parse_version(out: str) -> tuple[int, int, int] | None:
    # Example: "pypilot 1.0.2"
    for part in out.strip().split():
        components = part.split(".")
        if len(components) == 3 and all(c.isdigit() for c in components):
            return int(components[0]), int(components[1]), int(components[2])
    return None


def probe_binary(path: Path | str) -> tuple[int, int, int] | None:
    try:
        res = subprocess.run(
            [str(path), "--version"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if res.returncode == 0:
            return parse_version(res.stdout)
    except Exception:
        pass
    return None


def download_binary(tag: str = DEFAULT_TAG) -> Path:
    """Download prebuilt native binary from GitHub releases."""
    slug, ext = get_platform_slug()
    bin_name = binary_name()
    archive_name = f"pypilot-{slug}.{ext}"
    url = f"https://github.com/{GITHUB_REPO}/releases/download/{tag}/{archive_name}"

    cache_dir = get_cache_dir()
    dest_binary = cache_dir / bin_name

    print(f"PyPilot: downloading native engine from {url} ...", file=sys.stderr)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_archive = Path(tmpdir) / archive_name
        req = urllib.request.Request(url, headers={"User-Agent": "pypilot-python"})
        with urllib.request.urlopen(req) as resp, open(tmp_archive, "wb") as f:
            shutil.copyfileobj(resp, f)

        if ext == "zip":
            with zipfile.ZipFile(tmp_archive, "r") as zf:
                zf.extractall(tmpdir)
        else:
            with tarfile.open(tmp_archive, "r:gz") as tf:
                tf.extractall(tmpdir)

        extracted_bin = Path(tmpdir) / bin_name
        if not extracted_bin.exists():
            # Search subdirectories if any
            candidates = list(Path(tmpdir).rglob(bin_name))
            if candidates:
                extracted_bin = candidates[0]
            else:
                raise FileNotFoundError(f"{bin_name} not found in downloaded archive {archive_name}")

        shutil.copy2(extracted_bin, dest_binary)

    if sys.platform != "win32":
        dest_binary.chmod(dest_binary.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    return dest_binary


def ensure_binary() -> Path:
    """
    Locates an existing binary on PATH or in cache, or downloads it from GitHub.
    """
    bin_name = binary_name()

    # 1. Check if native binary is already in cache
    cached = get_cache_dir() / bin_name
    if cached.is_file():
        ver = probe_binary(cached)
        if ver and ver >= MIN_VERSION:
            return cached

    # 2. Check ~/.cargo/bin
    cargo_bin = Path.home() / ".cargo" / "bin" / bin_name
    if cargo_bin.is_file():
        ver = probe_binary(cargo_bin)
        if ver and ver >= MIN_VERSION:
            return cargo_bin

    # 3. Check system PATH (making sure we don't recurse into ourselves)
    system_path = shutil.which(bin_name)
    if system_path:
        p = Path(system_path).resolve()
        # Avoid looping if python script itself is called pypilot.exe
        if not str(p).lower().endswith((".py", ".pyw")):
            ver = probe_binary(p)
            if ver and ver >= MIN_VERSION:
                return p

    # 4. Download latest binary
    return download_binary()
