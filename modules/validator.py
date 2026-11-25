# ==================================================
# import
# ==================================================
import pandas as pd
import math
from openpyxl import workbook


# ==================================================
# validate_kpi_consistency()
# ==================================================
def validate_kpi_consistency(
    summary_df_added_kpi: pd.DataFrame,
    delivery_detail_df: pd.DataFrame,
    carrier_kpi_summary_df_added_kpi: pd.DataFrame,
) -> None:

    check_ng_results = []

    check_count = summary_df_added_kpi["total_deliveries"].iloc[0] == len(
        delivery_detail_df
    )

    if not check_count:
        check_ng_results.append("配送件数")

    check_total_amount = (
        carrier_kpi_summary_df_added_kpi["total_freight"].sum()
        == delivery_detail_df["freight_rate"].sum()
    )
    if not check_total_amount:
        check_ng_results.append("総運賃")

    check_freight_share_ratio = math.isclose(
        carrier_kpi_summary_df_added_kpi["freight_share"].sum(),
        1.0,
        rel_tol=0,
        abs_tol=1e-9,
    )

    if not check_freight_share_ratio:
        check_ng_results.append("構成比")

    if check_ng_results:
        raise ValueError(
            f"KPI整合性チェックでNGが発生しました NG箇所: {", ".join(check_ng_results)}"
        )


# ==================================================
# validate_excel_sheets()
# ==================================================
def validate_excel_sheets(wb: workbook) -> None:

    expected_sheets = [
        "Summary",
        "Carrier",
        "Prefecture",
        "Detail",
        "Check",
    ]

    loaded_sheets = wb.sheetnames

    missing_sheets = []

    for sheet in expected_sheets:

        if sheet not in loaded_sheets:
            missing_sheets.append(sheet)

    if missing_sheets:
        raise ValueError(
            f"Excelファイルに必要なシートが不足しています\n不足シート: {f', '.join(missing_sheets)}"
        )


# ==================================================
# validate_excel_formulas()
# ==================================================
def validate_excel_formulas(wb: workbook) -> None:

    ws_summary = wb["Summary"]
    ws_detail = wb["Detail"]
    ws_check = wb["Check"]

    ws_summary_formulas = ["B5", "B6"]
    ws_detail_formulas = ["J2", f"J{ws_detail.max_row}"]
    ws_check_formulas = ["B2", "B3", "B4"]

    formulas_dict = {
        ws_summary: ws_summary_formulas,
        ws_detail: ws_detail_formulas,
        ws_check: ws_check_formulas,
    }

    invalid_formula_cells = {}

    for ws, cell_addresses in formulas_dict.items():
        for address in cell_addresses:
            cell = ws[address]

            if cell.data_type != "f":
                if ws.title not in invalid_formula_cells:
                    invalid_formula_cells[ws.title] = []
                invalid_formula_cells[ws.title].append(cell.coordinate)

    print(invalid_formula_cells)

    if invalid_formula_cells:

        error_details = []

        for sheet_name, addresses in invalid_formula_cells.items():
            error_details.append(f"{sheet_name}: {', '.join(addresses)}")

        raise ValueError(
            "所定のセルに数式が設定されていません\n" + "\n".join(error_details)
        )
