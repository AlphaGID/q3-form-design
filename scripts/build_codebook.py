"""
Generates the codebook directly from form/HH2026v1.xlsx, so it can never
drift out of sync with the actual form the way a hand-typed codebook could.
Re-run this any time build_form.py changes.
"""
import csv
import re
import openpyxl

wb = openpyxl.load_workbook("form/HH2026v1.xlsx")
survey = wb["survey"]

header = [c.value for c in survey[1]]
col = {name: i for i, name in enumerate(header)}

rows_out = []
for r in survey.iter_rows(min_row=2, values_only=True):
    type_ = r[col["type"]]
    name = r[col["name"]]
    label = r[col["label"]] or ""
    calculation = r[col["calculation"]] if "calculation" in col else ""

    if type_ in ("begin group", "end group", "begin repeat", "end repeat"):
        continue
    if not name:
        continue

    # pull a question number like "1.04" or "4.13/4.14" off the front of the label, if present
    m = re.match(r"^([\d]+\.[\d]+(?:/[\d]+\.[\d]+)?)\s", label)
    question_number = m.group(1) if m else ""

    if calculation and not question_number:
        kind = "derived/internal (no paper question number)"
    elif type_ == "note":
        kind = "display note (not a stored response)"
    else:
        kind = "enumerator-entered"

    rows_out.append([name, question_number, type_, label, kind])

with open("docs/10-codebook.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["field_name", "question_number", "xlsform_type", "label", "kind"])
    writer.writerows(rows_out)

print(f"wrote docs/10-codebook.csv with {len(rows_out)} fields")
