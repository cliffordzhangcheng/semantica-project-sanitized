"""Public HTML must retain the fixture's bounded truth and privacy boundary."""
from __future__ import annotations

import re

from semantica_external.demo import load_demo
from semantica_external.workbench import render_workbench


def test_public_workbench_contains_exact_pseudonymous_set() -> None:
    demo = load_demo()
    page = render_workbench()
    assert page.count("<tr><th scope='row'>") == 26
    assert all(page.count(item["container_id"]) == 1 for item in demo["containers"])
    assert re.search(r"\b[A-Z]{4}\d{7}\b", page) is None


def test_public_workbench_preserves_unresolved_states() -> None:
    page = render_workbench()
    assert "UNALLOCATED" in page
    assert "UNKNOWN" in page
    assert "BLOCKED" in page
    assert "not a production or canonical record" in page
    assert "<script" not in page
    assert "<form" not in page
    assert "https://" not in page
