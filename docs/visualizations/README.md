# Archify visualization pilot — Semantica public demo

**Scope:** Additive, public, pseudonymized, read-only visualization pilot. The current `public-workbench.html` and all semantic query code are unchanged. These diagrams explain the existing engineering candidate; they are **not a production status dashboard** or a claim of settled business truth.

## Openable diagrams

| Diagram | View (download and open locally) | Editable source |
| --- | --- | --- |
| Evidence/semantic workflow | [semantica-evidence-workflow.html](semantica-evidence-workflow.html) | [semantica-evidence-workflow.json](semantica-evidence-workflow.json) |
| Source-linked code architecture | [semantica-code-architecture.html](semantica-code-architecture.html) | [semantica-code-architecture.json](semantica-code-architecture.json) |

Both HTML artifacts are self-contained and were rendered using upstream **tt-a1i/archify v3.2.0**. Nodes include file/line references to the **public** repository at commit `3dbda49eba2a3e6ee6eb0d01554b54763720cf20` (the original `main` revision inspected for this pilot). The scope is code responsibilities and public fixture semantics, not current private operational state.

## Important truth boundaries

- Observation is not a verified Event; Gate-In is not Off-Hire.
- Receipt, Payment, Allocation and Settlement remain different financial concepts.
- All 26 pseudonymous container identities have candidate date dispositions. An individual event must not be silently promoted to verified.
- The bounded public fixture remains case `OPEN`; this pilot does not change business state, code, queries or public datasets.

## Verification on November 7, 2026

- Archify `doctor`: PASS (Node v24.14.0; installed upstream v3.2.0).
- `archify finalize` for both original diagram artifacts: validation PASS, delivery PASS, content check PASS, browser-check PASS, no diagnostics.
- Published HTML had SVG-only numeric geometry normalized (spaces between adjacent numeric coordinates converted to SVG-valid commas; one long floating-point SVG attribute rounded). This was needed because the existing privacy scanner interpreted SVG coordinate strings as possible telephone numbers. There was no business data change.
- `archify check` run again on **both published normalized HTML artifacts**: PASS, zero errors/warnings. A fresh browser test for the normalized copies is not claimed here; the originals passed automated browser-check.
- Existing project tests: **16 passed** with `PYTHONPATH=src python3 -m pytest -q`.
- `python3 scripts/scan_candidate.py --worktree-only`: **PRIVACY_SECRET_SCAN_PASS** on 23 files in the local candidate checkout.
- Complete-history privacy scan on the local zip snapshot is unavailable because the snapshot lacks earlier Git parents. The GitHub PR's normal CI must independently verify the actual full history before merge.

## Remaining improvements (non-blocking pilot)

- Architecture diagram has two 3-bend routes and generous unused top margin; Archify's automated checks still pass.
- This PR does not install Archify globally, change Portal/production routes, alter existing WorkItems or change any semantics.
- If regenerated from the JSON, rerun the same SVG-only numeric formatting and the repository privacy scanner before publication.

## Original references

- Upstream project: https://github.com/tt-a1i/archify
- Source repository: https://github.com/cliffordzhangcheng/semantica-project-sanitized
- Existing Workbench: [../../public-workbench.html](../../public-workbench.html)
- Existing privacy contract: [../PRIVACY.md](../PRIVACY.md)
