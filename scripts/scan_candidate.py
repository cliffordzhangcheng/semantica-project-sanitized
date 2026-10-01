#!/usr/bin/env python3
"""Fail-closed privacy and secret scan for worktree and complete Git history."""
from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IGNORED_PARTS = {".git", ".venv", ".pytest_cache", "__pycache__", "dist", "build"}
FORBIDDEN_SUFFIXES = {".eml", ".msg", ".pst", ".mbox", ".p12", ".pfx", ".key"}


def patterns() -> dict[str, re.Pattern[bytes]]:
    return {
        "email_address": re.compile(rb"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
        "absolute_user_path": re.compile(rb"/" + rb"Users" + rb"/[A-Za-z0-9._-]+/"),
        "private_ledger_field": re.compile(rb"private_" + rb"ledger_ref"),
        "private_key": re.compile(rb"BEGIN (?:RSA |OPENSSH )?" + rb"PRIVATE KEY"),
        "aws_access_key": re.compile(rb"AKIA[0-9A-Z]{16}"),
        "generic_secret_assignment": re.compile(rb"(?i)(?:password|api[_-]?key|secret|token)\s*[:=]\s*['\"][^'\"]{8,}"),
        "phone_number": re.compile(rb"(?<![0-9A-Fa-f])\+?(?:\d[ ()-]?){9,15}(?![0-9A-Fa-f])"),
        "internal_inbox": re.compile(rb"_agent-" + rb"inbox"),
    }


def scan_blob(label: str, data: bytes) -> list[str]:
    if b"\0" in data[:4096]:
        return []
    return [f"{name}:{label}" for name, pattern in patterns().items() if pattern.search(data)]


def worktree_files() -> list[Path]:
    return sorted(path for path in ROOT.rglob("*") if path.is_file() and
                  not (set(path.relative_to(ROOT).parts) & IGNORED_PARTS))


def scan_worktree() -> list[str]:
    issues = []
    for path in worktree_files():
        relative = path.relative_to(ROOT)
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            issues.append(f"forbidden_suffix:{relative}")
        issues.extend(scan_blob(str(relative), path.read_bytes()))
    return issues


def scan_history() -> list[str]:
    if not (ROOT / ".git").exists():
        return ["history:git_repository_missing"]
    objects = subprocess.check_output(
        ["git", "rev-list", "--objects", "--all"], cwd=ROOT, text=True
    ).splitlines()
    issues = []
    seen = set()
    for line in objects:
        object_id, _, path = line.partition(" ")
        if not path or object_id in seen:
            continue
        seen.add(object_id)
        object_type = subprocess.check_output(
            ["git", "cat-file", "-t", object_id], cwd=ROOT, text=True
        ).strip()
        if object_type != "blob":
            continue
        if Path(path).suffix.lower() in FORBIDDEN_SUFFIXES:
            issues.append(f"history_forbidden_suffix:{path}")
        data = subprocess.check_output(["git", "cat-file", "-p", object_id], cwd=ROOT)
        issues.extend(scan_blob(f"history:{path}:{object_id[:12]}", data))
    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worktree-only", action="store_true")
    args = parser.parse_args()
    issues = scan_worktree()
    if not args.worktree_only:
        issues.extend(scan_history())
    if issues:
        print("PRIVACY_SECRET_SCAN_FAIL")
        for issue in sorted(set(issues)):
            print(issue)
        return 1
    print("PRIVACY_SECRET_SCAN_PASS")
    print(f"files_scanned={len(worktree_files())}")
    print("history_scanned=" + ("NO" if args.worktree_only else "YES"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

