#!/usr/bin/env python3
"""Bootstrap installer for tailscale-userspace-proxy.

Usage:
  curl -fsSL https://raw.githubusercontent.com/cadugevaerd/tailscale-userspace-proxy/main/install.py | python3
"""
from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

REPO_URL = "https://github.com/cadugevaerd/tailscale-userspace-proxy"
PACKAGE_SPEC = f"git+{REPO_URL}"


def run(cmd: list[str] | str, shell: bool = False, check: bool = True, env: dict[str, str] | None = None) -> int:
    print("$", cmd if isinstance(cmd, str) else " ".join(cmd))
    proc = subprocess.run(cmd, shell=shell, env=env)
    if check and proc.returncode != 0:
        raise SystemExit(proc.returncode)
    return proc.returncode


def is_yes(value: str) -> bool:
    return value.strip().lower() in {"y", "yes", "s", "sim"}


def confirm_or_cancel(question: str, cancel_message: str) -> None:
    answer = input(f"{question} [y/N]: ")
    if not is_yes(answer):
        raise SystemExit(cancel_message)


def install_uv() -> None:
    if shutil.which("uv"):
        return
    system = platform.system().lower()
    print("🔧 uv not found.")
    confirm_or_cancel("Install uv now?", "uv installation cancelled.")
    if system in {"linux", "darwin"}:
        if not shutil.which("curl"):
            raise SystemExit("curl is required to install uv automatically.")
        run("curl -LsSf https://astral.sh/uv/install.sh | sh", shell=True)
    elif system == "windows":
        run('powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"', shell=True)
    else:
        raise SystemExit(f"Unsupported OS for automatic uv install: {platform.system()}")


def candidate_paths() -> list[Path]:
    home = Path.home()
    names = ["tailscale-proxy.exe" if os.name == "nt" else "tailscale-proxy"]
    dirs = [
        home / ".local" / "bin",
        home / ".cargo" / "bin",
        home / "AppData" / "Roaming" / "Python" / "Scripts",
    ]
    found = []
    for d in dirs:
        for n in names:
            found.append(d / n)
    return found


def find_cli() -> str:
    exe = shutil.which("tailscale-proxy")
    if exe:
        return exe
    for path in candidate_paths():
        if path.exists():
            return str(path)
    return "tailscale-proxy"


def main() -> int:
    if sys.version_info < (3, 10):
        raise SystemExit("Python >= 3.10 is required.")
    install_uv()
    uv = shutil.which("uv")
    if not uv:
        extra = [str(Path.home() / ".local" / "bin"), str(Path.home() / ".cargo" / "bin")]
        os.environ["PATH"] = os.pathsep.join(extra + [os.environ.get("PATH", "")])
        uv = shutil.which("uv")
    if not uv:
        raise SystemExit("uv was installed but is not on PATH. Open a new shell and rerun this installer.")

    print("📦 Installing tailscale-proxy CLI with uv...")
    run([uv, "tool", "install", "--force", PACKAGE_SPEC])

    cli = find_cli()
    print("\n✅ CLI installed")
    print(f"Command: {cli}")
    print("\nRunning initial setup now...\n")
    return run([cli, "install"], check=False)


if __name__ == "__main__":
    raise SystemExit(main())
