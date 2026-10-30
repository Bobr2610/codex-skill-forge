from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path
from typing import Any


class OpsError(RuntimeError):
    """Expected safe generator failure suitable for a concise CLI message."""


def resolve_root(raw: str | Path) -> Path:
    path = Path(raw).expanduser().resolve()
    if not path.is_dir():
        raise OpsError(f"Not a directory: {path}")
    return path


def _git(root: Path, *args: str) -> str | None:
    if not (root / ".git").exists():
        return None
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True,
                            text=True, encoding="utf-8", errors="replace", check=False)
    return result.stdout.strip() if result.returncode == 0 else None


def inspect(root: Path) -> dict[str, Any]:
    excluded = {".git", ".venv", "venv", "node_modules", "__pycache__", "dist", "build", ".projectops"}
    manifests = {"pyproject.toml": "Python", "package.json": "JavaScript/TypeScript",
                 "Cargo.toml": "Rust", "go.mod": "Go", "pom.xml": "Java", "build.gradle": "Java/Kotlin",
                 "build.gradle.kts": "Kotlin", "Gemfile": "Ruby", "composer.json": "PHP"}
    found: list[tuple[str, str]] = []
    rules: list[str] = []
    readmes: list[str] = []
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in excluded]
        base = Path(current)
        for filename in files:
            rel = (base / filename).relative_to(root).as_posix()
            if filename in manifests:
                found.append((rel, manifests[filename]))
            if filename == "AGENTS.md":
                rules.append(rel)
            if filename.lower().startswith("readme"):
                readmes.append(rel)
    git_dir = root / ".git"
    return {"root": str(root), "stack": sorted({stack for _, stack in found}),
            "manifests": sorted(path for path, _ in found), "agent_rules": sorted(rules)[:50],
            "readmes": sorted(readmes)[:50],
            "git": {"present": git_dir.exists(), "status": _git(root, "status", "--short", "--branch"),
                    "branch": _git(root, "branch", "--show-current"),
                    "branches": (_git(root, "branch", "--format=%(refname:short)") or "").splitlines(),
                    "remotes": (_git(root, "remote", "-v") or "").splitlines()}}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")[:48].rstrip("-")
    if not slug:
        raise OpsError("Project folder name must contain ASCII letters or digits to generate a Codex skill name")
    return slug
