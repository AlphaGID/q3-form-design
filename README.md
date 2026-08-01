# HH2026 XLSForm — Part 2, Question 3 submission

Digitisation of `Household_Questionnaire_HH2026v1.docx` (paper instrument,
in `data/raw/`) into a working ODK/XLSForm, built and validated against
**pyxform 4.5.0**.

## Where to start

Read in this order:

1. `docs/01-section-reference-map.md` — which reference file serves which
   question, and where the questionnaire's own logic lives
2. `docs/02-defects-log.md` — three defects found and resolved/escalated
   (D01: missing medicine list, D02: sentinel field-width ambiguity,
   D03: a pyxform toolchain bug caught during the build)
3. `docs/03-settlement-list-mechanism.md` — how a 2,524-row settlement list
   is served on a 2GB offline device without a choices worksheet
4. `docs/04-constraint-register.csv` — every validation rule, range,
   skip-logic condition, and cross-check in the form, with its source
   (data pack file, questionnaire instruction, or judgement call)
5. `docs/05-sentinel-coding-scheme.md` — how the weight/height "not
   measured = 99" sentinel is handled without corrupting downstream analysis
6. `docs/06-specimen-check-digit.md` — the modulus-11 check digit algorithm,
   verified test cases, and how it's implemented in XPath (which has no
   loop construct, unlike the Python reference implementation)
7. `docs/07-test-plan.md` — 20 test cases across skip logic, repeat/count
   binding, range constraints, and reference-file lookups
8. `docs/08-fabrication-detection.md` — which quality checks belong in the
   form itself versus in post-hoc analysis of aggregated submissions
9. `docs/09-data-protection.md` — device encryption, GPS/specimen
   sensitivity, and a real trade-off in the settlement-list design that
   puts the full previous-round register on every device
10. `docs/10-codebook.csv` — every field in the built form, generated
    directly from `form/HH2026v1.xlsx` (not hand-typed), with each field
    mapped back to its paper question number where one exists

## The form itself

- `form/HH2026v1.xlsx` — the XLSForm, built programmatically by
  `scripts/build_form.py` (never hand-edited directly, to avoid the kind
  of silent spreadsheet mistakes a manual build risks)
- `form/HH2026v1-media/` — the reference CSVs shipped as form attachments
  (wards, settlements, staff roster, previous-round households, specimen
  label allocation)
- `output/HH2026v1.xml` — the compiled XForm, proof the form converts
- `scripts/check_digit.py` — standalone reference implementation of the
  specimen check-digit algorithm, with the verified test cases
- `scripts/build_codebook.py` — generates `docs/10-codebook.csv` from the
  actual built form

## How to reproduce the conversion

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 scripts/build_form.py
python3 -m pyxform.xls2xform form/HH2026v1.xlsx output/HH2026v1.xml
```

Validated with **pyxform 4.5.0** (see `requirements.txt` for the full
dependency list, and `docs/02-defects-log.md` D03 for a toolchain-level bug
found and fixed during this build).

## Known open items

- **4.13 (antibiotic name)** is implemented as free text, not a coded field,
  because no medicine list was included in the supplied data pack despite
  the README describing one — see D01 in the defects log. This is flagged
  as an open item pending the real list, not silently worked around.
- **Field performance on an actual 2GB device** has not been tested; the
  cascading-select design (docs/03) is verified logically/structurally but
  not benchmarked on real low-spec hardware.
- **Cross-submission fabrication checks** (enumerator visit pacing across a
  day, roster straight-lining) are designed but explicitly left as
  dataset-level post-hoc analysis rather than form-level constraints — see
  docs/08 for the reasoning.
