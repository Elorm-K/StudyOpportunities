# Query templates

Per-source query strings. Substitute `{field}`, `{subfield}`, `{PI}`, `{intake}` (e.g. "Fall 2026"),
`{nationality}` from the client profile. Always set the funding/eligibility filter to the client's
status **before** reading results.

## Structured boards
- **FindAPhD** — search `{subfield}`; set **Funding** filter to the student's status (e.g.
  "Self-Funded" off; "International students" eligible). Filter by country.
- **jobs.ac.uk** — `{subfield} PhD studentship`; filter discipline; check each advert's fee-status
  line (home vs international).
- **EURAXESS** — `{subfield}`; Offer type = Job/Funding; set Country, Research field, Funding
  programme (Horizon Europe / MSCA are often international-friendly).
- **Nature Careers / THEunijobs** — `{subfield} PhD`; filter discipline + location; read the salary/
  funding line per listing (THEunijobs has no funding filter — open each).

## US PI discovery
- **NSF Award Search** (nsf.gov) — search `{subfield}` active awards → note the **PI + institution**,
  then visit the lab page to check for open funded RA/PhD slots.
- **CSrankings** (csrankings.org) — find active groups in `{area}` → department/faculty pages.
- **Google PI/lab discovery** —
  `site:edu "{subfield}" ("recruiting PhD students" OR "seeking PhD" OR "open positions") "{intake}"`
  and `site:edu "prospective students" {subfield} lab`.

## Social / aggregators (verify everything)
- **X/Twitter** — `("recruiting PhD" OR "looking for PhD students") {subfield}` → sort **Latest**;
  optionally `min_faves` to cut noise.
- **Bluesky** — academic / discipline feeds + `recruiting PhD {subfield}`.
- **LinkedIn** — keyword `{subfield} PhD funded` → **Posts** → **Past week**.

> Each hit is a *lead*. Re-fetch the official source, confirm funding is open to `{nationality}`, and
> stamp `last_verified` before shortlisting.
