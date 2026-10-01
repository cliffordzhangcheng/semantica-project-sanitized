# Privacy boundary

This candidate follows data minimization by design.

Included:

- pseudonymous case and container identifiers;
- aggregate evidence coverage;
- redacted evidence-class references;
- candidate, unknown, conflict and reconciliation states;
- deterministic code and tests.

Excluded:

- raw email messages or headers;
- personal or corporate contact details;
- confidential agreements, invoices or attachments;
- local machine paths;
- private evidence bytes, source file hashes or source locators;
- internal task, agent, queue or control-plane provenance;
- credentials, tokens and authentication configuration.

The committed history is scanned by `scripts/scan_candidate.py`. The scan must
pass before any publication decision.

