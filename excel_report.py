import pandas as pd
from openpyxl.worksheet.table import TableStyleInfo, Table
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import PatternFill

# ==================================================
# table_style
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
