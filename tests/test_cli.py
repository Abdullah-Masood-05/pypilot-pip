import subprocess
import pypilot
from pypilot.binary import ensure_binary, get_platform_slug


def test_platform_slug():
    slug, ext = get_platform_slug()
    assert slug in ("linux-x64", "darwin-x64", "darwin-arm64", "windows-x64")
    assert ext in ("tar.gz", "zip")


def test_ensure_binary():
    bin_path = ensure_binary()
    assert bin_path.exists()


def test_pypilot_version():
    res = pypilot.run(["--version"], capture_output=True)
    assert res.returncode == 0
    assert "pypilot" in res.stdout
