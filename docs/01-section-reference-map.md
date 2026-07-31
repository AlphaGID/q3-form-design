# Section-to-reference-file map — HH2026 questionnaire

## Section 1 — Household identification
- 1.02-1.04 (LGA/ward/settlement name+code) -> lgas.csv, wards.csv, settlements.csv
- 1.06/1.07 (structure no., HH serial no.) -> no reference file, freeform
- 1.08/1.09 (enumerator code, team code) -> staff_roster.csv
- 1.11 (GPS reading) -> plausibility check only, against settlements.csv / settlements.geojson coordinates
- 1.12/1.13 (prior round visit + old HH id) -> previous_round_households.csv

## Section 2 — Consent
- No reference file. Skip logic only (refusal -> END).

## Section 3 — Household roster
- No reference file for the grid itself.
- 3.02 (count of eligible children) is a cross-check target against Section 4 completions.

## Section 4 — Child module
- 4.13 (antibiotic taken, "record from the medicine list") -> NO FILE SUPPLIED.
  README claims a medicine list is included; it is not present in docx, CSVs, or geojson.
  DEFECT: flag explicitly, do not silently invent a coding list.
- All other Section 4 items -> no reference file, range/logic validation designed in-house.

## Section 5 — Specimen collection
- 5.03 (label + check digit) -> specimen_label_allocation.csv
  (team_code, label_prefix "BSN", range_start/range_end, modulus 11 check digit scheme)

## Section 6 — Household environment
- No reference file.

## Section 7 — Close-out and supervisor review
- 7.04 (supervisor code) -> staff_roster.csv (filter role = Supervisor)

## Section 8 — Office use
- Out of scope for the digital form (paper-era double-entry step it replaces).
