from openpyxl_lesson8 import main
from openpyxl import load_workbook
from pathlib import Path

# ==================================================
# output_path
# ==================================================
output_path = Path("output/lesson8_report.xlsx")


# ==================================================
# test_expected_sheets
# ==================================================
def test_expected_sheets():

    main()

    wb = load_workbook(output_path)

    expected_sheets = ["Carrier", "RawData", "Summary"]

    assert wb.sheetnames == expected_sheets


# ==================================================
# test_carrier_value
# ==================================================
def test_carrier_value():

    main()

    wb = load_workbook(output_path)
    ws = wb["Carrier"]

    assert ws["D2"].value == "=B2*C2"


# ==================================================
# test_summary_value
# ==================================================
def test_summary_value():

    main()

    wb = load_workbook(output_path)
    ws = wb["Summary"]

    assert ws["B5"].value == "=B4/B3"
