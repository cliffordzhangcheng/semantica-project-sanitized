"""Render a static, read-only view of the public pseudonymous fixture."""
from __future__ import annotations

from html import escape

from .demo import load_demo


def _text(value: object) -> str:
    return escape(str(value), quote=True)


def _indicator(value: bool) -> str:
    return "Reported" if value else "Unknown"


def render_workbench() -> str:
    """Return standalone HTML; every displayed business value comes from public_demo.json."""
    demo = load_demo()
    coverage = demo["coverage"]
    finance = demo["finance"]
    closure = demo["closure"]
    rows = "\n".join(
        "<tr>"
        f"<th scope='row'>{_text(item['container_id'])}</th>"
        f"<td>{_indicator(item['owner_depot_gate_in'])}</td>"
        f"<td>{_indicator(item['carrier_notified_off_hire'])}</td>"
        f"<td>{_indicator(item['billing_reported_off_hire'])}</td>"
        f"<td>{_text(item['individual_date_status'])}</td>"
        f"<td>{_text(item['reconciliation_status'])}</td>"
        "</tr>"
        for item in demo["containers"]
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Semantica public case workbench</title>
<style>
:root {{ color-scheme: light dark; font-family: system-ui, sans-serif; line-height: 1.5; }}
body {{ max-width: 76rem; margin: auto; padding: 1.5rem; }}
header, section {{ margin-bottom: 2rem; }}
.summary {{ display: flex; flex-wrap: wrap; gap: 1rem; }}
.summary p {{ border: 1px solid #888; border-radius: .5rem; padding: .75rem 1rem; margin: 0; }}
.scroll {{ overflow-x: auto; }}
table {{ width: 100%; border-collapse: collapse; min-width: 45rem; }}
th, td {{ border-bottom: 1px solid #888; padding: .5rem; text-align: left; }}
thead th {{ position: sticky; top: 0; background: Canvas; }}
</style></head><body>
<header><h1>Semantica public case workbench</h1>
<p>This is a pseudonymous, read-only engineering demo. Candidate observations
are not verified events; the case is not a production or canonical record.</p></header>
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
</body></html>"""


if __name__ == "__main__":
    print(render_workbench())
