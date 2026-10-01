# Semantica Logistics Ontology Demo

This repository is a sanitized engineering candidate that demonstrates how a
logistics ontology can preserve evidence lineage, uncertainty and business
state boundaries in read-only operational queries.

The included bounded demo is pseudonymized. It contains no raw emails,
contact details, confidential documents, local machine paths or private
evidence bytes.

## What the demo proves

- One stable case contains 26 pseudonymous container identities.
- All 26 containers have source-bound candidate date dispositions.
- Evidence coverage includes 20 owner-reported depot gate-in observations,
  18 carrier-notified off-hire observations and 5 billing-reported off-hire
  observations.
- Gate-In and Off-Hire remain different business semantics.
- Observation and Event remain different record types.
- Receipt, Payment, Allocation and Settlement remain different financial
  concepts.
- Allocation remains `UNALLOCATED`, payments remain `0`, settlement remains
  `UNKNOWN`, and the case remains `OPEN`.

The demo does not prove production readiness, final settlement, canonical
business truth or general validity beyond this bounded case.

## Read-only capabilities

The Python package exposes four deterministic queries:

```python
from semantica_external import (
    explain_status,
    get_container_timeline,
    get_missing_evidence,
    get_offhire_status,
)

print(get_offhire_status("CASE-C01"))
print(get_missing_evidence("CASE-DEMO-001"))
```

- `get_container_timeline(container_no)`
- `get_offhire_status(container_no)`
- `get_missing_evidence(case_id)`
- `explain_status(case_id)`

Unknown identities fail closed. No query mutates the fixture or infers missing
payment, settlement or individual off-hire events.

## Run locally

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/python -m pytest -q
.venv/bin/python scripts/scan_candidate.py
```

## Repository layout

- `src/semantica_external/` — deterministic read-only demo API
- `src/semantica_external/data/` — pseudonymized bounded fixture
- `docs/` — architecture, status and privacy limits
- `tests/` — semantic, fail-closed and privacy regressions
- `scripts/scan_candidate.py` — worktree and complete-history privacy scan

See [Status and limits](docs/STATUS_AND_LIMITS.md) and
[Privacy boundary](docs/PRIVACY.md) before evaluating or reusing the demo.
