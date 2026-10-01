import json

import pytest

from semantica_external import (
    UnknownIdentityError,
    explain_status,
    get_container_timeline,
    get_missing_evidence,
    get_offhire_status,
    load_demo,
)


def test_fixture_has_expected_bounded_coverage():
    value = load_demo()
    assert value["coverage"] == {
        "containers": 26,
        "owner_depot_gate_in": 20,
        "carrier_notified_off_hire": 18,
        "billing_reported_off_hire": 5,
    }
    assert value["finance"] == {
        "receipts": 1,
        "allocation": "UNALLOCATED",
        "payments": 0,
        "settlement": "UNKNOWN",
        "case": "OPEN",
    }


def test_timeline_preserves_observation_event_boundary():
    response = get_container_timeline("CASE-C01")
    result = response["result"]
    assert result["individual_events"] == []
    assert {item["record_type"] for item in result["observations"]} == {"OBSERVATION"}
    assert "individual_off_hire_event=UNKNOWN" in response["unknown_markers"]
    assert response["read_only"] is True


def test_gate_in_and_offhire_are_separate():
    result = get_offhire_status("CASE-C01")["result"]
    assert result["owner_depot_gate_in"] is True
    assert result["carrier_notified_off_hire"] is True
    assert result["date_values"] == "REDACTED"
    assert result["individual_off_hire_event"] == "UNKNOWN"
    assert result["individual_date_status"] == "CANDIDATE"


def test_billing_only_candidate_is_not_promoted():
    response = get_offhire_status("CASE-C04")
    result = response["result"]
    assert result["billing_reported_off_hire"] is True
    assert result["carrier_notified_off_hire"] is False
    assert result["selected_candidate_basis"] == "BILLING_REPORTED_OFF_HIRE"
    assert result["reconciliation_status"] == "REQUIRED"


def test_missing_evidence_and_financial_unknowns_remain_visible():
    missing = get_missing_evidence("CASE-DEMO-001")
    explained = explain_status("CASE-DEMO-001")
    assert len(missing["result"]["containers_without_carrier_notified_off_hire"]) == 8
    assert "allocation=UNALLOCATED" in missing["unknown_markers"]
    assert explained["result"]["finance"]["payments"] == 0
    assert explained["result"]["finance"]["settlement"] == "UNKNOWN"


def test_same_query_is_deterministic_and_fixture_is_not_mutated():
    before = json.dumps(load_demo(), sort_keys=True)
    first = explain_status("CASE-DEMO-001")
    second = explain_status("CASE-DEMO-001")
    assert first["semantic_hash"] == second["semantic_hash"]
    assert json.dumps(load_demo(), sort_keys=True) == before


@pytest.mark.parametrize("call,identity", [
    (get_container_timeline, "UNKNOWN-CONTAINER"),
    (get_offhire_status, "UNKNOWN-CONTAINER"),
    (get_missing_evidence, "UNKNOWN-CASE"),
    (explain_status, "UNKNOWN-CASE"),
])
def test_unknown_identity_fails_closed(call, identity):
    with pytest.raises(UnknownIdentityError):
        call(identity)
