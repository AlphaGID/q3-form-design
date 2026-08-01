# AI assistance disclosure

AI assistance (Claude, Anthropic) was used throughout the development of this
submission. This file states what it was used for, specifically, rather than
as a general disclosure.

## What AI assistance was used for
- Code scaffolding for scripts/build_form.py, scripts/check_digit.py, and
  scripts/build_codebook.py, written and revised iteratively against actual
  pyxform conversion output.
- Debugging real conversion failures encountered during the build (e.g. the
  pyxform instance-duplication bug documented as D03 in docs/02-defects-log.md,
  and two XML-entity-escaping mistakes in early Section 5 constraint strings),
  each found by inspecting the compiled XForm output directly, not assumed.
- Drafting documentation across docs/01 through docs/10, based on decisions
  made and verified during the actual build — including the specimen
  check-digit algorithm, which was independently traced by hand against two
  known test cases before being trusted (see docs/06).
- Reasoning through design trade-offs (the settlement-list cascade mechanism,
  the sentinel-value coding scheme, the fabrication-detection design)
  collaboratively.

## What AI assistance was not used for
- The three defects logged (D01, D02, D03) were genuinely found during the
  build, not invented for the write-up; D01 in particular reflects an actual
  gap discovered in the supplied data pack.
- All final design decisions (settlement-list mechanism, ranges chosen where
  the questionnaire is silent, which fabrication checks belong in the form
  versus in post-hoc analysis) were made and are defensible by the candidate.

## Verification
The form can be independently reconverted by running
`python3 -m pyxform.xls2xform form/HH2026v1.xlsx output/HH2026v1.xml` and
compared against output/HH2026v1.xml already committed in this repository.
