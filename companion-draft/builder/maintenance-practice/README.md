# Maintenance practice tool

Fictional local reference for Chapters 27–30. AI-authored teaching code, not a captured Claude Code result. This program reads the CSV, validates the entire input, and prints JSON. It does not write data, connect to a service, or infer maintenance advice.

Use Python 3.10 or later. No third-party dependencies. Open a terminal in this directory, then run:

```sh
python3 tracker.py data/maintenance.csv --as-of 2026-10-17
python3 -m unittest discover -s tests -v
```

Expected: M01 and M02 due, M03 future, M04 done, M05 unknown. The comparison includes the supplied date. Blank dates are unknown; malformed dates, duplicate identifiers and unsupported statuses stop the report. A missing file produces a clear error and exit code 2.

The output is a teaching report, not a user-facing application. Preserve this version while building alternatives in a separate practice copy. Live Claude Code reproduction and beginner usability trials remain unperformed.
