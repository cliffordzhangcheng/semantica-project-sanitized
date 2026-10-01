# Status and limits

## Status

This repository is an evidence-grounded engineering candidate and demo. It is
not a production system or a canonical business record.

The bounded CASE-DEMO fixture preserves these current states:

| Dimension | Status |
| --- | --- |
| Containers | 26 pseudonymous identities |
| Individual date dispositions | 26 candidate dispositions |
| Owner depot gate-in coverage | 20 observations |
| Carrier off-hire coverage | 18 observations |
| Billing off-hire coverage | 5 observations |
| Receipt allocation | `UNALLOCATED` |
| Payments | `0` |
| Settlement | `UNKNOWN` |
| Case | `OPEN` |

## Limits

- Container identities and source locators are pseudonymized.
- Exact operational dates are redacted.
- The evidence bindings identify source classes, not confidential originals.
- A lot-level completion statement is not an individual container event.
- A candidate date is not a final business-approved timestamp.
- A receipt report is not proof of payment, allocation or settlement.
- The fixture is one bounded case and does not establish universal ontology
  rules by itself.
- The project has no write API, workflow execution, authentication layer,
  database, deployment definition or production integration.

## Interpretation rule

`UNKNOWN`, `REQUIRED`, `CONFLICTED` and `UNALLOCATED` are deliberate truth
states. Consumers must display them and must not silently replace them with a
successful outcome.

