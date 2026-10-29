# Step reviews

One file per step: `S1.11.md`, `S2.3.md`, …

Copy the template from `docs/AGENT_PLAYBOOK.md` §13. Keep every review — this folder is the audit trail that proves each step was verified by someone other than the session that wrote it.

Rules:

- A step's registry status may not move to `done` without a review file whose verdict is `SHIP`.
- A review with `FIX-FIRST` keeps the step `in_progress`; `FALSE-DONE` reopens it and gets a line in `docs/PROGRESS.md`.
- The break-it test (§6.1) must name which guard was deleted and confirm the suite went red.
