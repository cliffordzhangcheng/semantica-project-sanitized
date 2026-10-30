"""Render a static, read-only view of the public pseudonymous fixture."""
from __future__ import annotations

from html import escape

from .demo import (
    explain_status,
    get_container_timeline,
    get_missing_evidence,
    get_offhire_status,
    load_demo,
)


def _text(value: object) -> str:
    return escape(str(value), quote=True)


def _indicator(value: bool) -> str:
    return "Reported" if value else "Unknown"


def _list(items: list[object]) -> str:
    return "<ul>" + "".join(f"<li>{_text(item)}</li>" for item in items) + "</ul>"


def render_workbench() -> str:
    """Return standalone HTML; every displayed business value comes from public_demo.json."""
    demo = load_demo()
    coverage = demo["coverage"]
    finance = demo["finance"]
    closure = demo["closure"]
    case_id = demo["case"]["case_id"]
    missing = get_missing_evidence(case_id)["result"]
    explanation = explain_status(case_id)["result"]
    rows = "\n".join(
        "<tr>"
        f"<th scope='row'><a href='#{_text(item['container_id'])}'>{_text(item['container_id'])}</a></th>"
        f"<td>{_indicator(item['owner_depot_gate_in'])}</td>"
        f"<td>{_indicator(item['carrier_notified_off_hire'])}</td>"
        f"<td>{_indicator(item['billing_reported_off_hire'])}</td>"
        f"<td>{_text(item['individual_date_status'])}</td>"
        f"<td>{_text(item['reconciliation_status'])}</td>"
        "</tr>"
        for item in demo["containers"]
    )
    details = []
    for item in demo["containers"]:
        identity = item["container_id"]
        timeline = get_container_timeline(identity)["result"]
        status = get_offhire_status(identity)["result"]
        observations = timeline["observations"]
        detail = (
            f"<details id='{_text(identity)}'><summary>{_text(identity)} · "
            f"{_text(status['individual_date_status'])} · "
            f"reconciliation {_text(status['reconciliation_status'])}</summary>"
            f"<p>Selected candidate basis: {_text(status['selected_candidate_basis'])}. "
            "Lot completion is scoped to the lot; the individual off-hire event remains UNKNOWN. "
            "Observed dates and source values are redacted.</p>"
            + _list([
                f"{observation['observation_type']} · {observation['truth_status']} · "
                f"{observation['evidence_ref']}"
                for observation in observations
            ])
            + ("<p>No individual observation is reported in this public fixture.</p>"
               if not observations else "")
            + "</details>"
        )
        details.append(detail)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Semantica public case workbench</title>
<style>
:root {{ color-scheme: light dark; font-family: system-ui, sans-serif; line-height: 1.5; }}
body {{ max-width: 76rem; margin: auto; padding: 1.5rem; }}
header, section {{ margin-bottom: 2rem; }}
nav {{ display: flex; flex-wrap: wrap; gap: 1rem; }}
.summary {{ display: flex; flex-wrap: wrap; gap: 1rem; }}
.summary p {{ border: 1px solid #888; border-radius: .5rem; padding: .75rem 1rem; margin: 0; }}
.scroll {{ overflow-x: auto; }}
details {{ border: 1px solid #888; border-radius: .5rem; margin: .5rem 0; padding: .5rem 1rem; }}
summary {{ cursor: pointer; font-weight: 700; }}
table {{ width: 100%; border-collapse: collapse; min-width: 45rem; }}
th, td {{ border-bottom: 1px solid #888; padding: .5rem; text-align: left; }}
thead th {{ position: sticky; top: 0; background: Canvas; }}
</style></head><body>
<header><h1>Semantica public case workbench</h1>
<p>This is a pseudonymous, read-only engineering demo. Candidate observations
are not verified events; the case is not a production or canonical record.</p>
<nav aria-label="Workbench views"><a href="#summary">Case</a>
<a href="#container-table">Containers</a><a href="#details">Timelines and status</a>
<a href="#missing">Missing evidence</a><a href="#explanation">Status explanation</a></nav></header>
<section aria-labelledby="summary"><h2 id="summary">Bounded case</h2>
<p>Case: {_text(demo['case']['case_id'])}; closure: {_text(closure['status'])}.</p>
<div class="summary">
<p>Containers: <strong>{_text(coverage['containers'])}</strong></p>
<p>Owner gate-in reports: <strong>{_text(coverage['owner_depot_gate_in'])}</strong></p>
<p>Carrier off-hire reports: <strong>{_text(coverage['carrier_notified_off_hire'])}</strong></p>
<p>Billing off-hire reports: <strong>{_text(coverage['billing_reported_off_hire'])}</strong></p>
</div></section>
<section aria-labelledby="finance"><h2 id="finance">Financial boundaries</h2>
<p>Receipt allocation: {_text(finance['allocation'])}; payments:
{_text(finance['payments'])}; settlement: {_text(finance['settlement'])};
case: {_text(finance['case'])}.</p></section>
<section aria-labelledby="container-table"><h2 id="container-table">Container observations</h2>
<p>Reported means a redacted observation exists. Unknown does not imply that
the event did not occur. Individual dates remain candidates.</p>
<div class="scroll"><table><thead><tr><th scope="col">Pseudonymous ID</th>
<th scope="col">Owner gate-in</th><th scope="col">Carrier off-hire</th>
<th scope="col">Billing off-hire</th><th scope="col">Date status</th>
<th scope="col">Reconciliation</th></tr></thead><tbody>
{rows}
</tbody></table></div></section>
<section aria-labelledby="details"><h2 id="details">Container timelines and off-hire status</h2>
<p>Each row is derived from the public fixture's read-only timeline and status queries.
Evidence references name redacted source classes; they do not expose source documents.</p>
{''.join(details)}</section>
<section aria-labelledby="missing"><h2 id="missing">Missing evidence and gates</h2>
<p>The case remains {_text(closure['status'])}. Missing requirements:</p>
{_list(missing['missing_requirements'])}
<p>Blocking gates:</p>{_list(missing['blocking_gates'])}
<p>Containers without a carrier-notified off-hire report:</p>
{_list(missing['containers_without_carrier_notified_off_hire'])}
<p>Unresolved conflicts:</p>{_list(closure['conflicts'])}</section>
<section aria-labelledby="explanation"><h2 id="explanation">Status explanation</h2>
<p>Operational status: {_text(explanation['operational_status'])};
individual date status: {_text(explanation['individual_date_status'])};
financial status: {_text(explanation['financial_status'])};
closure status: {_text(explanation['closure_status'])}.</p>
{_list(explanation['explanation'])}</section>
</body></html>"""


if __name__ == "__main__":
    print(render_workbench())
