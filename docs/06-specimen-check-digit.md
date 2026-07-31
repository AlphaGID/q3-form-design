# Specimen label validation — check digit and range

## Source
specimen_label_allocation.csv gives, per team: a label prefix (BSN), a numeric
range (range_start-range_end), and the check digit scheme in prose: "Modulus
11, weights 2 to 7 applied right to left, remainder 10 recorded as X."

## Algorithm (confirmed by script, scripts/check_digit.py)
1. Take the numeric portion of the label (e.g. "480000").
2. Apply weights 2,3,4,5,6,7 to the digits right to left.
3. Sum the weighted digits.
4. check = 11 - (sum mod 11)
5. If check = 11, check = 0. If check = 10, check = "X".
6. Full label = prefix + numeric portion + "-" + check digit
   (matches the paper form's box: "BSN ⌷⌷⌷⌷⌷⌷ - ⌷").

## Two-part validation used in the form (5.03)
Both parts are needed; either alone is insufficient:

**A. Range membership.** The numeric portion must fall within the
range_start-range_end issued to the enumerator's own team_code (looked up
from specimen_label_allocation.csv via the enumerator's team, already
resolved at 1.09). This catches a label from the wrong team's batch being
used, even if that label is otherwise a validly-formed one.

**B. Check digit recomputation.** The check digit is recalculated from the
numeric portion and compared to what the enumerator typed. This catches
transcription errors, which are the realistic field failure mode: an
enumerator copying a 6-digit number by hand under field conditions.

## Test cases (scripts/check_digit.py, all passing)
| Case | Number | Given check | Expected | Result |
|---|---|---|---|---|
| Valid, range start (TM01) | 480000 | 1 | valid | PASS |
| Valid, hits remainder-10 -> X | 480001 | X | valid | PASS |
| Valid, range end (TM01) | 480899 | 1 | valid | PASS |
| Invalid, wrong check digit | 480010 | 0 | invalid (correct is 9) | PASS |
| Invalid, adjacent-digit transposition | 480001 | 9 | invalid (9 belongs to 480010) | PASS |
| Invalid, single-digit substitution | 480011 | 7 vs 9 | invalid | PASS |
| Boundary, one past TM01 range | 480900 | n/a | belongs to TM02, not TM01 | confirmed by range check |

The transposition and substitution cases are the ones that matter most in
practice: a modulus-11 scheme with position-dependent weights is specifically
chosen because it catches these two error types, which a simple digit-sum
checksum would miss. Worth stating explicitly in the write-up, since it's the
reason this scheme was chosen over a simpler one.

## What this needs in the actual XLSForm
- specimen_label_allocation.csv ships as a form attachment (pulldata source).
- On 5.03 entry: pulldata() looks up the enumerator's team_code range; a
  calculate node recomputes the check digit from the typed numeric portion;
  a constraint compares the two and blocks submission (with a clear error
  message) if they don't match, before the enumerator moves on.
