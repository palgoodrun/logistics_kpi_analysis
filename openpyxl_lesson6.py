# ==================================================
# import
# ==================================================
from pathlib import Path
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.utils import get_column_letter


# ==================================================
# create_template()
# ==================================================
def create_template(template_path: Path) -> None:

    # ==========================
    # style_setting
    # ==========================
    title_font = Font(bold=True, size=16)

    header_font = Font(color="FFFFFF", bold=True)
    header_fill = PatternFill(fgColor="24466B", fill_type="solid")

    integer_format = "#,##0"

    # ==========================
    # wb
    # ==========================

    wb = Workbook()

    # ==========================
    # summary_ws
    # ==========================

    summary_ws: Worksheet = wb.active
    summary_ws.title = "Summary"

    summary_ws["A1"] = "物流月次報告書"
    summary_ws["A3"] = "対象月"
    summary_ws["B3"] = "2026年9月"
    summary_ws["A5"] = "配送数量"
    summary_ws["B5"] = 3500
    summary_ws["A6"] = "配送単価"
    summary_ws["B6"] = 150
    summary_ws["A7"] = "運賃合計"
    summary_ws["B7"] = "=B5*B6"

    # style --------------------

    summary_ws["A1"].font = title_font

    for row in summary_ws.iter_rows(
        min_row=5,
        max_row=summary_ws.max_row,
        min_col=1,
        max_col=1,
    ):
        for cell in row:
            cell.font = header_font
            cell.fill = header_fill

    for row in summary_ws.iter_rows(
        min_row=5,
        max_row=summary_ws.max_row,
        min_col=2,
        max_col=2,
    ):
        for cell in row:
            cell.number_format = integer_format

    summary_ws.column_dimensions["A"].width = 20
    summary_ws.column_dimensions["B"].width = 20

    # ==========================
    # carrier_ws
    # ==========================

    carrier_ws: Worksheet = wb.create_sheet("Carrier")

    carrier_ws["A1"] = "配送会社"
    carrier_ws["A2"] = "Carrier A"
    carrier_ws["A3"] = "Carrier B"
    carrier_ws["A4"] = "Carrier C"
    carrier_ws["B1"] = "配送数量"
    carrier_ws["B2"] = 1200
    carrier_ws["B3"] = 800
    carrier_ws["B4"] = 1500
    carrier_ws["C1"] = "配送単価"
    carrier_ws["C2"] = 150
    carrier_ws["C3"] = 160
    carrier_ws["C4"] = 140
    carrier_ws["D1"] = "運賃"
    carrier_ws["D2"] = "=B2*C2"
    carrier_ws["D3"] = "=B3*C3"
    carrier_ws["D4"] = "=B4*C4"

    # style --------------------

    for row in carrier_ws.iter_rows(
        min_row=1,
        max_row=1,
        min_col=1,
        max_col=carrier_ws.max_column,
    ):
        for cell in row:
            cell.font = header_font
            cell.fill = header_fill

    for row in carrier_ws.iter_rows(
        min_row=2,
        max_row=carrier_ws.max_row,
        min_col=2,
        max_col=carrier_ws.max_column,
    ):
        for cell in row:
            cell.number_format = integer_format

    carrier_ws.column_dimensions["A"].width = 25

    for col_index in range(2, carrier_ws.max_column + 1):
        col_letter = get_column_letter(col_index)
        carrier_ws.column_dimensions[col_letter].width = 15

    carrier_ws.freeze_panes = "A2"

    # ==========================
    # save
    # ==========================

    wb.save(template_path)


