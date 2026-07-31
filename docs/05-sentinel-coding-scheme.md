# Sentinel code handling — measurement fields

## The problem
4.05 (weight) and 4.06 (height/length) each use "99" as a not-measured sentinel
inside a field that otherwise carries a real measurement. Stored as one plain
numeric field, 99 is indistinguishable from a (wildly implausible but
field-shaped) real value, and any downstream mean/range calculation will
silently include not-measured cases as if they were 99kg or 99.9cm children.

## Additional defect found here
4.06's sentinel is written as "99" but the field's own box width is 3 digits +
1 decimal (000.0-999.9). The paper form does not resolve whether the sentinel
is "99" or "099.9" or something else. Logged as D02 in the defects log
(docs/02-defects-log.md) — resolved in the form per the decision below, since
it's a formatting ambiguity, not a substantive design contradiction that needs
ministry sign-off.

## Resolution, applied to every measurement field with this pattern (4.05, 4.06)
Each measurement question is split into two form fields, not one:
- a numeric value field, constrained to a plausible physical range, left
  BLANK (not populated with 99) when not measured
- a separate `_status` select_one field: measured / not measured, driven
  directly by whether the enumerator picks the "Not measured" option

The paper form's single box becomes two linked fields under the hood, but
still presents as one prompt to the enumerator (relevant only sets the status
field, and the value field is only asked/enterable when status = measured).
This means:
- a downstream query for mean weight can filter on `_status = measured`
  without ever touching a sentinel value
- "not measured" is representable with no ambiguity about field width, since
  it's a category choice, not a number typed into a box

## Constraint register entries (added to docs/04-constraint-register.csv)
- 4.05 value: range 2.0-30.0 kg (plausible weight for a 9-59 month child;
  judgement, no range stated on paper)
- 4.05 status: not measured -> value field skipped, not defaulted to 99
- 4.06 value: range 60.0-120.0 cm (plausible length/height for 9-59 months;
  judgement, no range stated on paper)
- 4.06 status: same pattern as 4.05
- 4.07 (measurement position): required only when 4.06 status = measured

## Where else this pattern recurs
Checked every other question against this same failure mode (a numeric field
that also carries an 8/9/96/98/99-style code): none of the remaining Section 4
or Section 6 items mix a sentinel into a measurement field. 4.11, 4.12, 4.15
etc. use "Do not know = 8" but those are categorical select_one fields to
begin with, so 8 is just another category, not a collision with a continuous
measurement.
