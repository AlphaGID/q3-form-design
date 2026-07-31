"""
Builds the HH2026 XLSForm from plain Python lists.
Re-run this whole script every time the form changes; don't hand-edit the .xlsx.
"""
import csv
import openpyxl

HEADER = ["type", "name", "label", "hint", "required", "relevant",
          "constraint", "constraint_message", "calculation", "appearance",
          "choice_filter", "default", "readonly"]

def row(type_, name, label, hint="", required="", relevant="", constraint="",
        constraint_message="", calculation="", appearance="", choice_filter="",
        default="", readonly=""):
    return [type_, name, label, hint, required, relevant, constraint,
            constraint_message, calculation, appearance, choice_filter,
            default, readonly]

wb = openpyxl.Workbook()

# --- settings ---
settings_sheet = wb.active
settings_sheet.title = "settings"
settings_sheet.append(["form_title", "form_id", "version", "default_language", "style"])
settings_sheet.append(["Integrated Child Health and AMR Survey 2026", "hh2026_v1", "2026070200", "en", "pages"])

# --- survey ---
survey_sheet = wb.create_sheet("survey")
survey_sheet.append(HEADER)

survey_rows = [
    row("begin group", "section1", "Section 1: Household identification"),

    row("select_one lga_list", "lga", "1.02 Local Government Area", required="yes"),

    row("select_one_from_file wards.csv", "ward", "1.03 Ward",
        required="yes", choice_filter="lga_code=${lga}"),

    row("select_one_from_file settlements.csv", "settlement", "1.04 Settlement",
        required="yes", choice_filter="ward_code=${ward}"),

    row("select_one yesno", "settlement_known_locally",
        "1.05 Is the settlement known locally by a different name?", required="yes"),
    row("text", "settlement_local_name", "Name used locally",
        relevant="${settlement_known_locally}='1'",
        required="${settlement_known_locally}='1'"),

    row("integer", "structure_number", "1.06 Structure number painted on the dwelling",
        required="yes", constraint=". >= 1 and . <= 999",
        constraint_message="Enter a number between 1 and 999"),

    row("integer", "hh_serial_number", "1.07 Household serial number within the settlement",
        required="yes", constraint=". >= 1 and . <= 999",
        constraint_message="Enter a number between 1 and 999"),

    row("select_one_from_file staff_roster.csv", "enumerator_code", "1.08 Enumerator code",
        required="yes", choice_filter="role='Enumerator'"),

    row("calculate", "team_code_calc", "",
        calculation="pulldata('staff_roster','team_code','name',${enumerator_code})"),
    row("text", "team_code_display", "1.09 Team code",
        calculation="${team_code_calc}", readonly="yes"),

    row("date", "visit_date", "1.10 Date of visit", required="yes",
        constraint=". >= date('2026-06-01') and . <= date('2026-06-30')",
        constraint_message="Date must be within the fieldwork period, 1-30 June 2026"),

    row("geopoint", "gps_reading",
        "1.11 Record the GPS reading taken at the entrance to the dwelling.", required="yes"),
    row("calculate", "gps_lat", "", calculation="substring-before(${gps_reading},' ')"),
    row("calculate", "gps_lon", "",
        calculation="substring-before(substring-after(${gps_reading},' '),' ')"),
    row("calculate", "settlement_lat_calc", "",
        calculation="pulldata('settlements','latitude','name',${settlement})"),
    row("calculate", "settlement_lon_calc", "",
        calculation="pulldata('settlements','longitude','name',${settlement})"),
    row("note", "gps_plausibility_flag",
        "This GPS reading looks far from the registered location of the selected settlement. Please confirm this is the correct dwelling before continuing.",
        relevant="(${gps_reading}!='') and ((abs(number(${gps_lat}) - number(${settlement_lat_calc})) > 0.05) or (abs(number(${gps_lon}) - number(${settlement_lon_calc})) > 0.05))"),

    row("select_one visited_previous_list", "prev_round_visited",
        "1.12 Was this household visited during the October 2025 round?", required="yes"),
    row("text", "prev_household_id",
        "1.13 Record the household identifier allocated in the October 2025 round.",
        relevant="${prev_round_visited}='1'",
        constraint="pulldata('previous_round_households','household_id','household_id',.) != ''",
        constraint_message="This household ID was not found in the previous round register. Please check and re-enter."),

    row("select_one visit_result_list", "result_of_visit", "1.14 Result of visit", required="yes"),

    row("end group", "", ""),
]

for r in survey_rows:
    survey_sheet.append(r)

# --- choices ---
choices_sheet = wb.create_sheet("choices")
choices_sheet.append(["list_name", "name", "label"])

# LGA list read from the actual data file, not retyped
with open("data/reference/lgas.csv") as f:
    reader = csv.DictReader(f)
    for lga in reader:
        choices_sheet.append(["lga_list", lga["name"], lga["label"]])

choices_sheet.append(["yesno", "1", "Yes"])
choices_sheet.append(["yesno", "2", "No"])

choices_sheet.append(["visited_previous_list", "1", "Yes"])
choices_sheet.append(["visited_previous_list", "2", "No"])
choices_sheet.append(["visited_previous_list", "8", "Do not know"])

choices_sheet.append(["visit_result_list", "1", "Completed"])
choices_sheet.append(["visit_result_list", "2", "Refused"])
choices_sheet.append(["visit_result_list", "3", "No competent adult after three visits"])
choices_sheet.append(["visit_result_list", "4", "Dwelling vacant or demolished"])

wb.save("form/HH2026v1.xlsx")
print("form/HH2026v1.xlsx written with Section 1")
