# Security policy

Do not submit confidential business documents, message archives, credentials
or personal contact data to this repository.

Before publishing a change, run:

```sh
python scripts/scan_candidate.py
python -m pytest -q
```

If sensitive material is discovered, stop distribution and remove it from the
complete unpublished history before proceeding. Deleting a file in a later
commit is insufficient because earlier commits remain reachable.

