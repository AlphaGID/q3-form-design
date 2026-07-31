# Test plan — HH2026 XLSForm

Each case: what's being tested, the input, the expected behaviour, and how to
verify it (either by tracing the compiled XML, as done throughout the build,
or by manual walkthrough in ODK Collect/Enketo once the form is loaded).

Check-digit test cases (6 cases, all passing) are in docs/06-specimen-check-digit.md
and scripts/check_digit.py; not repeated here.

---

## Skip logic and section gating

**T01 — Result of visit = Refused (2) ends the form.**
Input: 1.14 = 2. Expected: Sections 2-7 all remain hidden (relevant on
section2 checks result_of_visit='1'; every later section chains off that).
Verify: confirmed at build time — section2's bind requires result_of_visit='1'.

**T02 — Result of visit = Completed (1) allows the form to continue.**
Input: 1.14 = 1. Expected: Section 2 becomes visible.
Verify: same bind, positive case.

**T03 — Consent refused (2.02 = 2) ends the form after Section 2.**
Input: result_of_visit=1, consent_given=2. Expected: Section 3 onward stay
hidden (section3's bind requires consent_given='1' in addition to
result_of_visit='1').
Verify: confirmed at build time (section3, section6, section7 binds).

**T04 — Prior-round household id only asked if 1.12 = Yes.**
Input: prev_round_visited=2 (No). Expected: 1.13 hidden, no ID required.
Input: prev_round_visited=1 (Yes). Expected: 1.13 shown, required, and
constrained against previous_round_households.csv.

**T05 — Vaccination card branch is mutually exclusive.**
Input: card_seen=1. Expected: 4.09 shown, 4.10 hidden.
Input: card_seen=2. Expected: 4.09 hidden, 4.10 shown.

**T06 — Antibiotic detail block only appears if 4.12 = Yes.**
Input: antibiotic_30d=2 or 8. Expected: 4.13-4.16 (antibiotic_name through
antibiotic_photo_taken) all hidden.
Input: antibiotic_30d=1. Expected: all four shown and required.

**T07 — Specimen collection only asked for children 12+ months.**
Input: age12plus=2 (No). Expected: 5.02 onward hidden for that child.

**T08 — Reason-for-no-specimen only when specimen not obtained.**
Input: specimen_obtained=1 (Yes). Expected: 5.06/5.07 hidden.
Input: specimen_obtained=2 (No). Expected: 5.06 shown; 5.07 additionally
shown only if 5.06=96 (Other).

**T09 — Animal antibiotic question only if household keeps animals.**
Input: keeps_animals=2. Expected: 6.04 hidden.

---

## Repeat / count binding (structural cross-checks)

**T10 — Roster row count matches household size exactly.**
Input: household_size=4. Expected: exactly 4 roster repeat instances
available; the repeat cannot be extended to a 5th or left at 3 in a way
that submits cleanly (jr:count enforces this, not a post-hoc constraint).
Verify: confirmed at build time — jr:count="/data/section3/household_size".

**T11 — Eligible children count is derived, not entered.**
Input: 2 roster rows with under5=1 and age_months in [9,59]; 2 rows outside
that range or under5=2. Expected: eligible_children_count = 2, computed
automatically, matching exactly the number of Section 4 modules that appear
(since Section 4 is nested per-row on eligible_for_section4, not a
separately-counted block).
Verify: confirmed at build time — sum(../roster/eligible_for_section4).

**T12 — Section 4/5 modules appear only for eligible children.**
Input: a roster with a mix of eligible and non-eligible rows. Expected:
Section 4 and Section 5 groups render only for rows where
eligible_for_section4=1; non-eligible rows show no child module at all.

---

## Range and format constraints

**T13 — Structure number and household serial number reject out-of-range entry.**
Input: structure_number=0. Expected: rejected (constraint is 1-999).
Input: structure_number=1000. Expected: rejected.
Input: structure_number=500. Expected: accepted.

**T14 — Visit date outside the fieldwork window is rejected.**
Input: visit_date=2026-05-31. Expected: rejected (window is 1-30 June 2026).
Input: visit_date=2026-07-01. Expected: rejected.
Input: visit_date=2026-06-15. Expected: accepted.

**T15 — Weight/height sentinel split prevents the 99-collision.**
Input: weight_status=2 (Not measured). Expected: weight_kg field hidden and
not required; no numeric value (99 or otherwise) is ever stored for weight.
Input: weight_status=1 (Measured), weight_kg=45.0. Expected: rejected
(constraint is 2.0-30.0 kg, appropriate for a 9-59 month child; 45.0 is
implausible and should be caught).
Input: weight_kg=12.5. Expected: accepted.

**T16 — Cold box temperature range.**
Input: specimen_coldbox_temp=15.0. Expected: rejected (range is 2.0-8.0 C).
Input: specimen_coldbox_temp=4.0. Expected: accepted.

**T17 — Household asset "None of these" mutual exclusion.**
Input: household_assets = A, H (Radio and None of these both selected).
Expected: rejected by the count-selected(.)=1-when-H-present constraint.
Input: household_assets = A, C (Radio and Mobile telephone). Expected:
accepted (H not involved, no restriction applies).
Input: household_assets = H only. Expected: accepted.

---

## Lookups against reference files

**T18 — Enumerator code must exist in the staff roster with the right role.**
Input: an enumerator_code not present in staff_roster.csv. Expected: not
selectable (select_one_from_file only offers real roster entries filtered
to role=Enumerator, so this failure mode is prevented by construction
rather than caught after the fact).

**T19 — Supervisor code, same pattern, filtered to role=Supervisor.**
Same reasoning as T18, applied to 7.04.

**T20 — Team code is consistent with enumerator code, not independently entered.**
Input: any valid enumerator_code. Expected: team_code_display auto-populates
via pulldata from staff_roster, with no way for it to disagree with the
roster (it isn't a separate manually-entered field).

---

## What this test plan does not yet cover (open items)

- Field testing on an actual low-spec Android device (2GB RAM) to confirm the
  cascading select performs acceptably with the full 2,524-row settlements.csv
  loaded as a media file — everything above is verified structurally/logically,
  not for on-device performance.
- Section 4.13 (antibiotic name) has no automated test beyond "is it shown
  when expected", since it's free text pending the missing medicine list (D01).
