import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def candidate_text():
    parts = []
    for path in ROOT.rglob("*"):
        ignored = {".git", ".venv", ".pytest_cache", "__pycache__", "dist", "build"}
        if path.is_file() and not (set(path.relative_to(ROOT).parts) & ignored):
            try:
                parts.append(path.read_text())
            except UnicodeDecodeError:
                pass
    return "\n".join(parts)


def test_candidate_contains_no_contact_or_local_path_values():
    text = candidate_text()
    assert not re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    assert "/" + "Users" + "/" not in text
    assert "private_" + "ledger_ref" not in text


def test_candidate_contains_no_raw_message_or_document_files():
    forbidden = {".eml", ".msg", ".pst", ".mbox", ".p12", ".pfx", ".key"}
    assert not any(path.suffix.lower() in forbidden for path in ROOT.rglob("*") if path.is_file())
