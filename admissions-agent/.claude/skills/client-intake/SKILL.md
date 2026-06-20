---
name: client-intake
description: Use when a new client profile is being created or an existing one is incomplete. Runs a branching question bank conversationally, captures self-reported academics, and writes a validated client_profile.json.
---

# Client intake

Build (or complete) a client's `client_profile.json` by running a **branching, conversational
question bank** — asking only the questions relevant to this client's path. Capture exactly what the
downstream search skills need, and nothing they don't.

This skill is **question-driven**. Grades, test scores, and experience are **self-reported** — the
agent does **not** ingest or parse transcripts or uploaded documents. Ask the academic questions
directly (the 5 academic questions below) and record the client's answers. (A client may still file
a transcript in `clients/<name>/transcripts/` for the operator's own reference, but it is never
parsed by the agent.)

## When to run

- A new client: no `client_profile.json` yet (copy `clients/_template/` to start).
- An existing client whose profile is missing search-critical fields, or whose inputs changed.

## Process

1. **Load or create the profile.** Use `lib/profile_io.py` (`load_profile` / `save_profile`).
   Never hand-edit the JSON. New client → copy the template first.

2. **Branch before asking.** Determine the client's path from three switches and ask only what
   applies (see `references/intake-questions.md`, where every question is tagged with the downstream
   skill it feeds):
   - **degree_level** — undergraduate / postgraduate_taught / postgraduate_research. Research
     levels unlock research-interest and target-PI questions; undergraduate skips them.
   - **target countries** — UK / US / both. Selects which deadline/document/test questions matter.
   - **funding need** — full-funding-required gates the depth of scholarship and funded-position
     questions.

3. **Ask the 5 academic questions.** Ask each directly and store the answers in
   `academics.qualifications[]` with each item's `source` set to `self_reported` (or `confirmed`
   once the client has explicitly verified the value back to you). The five:
   1. University / institution attended (name + country)
   2. Degree / qualification + field of study
   3. Grading system used (e.g. Nigerian 5.0 CGPA, UK honours, percentage, US 4.0)
   4. Your result / CGPA (the raw grade)
   5. Graduation date (or expected)

4. **Capture search-critical fields — and push back on vagueness.** These directly seed
   `university-matching` and (later) `funded-position-finder` query construction. A vague answer
   produces a weak search; demand specificity:
   - research interests / subfield (research levels) — "CS" is too broad; "reinforcement learning
     for robotics, interested in Prof. X's sim-to-real work" is searchable. Ask a follow-up when an
     answer is too broad to search on.
   - admired labs / professors / papers (research levels)
   - nationality (drives scholarship and funded-position eligibility gates)
   - degree level
   - full-funding flag (`targets.full_funding_required`, `funding.needs_scholarship`)

5. **Validate for internal consistency.** Check that answers cohere — e.g. the reported grade
   format matches the stated grading system (a "4.52" with grading system "UK honours" is a
   mismatch; re-ask). Normalize answers into the §3 contract shape.

6. **Confirm completeness, then write.** Ensure the search-critical fields are specific enough to
   move on. Write the profile with `save_profile` (it validates against the schema), and set
   `pipeline_state.intake = "done"`.

## Output

- A validated `client_profile.json`.
- `pipeline_state.intake = "done"`.
- Academic fields ready for `transcript-evaluation`'s grade mapping (self-reported raw grade +
  grading system).

## Guardrails (see ../../../CLAUDE.md)

- Self-reported grades are **planning estimates** — `mapped_grades.is_official` stays `false`. Tell
  the client.
- The agent never parses uploaded files; academics come only from the client's stated answers.
- Don't over-collect: ask only what the branched path needs.
