"""Deterministic, read-only capability functions over a sanitized fixture."""
from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from importlib.resources import files
from typing import Any, Callable


CAPABILITY_VERSION = "semantica-logistics-demo-v0.1"
TRUTH_STATES = {"VERIFIED", "CANDIDATE", "UNKNOWN", "REQUIRED", "CONFLICTED", "UNALLOCATED"}


class UnknownIdentityError(ValueError):
    """Raised when a query identity is not present in the bounded fixture."""


def _hash(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_demo() -> dict:
    path = files("semantica_external").joinpath("data/public_demo.json")
    value = json.loads(path.read_text(encoding="utf-8"))
    _validate(value)
    return value


def _validate(value: dict) -> None:
    containers = value["containers"]
    if len(containers) != 26 or len({item["container_id"] for item in containers}) != 26:
        raise ValueError("container identity coverage changed")
    coverage = value["coverage"]
    observed = {
        "containers": len(containers),
        "owner_depot_gate_in": sum(item["owner_depot_gate_in"] for item in containers),
        "carrier_notified_off_hire": sum(item["carrier_notified_off_hire"] for item in containers),
        "billing_reported_off_hire": sum(item["billing_reported_off_hire"] for item in containers),
    }
    if observed != coverage:
        raise ValueError("evidence coverage changed")
    if any(item["individual_date_status"] != "CANDIDATE" or
           item["reconciliation_status"] != "REQUIRED" for item in containers):
        raise ValueError("candidate truth was promoted")
    finance = value["finance"]
    if finance != {"receipts": 1, "allocation": "UNALLOCATED", "payments": 0,
                   "settlement": "UNKNOWN", "case": "OPEN"}:
        raise ValueError("financial truth changed")
    states = set(value["truth_states"])
    if not TRUTH_STATES <= states:
        raise ValueError("truth-state vocabulary is incomplete")


def _container(value: dict, container_no: str) -> dict:
    for item in value["containers"]:
        if item["container_id"] == container_no:
            return item
    raise UnknownIdentityError(f"UNKNOWN_CONTAINER:{container_no}")


def _case(value: dict, case_id: str) -> None:
    if case_id != value["case"]["case_id"]:
        raise UnknownIdentityError(f"UNKNOWN_CASE:{case_id}")


def _envelope(value: dict, capability: str, identity: str, result: dict,
              evidence_refs: list[str], unknowns: list[str], conflicts: list[str]) -> dict:
    semantic = {
        "capability": capability,
        "case_id": value["case"]["case_id"],
        "requested_identity": identity,
        "status": "BLOCKED",
        "result": result,
        "evidence_refs": sorted(set(evidence_refs)),
        "unknown_markers": sorted(set(unknowns)),
        "conflict_markers": sorted(set(conflicts)),
    }
    return {
        "capability_version": CAPABILITY_VERSION,
        "read_only": True,
        "no_implicit_mutation": True,
        **semantic,
        "semantic_hash": _hash(semantic),
    }


def _query_container(capability: str, container_no: str,
                     project: Callable[[dict, dict], tuple[dict, list[str], list[str], list[str]]]) -> dict:
    value = load_demo()
    before = _hash(value)
    item = _container(value, container_no)
    result, refs, unknowns, conflicts = project(value, item)
    response = _envelope(value, capability, container_no, result, refs, unknowns, conflicts)
    if _hash(value) != before:
        raise RuntimeError("read-only query mutated the fixture")
    return response


def get_container_timeline(container_no: str) -> dict:
    def project(_: dict, item: dict):
        observations = []
        mapping = (
            ("owner_depot_gate_in", "OWNER_DEPOT_GATE_IN_REPORTED", "EV-OWNER-GATE-IN"),
            ("carrier_notified_off_hire", "CARRIER_OFF_HIRE_DATE_NOTIFIED", "EV-CARRIER-OFF-HIRE"),
            ("billing_reported_off_hire", "BILLING_REPORTED_OFF_HIRE", "EV-BILLING-OFF-HIRE"),
        )
        for flag, observation_type, evidence_ref in mapping:
            if item[flag]:
                observations.append({
                    "record_type": "OBSERVATION",
                    "observation_type": observation_type,
                    "date_value": "REDACTED",
                    "truth_status": "CANDIDATE",
                    "evidence_ref": evidence_ref,
                })
        unknowns = ["individual_off_hire_event=UNKNOWN"]
        conflicts = (["date_semantics=DISTINCT_DATE_SEMANTICS_RETAINED"]
                     if item["date_semantics"] == "DISTINCT_DATE_SEMANTICS_RETAINED" else [])
        result = {
            "container_id": item["container_id"],
            "observations": observations,
            "individual_events": [],
            "lot_completion": "OFF_HIRE_CONFIRMED_LOT_SCOPE",
            "lot_completion_scope": "LOT",
            "individual_date_status": item["individual_date_status"],
            "reconciliation_status": item["reconciliation_status"],
        }
        return result, item["evidence_refs"] + ["EV-LOT-COMPLETION"], unknowns, conflicts

    return _query_container("get_container_timeline", container_no, project)


def get_offhire_status(container_no: str) -> dict:
    def project(_: dict, item: dict):
        result = {
            "container_id": item["container_id"],
            "lot_completion": "OFF_HIRE_CONFIRMED_LOT_SCOPE",
            "lot_completion_scope": "LOT",
            "individual_off_hire_event": "UNKNOWN",
            "individual_date_status": item["individual_date_status"],
            "selected_candidate_basis": item["selected_candidate_basis"],
            "owner_depot_gate_in": item["owner_depot_gate_in"],
            "carrier_notified_off_hire": item["carrier_notified_off_hire"],
            "billing_reported_off_hire": item["billing_reported_off_hire"],
            "date_values": "REDACTED",
            "date_semantics": item["date_semantics"],
            "reconciliation_status": item["reconciliation_status"],
        }
        unknowns = ["individual_off_hire_event=UNKNOWN"]
        conflicts = (["date_semantics=DISTINCT_DATE_SEMANTICS_RETAINED"]
                     if item["date_semantics"] == "DISTINCT_DATE_SEMANTICS_RETAINED" else [])
        return result, item["evidence_refs"] + ["EV-LOT-COMPLETION"], unknowns, conflicts

    return _query_container("get_offhire_status", container_no, project)


def get_missing_evidence(case_id: str) -> dict:
    value = load_demo()
    _case(value, case_id)
    missing_carrier = [item["container_id"] for item in value["containers"]
                       if not item["carrier_notified_off_hire"]]
    result = {
        "case_id": case_id,
        "missing_requirements": deepcopy(value["closure"]["missing_requirements"]),
        "containers_without_carrier_notified_off_hire": missing_carrier,
        "blocking_gates": deepcopy(value["closure"]["blocking_gates"]),
    }
    return _envelope(
        value, "get_missing_evidence", case_id, result,
        [item["evidence_id"] for item in value["evidence_bindings"]],
        ["payment=UNKNOWN", "settlement=UNKNOWN", "allocation=UNALLOCATED"],
        deepcopy(value["closure"]["conflicts"]),
    )


def explain_status(case_id: str) -> dict:
    value = load_demo()
    _case(value, case_id)
    result = {
        "case_id": case_id,
        "case_status": value["finance"]["case"],
        "operational_status": "OFF_HIRE_CONFIRMED_LOT_SCOPE",
        "individual_date_status": "CANDIDATE",
        "financial_status": "REQUIRED",
        "closure_status": value["closure"]["status"],
        "finance": deepcopy(value["finance"]),
        "explanation": [
            "Lot completion and individual candidate dates are separate.",
            "Gate-In and Off-Hire are separate business semantics.",
            "Receipt, Payment, Allocation and Settlement are separate.",
        ],
    }
    return _envelope(
        value, "explain_status", case_id, result,
        [item["evidence_id"] for item in value["evidence_bindings"]],
        ["payment=UNKNOWN", "settlement=UNKNOWN", "allocation=UNALLOCATED"],
        deepcopy(value["closure"]["conflicts"]),
    )

