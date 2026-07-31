# Defects log — HH2026 questionnaire and data pack

For each defect: what it is, where it shows up, whether it was resolved in the form
or escalated, and why.

---

## D01 — Missing medicine list (data pack gap, not a questionnaire defect)

**Where it shows up:** Question 4.13 instructs the enumerator to "record from the
medicine list" when coding the antibiotic taken by the child. The README for the data
pack states the reference files exist "because the questionnaire refers to a
settlement list, a medicine list, a staff roster and pre-printed specimen labels."

**What's actually wrong:** No medicine list file is present anywhere in the supplied
data pack. It is not among the 7 reference CSVs/geojson, not embedded in the
questionnaire docx, and not referenced by any other file. The pack promises a
controlled list to code 4.13 against, and does not supply one.

**Resolution: escalated, not resolved in the form.**
Reasoning: inventing a plausible-looking antibiotic code list ourselves would mean
silently fabricating the coding frame for a clinically meaningful variable (this
question is one of two AMR-relevant items on the whole form). A wrong or
incomplete list here corrupts the antimicrobial-use analysis without anyone noticing,
which is a worse failure mode than leaving 4.13 as free text pending the real list.

**What the form does instead, until the real list is supplied:**
4.13 is implemented as free text (matching the "Other, specify" pattern the
questionnaire already uses at 4.14), with the code field left inactive. This is
flagged as an open item in the codebook and in the README of this repo, so the gap
is visible rather than hidden.

---

## D02 — Sentinel code field-width ambiguity (4.06)

**Where it shows up:** Question 4.06 (height/length) allots 3 digit boxes plus
a decimal on paper (000.0-999.9), but the not-measured sentinel is written as
plain "99". The paper form does not resolve whether the sentinel should be
entered as "99", "099.9", or some other value consistent with the field's
own box width.

**Resolution: resolved in the form**, not escalated. Unlike D01, this is a
formatting ambiguity rather than a missing external input the design
genuinely depends on — it can be closed by a form design decision without
ministry sign-off.

**What the form does:** per docs/05-sentinel-coding-scheme.md, 4.05 and 4.06
are each split into a numeric value field plus a separate measured/not-measured
status field. The sentinel is never typed into the numeric field at all, so
the box-width ambiguity is eliminated rather than resolved by picking one of
the ambiguous readings.

---

(further defects to be added: contradictions, ambiguous/missing skip logic, and
paper-design gaps that permit unanalysable data — per the assessment's Q3 requirement)

---

## D03 — pyxform instance-duplication bug: pulldata() vs select_one_from_file filename mismatch

**Where it shows up:** any field referenced by both a select_one_from_file
question (e.g. settlement, from settlements.csv) and a pulldata() calculation
elsewhere in the form (e.g. the GPS plausibility check, which pulls
settlements.csv's own lat/long back out for the same settlement).

**What went wrong:** select_one_from_file wards.csv creates a secondary XForm
instance named "wards" (extension stripped). pulldata('settlements.csv', ...)
independently creates a second, separate instance literally named
"settlements.csv" (extension kept), and pyxform then appends another .csv
when resolving the file path, producing a reference to a non-existent file
("settlements.csv.csv"). This is caught by pyxform's own "Conversion
complete!" message with no error or warning shown, so silent unless the
compiled XML is inspected directly.

**How it was caught:** by grepping the compiled output XML for instance IDs
and file references after building Section 1, rather than trusting a
successful conversion message alone.

**Resolution:** always call pulldata() with the filename WITHOUT the .csv
extension (e.g. pulldata('settlements', ...), not
pulldata('settlements.csv', ...)) whenever a select_one_from_file question
already references that same file elsewhere in the form. Applied to all four
affected calls (team_code lookup, settlement lat/long x2, previous-round
household id lookup).