# ==================================================
# update_report()
# ==================================================
def update_report(template_path: Path, output_path: Path) -> None:

    wb = load_workbook(template_path)

    # ==========================
    # velidation
    # ==========================

    # --------------------------
    # sheets
    # --------------------------

    required_sheets = ["Summary", "Carrier"]

    missing_sheets = [sheet for sheet in required_sheets if sheet not in wb.sheetnames]

    if missing_sheets:
        raise ValueError(f"必要なシートがありません: {','.join(missing_sheets)}")

    # --------------------------
    # heading
    # --------------------------
    # summary --------------------
    ws_summary: Worksheet = wb["Summary"]

    required_heading_summary = {
        "A3": "対象月",
        "A5": "配送数量",
        "A6": "配送単価",
        "A7": "運賃合計",
    }

    invalid_heading_summary = []

    for coodinate, expected in required_heading_summary.items():
        if ws_summary[coodinate].value != expected:
            invalid_heading_summary.append({coodinate: expected})

    if invalid_heading_summary:
        raise ValueError(
            f"Summaryシートに必要な見出しがありません: {invalid_heading_summary})"
        )

    if ws_summary["B7"].value != "=B5*B6":
        raise ValueError(f"Summaryシートに必要な計算式がありません B7: =B5*B6")

    # carrier --------------------
    ws_carrier: Worksheet = wb["Carrier"]

    required_heading_carrier = {
        "A1": "配送会社",
        "B1": "配送数量",
        "C1": "配送単価",
        "D1": "運賃",
    }

    invalid_heading_carrier = []

    for coodinate, expected in required_heading_carrier.items():
        if ws_carrier[coodinate].value != expected:
            invalid_heading_carrier.append({coodinate: expected})

    if invalid_heading_carrier:
        raise ValueError(
            f"Carrierシートに必要な見出しがありません: {invalid_heading_carrier})"
        )

    required_calc_carrier = {
        "D2": "=B2*C2",
        "D3": "=B3*C3",
        "D4": "=B4*C4",
    }

    invalid_calc_carrier = []

    for coodinate, expected in required_calc_carrier.items():
        if ws_carrier[coodinate].value != expected:
            invalid_calc_carrier.append({coodinate: expected})

    if invalid_calc_carrier:
        raise ValueError(
            f"Carrierシートに必要な見出しがありません: {invalid_calc_carrier}"
        )

    # ==========================
    # update
    # ==========================
    # --------------------------
    # Summary
    # --------------------------
    ws_summary["B3"] = "2026年10月"
    ws_summary["B5"] = 4200
    ws_summary["B6"] = 160

    # --------------------------
    # Carrier
    # --------------------------
    ws_carrier["B2"] = 1400
    ws_carrier["C2"] = 155
    ws_carrier["B3"] = 900
    ws_carrier["C3"] = 165
    ws_carrier["B4"] = 1900
    ws_carrier["C4"] = 145

    # ==========================
    # save
    # ==========================
    wb.save(output_path)


# ==================================================
# validate_report()
# ==================================================
def validate_report(output_path: Path) -> None:

    wb = load_workbook(output_path)

    # ==========================
    # sheetname
    # ==========================
    expected_sheetnames = ["Summary", "Carrier"]

    if wb.sheetnames != expected_sheetnames:
        raise ValueError(f"シート名を確認してください 期待値: {expected_sheetnames}")

    # ==========================
    # value
    # ==========================
    # --------------------------
    # Summary
    # --------------------------
    ws_summary = wb["Summary"]

    expected_values_summary = {
        "B3": "2026年10月",
        "B5": 4200,
        "B6": 160,
        "B7": "=B5*B6",
    }

    invalid_values_summary = []

    for coodinate, expected in expected_values_summary.items():
        if ws_summary[coodinate].value != expected:
            invalid_values_summary.append({coodinate: expected})

    if invalid_values_summary:
        raise ValueError(
            f"Summaryシートに必要な値がありません 期待値: {invalid_values_summary}"
        )

    expected_fill_summary = PatternFill(fgColor="24466B", fill_type="solid")

    if ws_summary["A5"].fill != expected_fill_summary:
        raise ValueError(
            f"Sammaryシートの書式設定が設定と異なります 期待値: {expected_fill_summary}"
        )

    # --------------------------
    # Carrier
    # --------------------------
    ws_carrier = wb["Carrier"]

    expected_values_carrier = {
        "B2": 1400,
        "C2": 155,
        "D2": "=B2*C2",
        "D3": "=B3*C3",
        "D4": "=B4*C4",
    }

    invalid_values_carrier = []

    for coodinate, expected in expected_values_carrier.items():
        if ws_carrier[coodinate].value != expected:
            invalid_values_carrier.append({coodinate: expected})

    if invalid_values_carrier:
        raise ValueError(
            f"Carrierシートに必要な値がありません 期待値: {invalid_values_carrier}"
        )

    expected_freeze_panes_carrier = "A2"

    if ws_carrier.freeze_panes != expected_freeze_panes_carrier:
        raise ValueError(
            f"Carrierシートのシート固定位置が異なります 期待値:{expected_freeze_panes_carrier}"
        )

    print(f"検証成功: {output_path}")


# ==================================================
# main()
# ==================================================
def main():

    template_path = Path("templates/opx_lesson6_template.xlsx")

    template_path.parent.mkdir(parents=True, exist_ok=True)

    output_path = Path("output/openpyxl_lesson6.xlsx")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    create_template(template_path)

    update_report(template_path, output_path)

    validate_report(output_path)


# ==================================================
# entrypoint
# ==================================================
if __name__ == "__main__":
    main()
