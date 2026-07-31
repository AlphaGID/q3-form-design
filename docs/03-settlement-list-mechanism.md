# Serving the settlement list on a 2GB offline device

## The problem
Question 1.04 requires selecting a settlement (name + code) from settlements.csv,
2,524 rows, on an Android tablet with 2GB RAM and no network for up to 9 consecutive
days. The question paper explicitly rules out a choices worksheet as an answer.

## Rejected approaches

**1. Standard XLSForm choices worksheet (explicitly disallowed).**
A choices sheet with 2,500+ rows gets compiled directly into the XForm XML that
ODK Collect/KoboCollect must parse and hold in memory every time the form opens.
On a 2GB device this causes multi-second UI freezes on the settlement question and
raises real risk of the app being killed for memory over a multi-day offline
deployment. It also means any correction to the settlement list requires
re-pushing the entire form definition.

**2. Flat select_one_from_file, no cascading.**
Moving the list to an external CSV media file (rather than an embedded choices
sheet) removes the XML-bloat problem, since the list lives on disk and is looked
up rather than compiled in. But it still presents the enumerator with a single
list of 2,500+ names to search or scroll through. Given 38% of enumerators are not
confident English readers and mean schooling is 6 years, a flat list of this size
is an error-prone UI regardless of how it's stored.

**3. Full external database / case-management backend.**
Architecturally the "right" answer at national programme scale (a proper
spatially-indexed lookup service), but disproportionate for a single deployable
XLSForm and outside what a self-contained form can implement. Noted as the
correct next step if this design were scaled beyond one survey round, not
implemented here.

## Chosen mechanism

1. **External CSV media file, not a choices worksheet.** settlements.csv (and
   wards.csv) ship as form attachments. The settlement question uses
   `select_one_from_file settlements.csv`, so the list is looked up from disk at
   render time rather than compiled into the form's XML.

2. **Cascading select, filtered by ward.**
   - 1.02 LGA: `select_one` from a 4-row internal list (lgas.csv) — cheap, no
     external lookup needed.
   - 1.03 Ward: `select_one_from_file wards.csv`, filtered by
     `lga_code = ${lga}` — narrows 40 wards down to ~10 per LGA.
   - 1.04 Settlement: `select_one_from_file settlements.csv`, filtered by
     `ward_code = ${ward}` — narrows 2,524 settlements down to roughly 60 per
     ward on average (2524 / 40 wards), not 2,500.
   This is the actual mechanism that avoids both the XML bloat and the giant list:
   filtering happens before rendering, so the device only ever holds ~60 rows in
   the visible choice list at once.

3. **search() appearance (autocomplete) on top of the filtered list**, so the ~60
   ward-level settlement options can be typed against instead of scrolled — a
   second layer of usability on top of the cascade, not a replacement for it.

4. **pulldata() to auto-populate settlement coordinates into hidden fields**,
   pulled from settlements.csv/settlements.geojson once a settlement is selected,
   feeding the 1.11 GPS plausibility check (compare the live GPS reading against
   the settlement's registered coordinates; this is a soft check, not a hard
   constraint, since dwellings aren't at the settlement centroid).

## What this needs in the test plan
- Confirm ward selection correctly filters the settlement list to only that
  ward's settlements.
- Confirm settlement code and name populate consistently together (no
  code/name mismatch).
- Confirm the cascade resets correctly if an enumerator backs up and changes
  the LGA or ward after already selecting a settlement.
