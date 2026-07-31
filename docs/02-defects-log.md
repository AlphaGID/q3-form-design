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

(further defects to be added: contradictions, ambiguous/missing skip logic, and
paper-design gaps that permit unanalysable data — per the assessment's Q3 requirement)
