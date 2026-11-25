# ==================================================
# import
# ==================================================
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Font, PatternFill, Alignment, Border
from openpyxl.cell.cell import Cell
import pandas as pd


# ==================================================
# build_summary_sheet
# ==================================================
def build_summary_sheet(
    df: pd.DataFrame,
    ws_carrier: Worksheet,
    ws_summary: Worksheet,
    TITLE_FONT: Font,
    TITLE_FILL: PatternFill,
    ALIGN_CENTER: Alignment,
    BORDER_BOTTOM: Border,
    THOUSANDS_FORMAT: str,
    DECIMAL_2_FORMAT: str,
    DATE_FORMAT: str,
) -> None:

    summary_items = [
        ("総配送件数", df["total_deliveries"].iloc[0]),
        ("総出荷個数", df["total_quantity"].iloc[0]),
        ("総運賃", f"=SUM({ws_carrier.title}!D2:D{ws_carrier.max_row})"),
        ("平均運賃", "=B5/B3"),
        ("配送会社数", df["carrier_counts"].iloc[0]),
        (
            "集計開始日",
            df["min_date"].iloc[0],
        ),
        (
            "集計終了日",
            df["max_date"].iloc[0],
        ),
    ]

    ws_summary["A1"] = "物流KPIレポート"

    for row_num, (label, value) in enumerate(summary_items, start=3):
        ws_summary.cell(row=row_num, column=1, value=label)
        ws_summary.cell(row=row_num, column=2, value=value)

    # --------------------------
    # 書式設定
    # --------------------------
    ws_summary.merge_cells("A1:B1")

    ws_summary["A1"].font = TITLE_FONT
    ws_summary["A1"].fill = TITLE_FILL
    ws_summary["A1"].alignment = ALIGN_CENTER

    for row in ws_summary.iter_rows(
        min_row=3,
        max_row=ws_summary.max_row,
        min_col=1,
        max_col=2,
    ):
        for cell in row:
            cell.border = BORDER_BOTTOM

    number_formats = [
        (["B3", "B4", "B5", "B7"], THOUSANDS_FORMAT),
        (["B6"], DECIMAL_2_FORMAT),
        (["B8", "B9"], DATE_FORMAT),
    ]

    for cells, fmt in number_formats:
        for cell in cells:
            ws_summary[cell].number_format = fmt

    for col in range(1, ws_summary.max_column + 1):
        ws_summary.column_dimensions[f"{get_column_letter(col)}"].width = 12


# ==================================================
# build_carrier_sheet
# ==================================================
def build_carrier_sheet(
    df: pd.DataFrame,
    ws: Worksheet,
    table_style: TableStyleInfo,
    THOUSANDS_FORMAT: str,
    PERCENT_FORMAT: str,
    HEADING_FONT: str,
    rule: CellIsRule,
) -> None:
    # 値の設定
    for row_index, row in enumerate(
        dataframe_to_rows(df, index=False, header=True),
        start=1,
    ):
        for col_index, value in enumerate(row, start=1):
            ws.cell(row=row_index, column=col_index, value=value)

    # テーブルの設定
    table = Table(
        displayName="CarrierTable",
        ref=f"A1:{get_column_letter(ws.max_column)}{ws.max_row}",
    )
    table.tableStyleInfo = table_style
    ws.add_table(table)

    # 表示設定
    for row in ws.iter_rows(
        min_row=2,
        max_row=ws.max_row,
        min_col=2,
        max_col=4,
    ):
        for cell in row:
            cell.number_format = THOUSANDS_FORMAT

    for row in ws.iter_rows(
        min_row=2,
        max_row=ws.max_row,
        min_col=5,
        max_col=6,
    ):
        for cell in row:
            cell.number_format = PERCENT_FORMAT

    # 条件付き書式設定
    carrier_rule = rule(ws.max_row)
    ws.conditional_formatting.add(f"D2:D{ws.max_row}", carrier_rule)

    # フォント設定（見出し）
    for row in ws.iter_rows(
        min_row=1,
        max_row=1,
        min_col=1,
        max_col=ws.max_column,
    ):
        for cell in row:
            cell.font = HEADING_FONT

    # 列幅設定
    for col in range(1, ws.max_column + 1):
        ws.column_dimensions[f"{get_column_letter(col)}"].width = 20


