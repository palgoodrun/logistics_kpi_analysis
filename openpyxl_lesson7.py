import pandas as pd
from pathlib import Path
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import PatternFill

# ==================================================
# input_data
# ==================================================
input_data = pd.DataFrame(
    [
        ["佐川急便", 1500, 160],
        ["ヤマト運輸", 1100, 175],
        ["日本郵便", 2000, 140],
        ["西濃運輸", 800, 190],
        ["その他", 500, 150],
    ],
    columns=["配送会社", "出荷個数", "単価"],
)

# ==================================================
# output_path
# ==================================================
output_path = Path("output/lesson7_report.xlsx")

# ==================================================
# setting
# ==================================================
table_style = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)

# ==================================================
# rule
# ==================================================
carrier_rule = CellIsRule(
    operator="greaterThanOrEqual",
    formula=["250000"],
    fill=PatternFill(
        fill_type="solid",
        fgColor="FFFFC7CE",
        bgColor="FFFFC7CE",
    ),
)

# ==================================================
# format
# ==================================================
THOUSANDS_FORMAT = "#,##0"
DECIMAL_FORMAT = "#,##0.00"


# ==================================================
# build_carrier_sheet
# ==================================================
def build_carrier_sheet(ws: Worksheet, input_data: pd.DataFrame) -> None:

    for row_index, row in enumerate(
        dataframe_to_rows(input_data, index=False, header=True), start=1
    ):
        for col_index, value in enumerate(row, start=1):
            ws.cell(row=row_index, column=col_index, value=value)

    ws["D1"].value = "運賃合計"

    for col in ws.iter_cols(min_row=2, max_row=ws.max_row, min_col=4, max_col=4):
        for cell in col:
            cell_num = cell.row
            cell.value = f"=B{cell_num}*C{cell_num}"

            cell.number_format = THOUSANDS_FORMAT

    # table --------------------
    table = Table(displayName="CarrierTable", ref=f"A1:D{ws.max_row}")
    table.tableStyleInfo = table_style
    ws.add_table(table)

    # rule --------------------
    ws.conditional_formatting.add(f"D2:D{ws.max_row}", carrier_rule)


# ==================================================
# build_raw_data_sheet
# ==================================================
def build_raw_data_sheet(raw_data_ws: Worksheet, carrier_ws: Worksheet) -> None:

    for row in raw_data_ws.iter_rows(
        min_row=1,
        max_row=carrier_ws.max_row,
        min_col=1,
        max_col=3,
    ):
        for cell in row:
            cell.value = carrier_ws[cell.coordinate].value

    raw_data_ws.auto_filter.ref = f"A1:C{raw_data_ws.max_row}"


# ==================================================
# build_summary_sheet
# ==================================================
def build_summary_sheet(summary_ws: Worksheet, carrier_ws: Worksheet) -> None:

    summary_ws["A1"] = "配送実績サマリー"
    summary_ws["A3"] = "総出荷個数"
    summary_ws["A4"] = "総運賃"
    summary_ws["A5"] = "平均単価"

    carrier_ws_sheet_name = carrier_ws.title

    summary_ws["B3"] = f"=SUM({carrier_ws_sheet_name}!B2:B{carrier_ws.max_row})"
    summary_ws["B3"].number_format = THOUSANDS_FORMAT
    summary_ws["B4"] = f"=SUM({carrier_ws_sheet_name}!D2:D{carrier_ws.max_row})"
    summary_ws["B4"].number_format = THOUSANDS_FORMAT
    summary_ws["B5"] = "=B4/B3"
    summary_ws["B5"].number_format = DECIMAL_FORMAT


# ==================================================
# main
# ==================================================
def main():

    wb = Workbook()

    ws_carrier = wb.active
    ws_carrier.title = "Carrier"
    ws_raw_data = wb.create_sheet("RawData")
    ws_summary = wb.create_sheet("Summary")

    build_carrier_sheet(ws_carrier, input_data)

    build_raw_data_sheet(ws_raw_data, ws_carrier)

    build_summary_sheet(ws_summary, ws_carrier)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    wb.save(output_path)


# ==================================================
# entrypoint
# ==================================================
if __name__ == "__main__":
    main()
