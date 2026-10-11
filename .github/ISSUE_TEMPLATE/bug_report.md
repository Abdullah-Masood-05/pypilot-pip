---
name: Bug report
about: pip install, engine download or launch did not work as expected
title: ""
labels: bug
assignees: ""
---

**What happened**
A clear description of the problem.

**What you expected**
What you thought would happen.

**Steps to reproduce**
1.
2.
3.

**Versions**
- OS:
- Python version:
- Install method (pip / pipx / uv tool):
- `pip show pypilot-cli`:
- `pypilot --version`:

**The full error**
The complete output, including the `PyPilot: downloading native engine from ...` line and any `Error: failed to locate or download PyPilot native engine: ...` line.

**Anything else**
Proxy or offline setup, a `pypilot` already on your PATH or in `~/.cargo/bin`, or whether deleting the cached engine helped. If the problem is about what PyPilot decides for an environment, the engine repo (pypilot-dev/pypilot) is the better place.
