# Decision Log

Record of consequential decisions made during this research program, with
date, rationale, and who made the call (autonomous engineering decision vs.
human-approved research decision).

---

### D001 — 2026-09-09 — Repository structure adopted (autonomous)
Adopted the directory structure specified in the project brief
(`/research`, `/src`, `/configs`, `/scripts`, `/tests`, `/docs`, `/data`)
as-is, since it already matches sound research-repo practice. No deviation
needed at this time.

**Type:** routine engineering — no human approval required.

---

### D002 — 2026-09-09 — Raw data will never be committed (autonomous)
`.gitignore` configured to exclude `data/`, `*.csv`, `*.parquet`, `*.json`,
`*.sqlite`, `*.db` etc. by default, with explicit exceptions carved out
for known-safe files (e.g. `research/LITERATURE_MATRIX.csv`, JSON configs).
This is a hard safety requirement from the project brief, not open to
autonomous override.

**Type:** routine engineering — no human approval required.

---

*(Further entries appended as decisions are made. Entries requiring human
sign-off will be flagged **DECISION REQUIRED** in `PROGRESS.md` before being
finalized here.)*