# ==================================================
# build_prefecture_sheet
# ==================================================
def build_prefecture_sheet(
    df: pd.DataFrame,
    ws: Worksheet,
    HEADING_FONT: str,
    HEADING_FILL: str,
    BORDER_BOTTOM: Border,
    THOUSANDS_FORMAT: str,
    PERCENT_FORMAT: str,
) -> None:
    # 値の設定
    for row_index, row in enumerate(
        dataframe_to_rows(df, index=False, header=True),
        start=1,
    ):
        for col_index, value in enumerate(row, start=1):
            ws.cell(row=row_index, column=col_index, value=value)

    # フォント設定（見出し）
    for row in ws.iter_rows(
        min_row=1,
        max_row=1,
        min_col=1,
        max_col=ws.max_column,
    ):
        for cell in row:
            cell.font = HEADING_FONT
            cell.fill = HEADING_FILL

    # 罫線設定
    for row in ws.iter_rows(
        min_row=1,
        max_row=ws.max_row,
        min_col=1,
        max_col=ws.max_column,
    ):
        for cell in row:
            cell.border = BORDER_BOTTOM

    # 表示設定
    for row in ws.iter_rows(
        min_row=2,
        max_row=ws.max_row,
        min_col=2,
        max_col=4,
    ):
        for cell in row:
            cell.number_format = THOUSANDS_FORMAT

    for row in ws.iter_rows(
        min_row=2,
        max_row=ws.max_row,
        min_col=5,
        max_col=6,
    ):
        for cell in row:
            cell.number_format = PERCENT_FORMAT

    ws.auto_filter.ref = f"A1:{get_column_letter(ws.max_column)}{ws.max_row}"

    # 列幅設定
    for col in range(1, ws.max_column + 1):
        ws.column_dimensions[f"{get_column_letter(col)}"].width = 20


# ==================================================
# build_detail_sheet
# ==================================================
def build_detail_sheet(
    df: pd.DataFrame,
    ws: Worksheet,
    HEADING_FONT: Font,
    HEADING_FILL: PatternFill,
    ALIGN_CENTER: Alignment,
    DATE_FORMAT: str,
    THOUSANDS_FORMAT: str,
) -> None:
    for row_index, row in enumerate(
        dataframe_to_rows(df, index=False, header=True), start=1
    ):
        for col_index, value in enumerate(row, start=1):
            ws.cell(row=row_index, column=col_index, value=value)

    ws[f"{get_column_letter(ws.max_column+1)}1"] = "運賃合計"

    last_col = ws.max_column

    left_col = get_column_letter(last_col - 1)

    for row in range(2, ws.max_row + 1):
        ws.cell(row=row, column=last_col, value=f"={left_col}{row}")

    # --------------------------
    # 見出し表示設定
    # --------------------------
    for col in range(1, ws.max_column + 1):
        cell = ws.cell(row=1, column=col)
        cell.font = HEADING_FONT
        cell.fill = HEADING_FILL
        cell.alignment = ALIGN_CENTER

    # --------------------------
    # 書式設定
    # --------------------------
    # 日付 --------------------
    for col in [2, 8]:
        for row in range(2, ws.max_row + 1):
            cell: Cell = ws.cell(row=row, column=col)
            cell.number_format = DATE_FORMAT

    # 桁区切り --------------------
    for row in ws.iter_rows(
        min_row=2,
        max_row=ws.max_row,
        min_col=9,
        max_col=10,
    ):
        for cell in row:
            cell.number_format = THOUSANDS_FORMAT

    # 列幅 --------------------
    for col in range(1, ws.max_column + 1):
        ws.column_dimensions[f"{get_column_letter(col)}"].width = 20

    # ウィンドウ枠の固定 --------------------
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(ws.max_column)}{ws.max_row}"


# ==================================================
# build_check_sheet
# ==================================================
def build_check_sheet(
    ws_check: Worksheet,
    ws_summary: Worksheet,
    ws_detail: Worksheet,
    HEADING_FONT: Font,
    HEADING_FILL: PatternFill,
    ALIGN_CENTER: Alignment,
    rule: CellIsRule,
    ok_fill: PatternFill,
    ng_fill: PatternFill,
) -> None:

    check_item = [
        ("項目", "比較対象"),
        (
            "配送件数",
            f'=IF({ws_summary.title}!B3=COUNTA({ws_detail.title}!A2:A{ws_detail.max_row}),"OK","NG")',
        ),
        (
            "総運賃",
            f'=IF({ws_summary.title}!B5=SUM({ws_detail.title}!J2:J{ws_detail.max_row}),"OK","NG")',
        ),
        ("構成比", '=IF(SUM(CarrierTable[freight_share])=1,"OK","NG")'),
    ]

    for row_number, (lavel, value) in enumerate(check_item, start=1):
        ws_check.cell(row=row_number, column=1, value=lavel)
        ws_check.cell(row=row_number, column=2, value=value)

    # --------------------------
    # 表示形式
    # --------------------------
    # 見出し --------------------
    for col in range(1, ws_check.max_column + 1):
        cell = ws_check.cell(row=1, column=col)
        cell.font = HEADING_FONT
        cell.fill = HEADING_FILL
        cell.alignment = ALIGN_CENTER

    # --------------------------
    # 条件書式
    # --------------------------
    ok_rule = rule("OK", ok_fill)
    ng_rule = rule("NG", ng_fill)

    ws_check.conditional_formatting.add(f"B2:B{ws_check.max_row}", ok_rule)
    ws_check.conditional_formatting.add(f"B2:B{ws_check.max_row}", ng_rule)

    # --------------------------
    # 列幅調整
    # --------------------------
    for col in range(1, ws_check.max_column + 1):
        ws_check.column_dimensions[f"{get_column_letter(col)}"].width = 10
