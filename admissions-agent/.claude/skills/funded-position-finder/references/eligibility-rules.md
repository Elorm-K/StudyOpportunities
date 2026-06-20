# Eligibility rules

The hard rules that decide whether a "funded" position actually funds **this** client. Apply the
nationality/fee-status filter **before** reading results. Detailed, sourced UKRI rules live in
`kb/sources/funded-positions.md` (verified); this is the working summary.

## UK

- **Home vs international fee status.** A UKRI studentship pays only the **home** fee level; the
  **home↔international fee gap** must be covered by the institution, a co-funder, a fee waiver, or the
  student. Many "fully funded" UK PhDs are funded **at home level** → an international applicant may
  face an unfunded gap. Check the advert's fee-status line.
- **30% international cohort cap.** Since AY 2021/22, UKRI normally limits international students to
  **~30% of each cohort** per training grant (varies by research council). International slots are
  scarce and competitive — factor this into `funding_certainty`.
- **All UKRI studentships are open to internationals** and pay a full award (stipend + home fees), but
  the cap + fee-gap above still gate real access.

## US

- **RA / TA / fellowship model.** Funding is awarded by the **department/PI**, not a central office —
  admission and funding are usually one decision. Fully-funded PhD offers bundle tuition waiver +
  stipend + health insurance, typically ~5 years. RA = PI's grant; TA = teaching; fellowship = merit.
- **Visa work-hour limits** (~20 hrs/wk on-campus) shape RA/TA structure but don't block funding.
- Confirm the offer covers tuition **and** stipend for an international before treating it as funded.

## Nationality → scholarship cross-reference

When a position is unfunded for the client, pair it with a portable scholarship they qualify for:
- West Africa / Nigeria / Ghana → `kb/scholarships/africa.md` (Commonwealth, Mastercard, PTDF, GETFund).
- Bangladesh / SE Asia → `kb/scholarships/seasia.md` (Commonwealth, STFT, LPDP, Chevening, GREAT).
- UK/US named awards → `kb/scholarships/uk.md`, `kb/scholarships/us.md`.

## The core filter (keep only if ALL hold)
funded **for this nationality** · eligible (fee status / cohort cap) · recent (≤1–3 months) ·
interest/PI-matched. Drop anything that fails — never present an international-ineligible post as a fit.
