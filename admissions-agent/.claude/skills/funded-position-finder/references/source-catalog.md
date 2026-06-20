# Source catalog

The catalog of where to look for funded PhD positions / RAships lives in the KB:
**`kb/sources/funded-positions.md`** (each source with URL, coverage, free/paid, freshness, filter
mechanics, and the international-eligibility caveat). Read that file first; refresh it via
`knowledge-base-update` if stale. This reference adds the **search ORDER** the skill follows.

## Query in precision order (highest-precision first)

1. **Structured boards** (highest precision, explicit funding/filters) —
   jobs.ac.uk, EURAXESS, Nature Careers, THEunijobs, FindAPhD. Filter by funding + discipline; set the
   eligibility/funding filter to the client's nationality *before* reading (see eligibility-rules.md).
2. **US PI discovery** (medium precision; build the lab list, then check each lab's page) —
   NSF Award Search (funded grants → active PIs), CSrankings (active groups by area), department/lab
   pages, society/listserv postings. Then verify funding on the lab/department page directly.
3. **Social / aggregators** (noisiest, most verification) — Bluesky academic feeds, X "recruiting PhD
   students" + "Latest", LinkedIn keyword → Posts → Past-week, and aggregators. Treat every hit as a
   lead to confirm against the official source.

> **Verification is non-negotiable:** re-fetch each shortlisted listing live and stamp `last_verified`.
> "Fully funded" ≠ funded for internationals; aggregator "scans social media" claims are marketing —
> confirm on the primary source. Live listings are **never cached**.

See `query-templates.md` for the exact per-source query strings.
