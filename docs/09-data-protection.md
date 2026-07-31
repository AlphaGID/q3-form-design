# Data protection note

## What the paper form already commits to
The confidentiality notice printed on HH2026v1 states the form identifies
individual households and children, includes biological specimen
identifiers, may be used only for survey purposes, must not be shown or
disclosed to anyone outside the survey team, and that completed forms must
remain in the supervisor's custody at all times (ethics approval
BSHREC/2026/041). Digitising the form does not relax any of this — if
anything it raises the stakes, since a lost or compromised device can expose
far more households at once than a lost stack of paper forms.

## What changes, going from paper to digital

**Data at rest on the device.** Between collection and sync/upload, this
survey's household roster, GPS coordinates, and specimen identifiers sit on
an Android tablet in the field for up to the full fieldwork window (a
multi-day offline deployment, per the operating conditions). ODK Collect
encrypts finalized-but-unsent form data on-device when form encryption is
enabled; this should be enabled for this form given the specimen identifiers
and GPS coordinates it carries, rather than left at ODK's default.

**Device loss or theft.** A lost paper form exposes one household's data.
A lost tablet, if not encrypted and PIN/passcode-protected, exposes every
household visited by that enumerator up to that point, plus the full
reference media (settlement list, staff roster, and — notably —
previous_round_households.csv, a 3,982-row register of a prior survey round
that sits on every single enumerator's device regardless of which
settlements they're actually assigned to). This is a real amplification of
exposure risk from digitisation and worth stating explicitly rather than
glossing over: the offline-cascade design decided in docs/03 means the
*entire* previous-round register, not just the relevant slice, has to be on
every device.

**GPS coordinates.** 1.11 records a precise GPS reading at the dwelling
entrance. Precise geolocation of a household is itself sensitive, beyond
just being an aid to fieldwork logistics — worth a clear internal access
policy on who can view the raw coordinates versus only the settlement-level
aggregate, once data reaches the office.

**Specimen identifiers.** The label a stool specimen carries (BSN-prefixed,
per specimen_label_allocation.csv) links directly to a household and a
named child through 1.06/1.07/4.02 on the same form page. Anyone with both
the completed form and the physical labeled specimen can identify the child
the biological sample came from — this is exactly the kind of link the
paper form's confidentiality notice is written to prevent from spreading
beyond the survey team, and the digital form's photo-capture step at 4.16
(photograph of medicine packaging) adds a further sensitive data type
(an image, potentially showing identifying context) that the paper form
never had to account for at all.

**Transmission.** Submissions should sync to the server (ODK Central/Kobo)
only over an encrypted connection (HTTPS, which is the platform default),
and only once, ideally, connectivity is available on a trusted network
rather than any open network encountered in the field.

**Data minimisation on the device beyond what's collected.** The offline
cascade design means every device carries the full settlements.csv,
wards.csv, staff_roster.csv, and previous_round_households.csv regardless of
that enumerator's actual assignment. This is a real form-design trade-off
against pure data minimisation, made necessary by the "no choices worksheet,
2GB device, no cascading list scoped to individual enumerator assignment"
constraints already documented in docs/03. Flagged here explicitly as a
known and accepted trade-off, not an oversight: solving it fully (shipping
each enumerator only their own assigned subset of the reference files) would
require a per-device form-build step keyed to team assignment, which is
disproportionate for a single deployable form and was explicitly ruled out
of scope in docs/03's rejected-approaches section.

## Recommendations for deployment (not built into the form itself, since these are
## deployment/device-configuration decisions, not XLSForm-level ones)
- Enable ODK Collect's form encryption for this form specifically, given the
  specimen identifiers and GPS coordinates it carries.
- Enforce device-level PIN/passcode and, ideally, full-disk encryption on
  every team tablet, as an organisational device-management policy rather
  than something the form definition can enforce.
- Restrict server-side access to raw GPS coordinates and specimen-linked
  identifiers to roles that need them, with settlement-level aggregation as
  the default view for broader analysis access.
- Ensure devices sync and then clear locally finalized submissions promptly,
  rather than accumulating a large local backlog of sensitive records across
  the full fieldwork window.
