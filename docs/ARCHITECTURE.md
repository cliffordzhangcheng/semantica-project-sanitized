# Architecture

```text
Pseudonymized bounded fixture
        |
        v
Semantic validation and fail-closed rules
        |
        v
Deterministic read-only capability functions
        |
        v
Evidence refs + unknown/conflict markers + semantic hash
```

The ontology layer carries the business distinctions. A future transport
adapter may expose the functions over an API or MCP, but transport code must
not reinterpret the statuses.

## Core distinctions

- `Observation != Event`
- `Gate-In != Off-Hire`
- `Receipt != Payment != Allocation != Settlement`
- `Payable Booked != Paid`

## Determinism

Each query returns a `semantic_hash` calculated from its semantic payload.
Repeated calls with the same fixture and identity return the same hash.

## Mutation boundary

The package loads a fresh validated fixture for each query and returns copies.
It provides no mutation, persistence or execution interface.

