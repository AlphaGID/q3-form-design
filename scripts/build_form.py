"""
Builds the HH2026 XLSForm from plain Python lists.
Run this, then convert with pyxform, every time the form changes.
"""
import openpyxl

wb = openpyxl.Workbook()

# --- settings sheet ---
settings_sheet = wb.active
settings_sheet.title = "settings"
settings_sheet.append(["form_title", "form_id", "version", "default_language", "style"])
settings_sheet.append(["Integrated Child Health and AMR Survey 2026", "hh2026_v1", "2026070100", "en", "pages"])

# --- survey sheet (skeleton only for now — just a title screen, to prove conversion works) ---
survey_sheet = wb.create_sheet("survey")
survey_sheet.append(["type", "name", "label", "hint", "required", "relevant", "constraint", "constraint_message", "calculation", "appearance"])
survey_sheet.append(["note", "form_intro", "Integrated Child Health and Antimicrobial Resistance Survey 2026 — Household Questionnaire", "", "", "", "", "", "", ""])

# --- choices sheet (empty for now — internal lists only go here, external files handled separately) ---
choices_sheet = wb.create_sheet("choices")
choices_sheet.append(["list_name", "name", "label"])

wb.save("form/HH2026v1.xlsx")
print("form/HH2026v1.xlsx written")
