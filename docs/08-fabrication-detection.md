# Fabrication and data-quality detection design

Digitising the form creates an opportunity paper cannot offer: automated,
cross-field checks that flag suspicious patterns for supervisor review,
without blocking submission outright (since a flagged record may still be
genuine — the point is to surface it for review, not to accuse the
enumerator).

## Checks already built into the form logic

These block or constrain at data-entry time, covered in the constraint
register (docs/04) and test plan (docs/07):
- Household size vs roster row count (structural, via jr:count)
- Eligible children count vs Section 4 modules rendered (structural, via
  nesting Section 4 inside the roster repeat)
- GPS reading vs registered settlement location (soft warning, not blocking)
- Visit date within the fieldwork window
- Specimen label check digit and team-range membership

## Additional fabrication-detection checks, timing-based

These are not about any single field being out of range, but about
implausible relationships between timestamps recorded across the form —
the classic signature of a form filled in after the fact rather than during
a real household visit.

**Interview duration plausibility.** 7.01 (interview end time) minus 1.10 (date
of visit, though only date not time is captured on paper, limiting this check)
combined with 5.04 (specimen cold-box time) gives an approximate span the
interview must have covered. A specimen timestamp that falls before the
household roster could plausibly have been completed, or an interview
recorded as lasting under two minutes end-to-end, are both signals worth a
supervisor's attention rather than automatic rejection.

**Note on what the paper form does not give us.** The paper questionnaire
only captures interview END time (7.01), not START time. This means a true
"interview took an implausibly short time" check cannot be computed from
the fields the ministry's paper design actually asks for. This is flagged
here as a form-design limitation inherited from the paper instrument, not
something the digital form invents a workaround for by adding an unrequested
field — adding an interview-start-time field would be a legitimate
recommendation for a future round, but is out of scope for a straight
digitisation of the approved HH2026v1 instrument.

**Same enumerator, implausible visit pace across a day.** This requires
aggregating across multiple submitted forms (all forms by one enumerator
code on one date), which is a server-side / dataset-level check, not
something a single XLSForm instance can compute about itself. Recommended
as a post-hoc analysis step run on the aggregated submission data (e.g. flag
any enumerator with more than N household visits recorded on one calendar
date, where N is set based on realistic travel time between settlements
using the settlements.csv coordinates), not as a form-level constraint.

**Straight-lining on the household roster.** If every roster row across a
household has identical relationship_to_head, sex, and age values, that's a
classic fabrication signature (an enumerator inventing a household rather
than actually enumerating it). Like the pacing check, this is naturally a
dataset-level check (comparing rows within one household's roster, ideally
compared against typical household composition patterns from
previous_round_households.csv), not a single-record form constraint, since a
small household with genuinely similar ages (e.g. twins) shouldn't be
auto-flagged by an in-form rule with no comparative context.

**Specimen label range membership** (already implemented, see docs/04) is
itself a fabrication-relevant check as well as a data-entry error check: a
label from another team's batch showing up on a form is either a
transcription mistake or a sign that labels are being shared/reused across
teams, which is a data-integrity issue with process-level as well as
technical implications, worth flagging to supervisors as such rather than
purely a "wrong number typed" framing.

## What is form-level vs dataset-level

| Check | Level | Where implemented |
|---|---|---|
| Roster count vs household size | form (structural) | XLSForm jr:count |
| Eligible count vs Section 4 modules | form (structural) | XLSForm nesting |
| GPS vs settlement location | form (soft flag) | XLSForm calculate + note |
| Specimen check digit / range | form (blocking constraint) | XLSForm constraint |
| Visit date in fieldwork window | form (blocking constraint) | XLSForm constraint |
| Enumerator visit pace across a day | dataset (cross-submission) | recommended post-hoc analysis, not built here |
| Roster straight-lining | dataset (cross-submission) | recommended post-hoc analysis, not built here |
| Interview duration plausibility | form, but limited by missing start-time field on paper | noted as inherited limitation |

This split matters for the submission: a single XLSForm instance genuinely
cannot see other submissions, so any check that depends on comparing across
households or across a day's work for one enumerator belongs in whatever
analysis pipeline runs on the aggregated ODK Central/Kobo submissions, not
inside the form definition itself. Presenting all of these as if they were
implementable as form-level constraints would overstate what a single
XLSForm can actually do.
