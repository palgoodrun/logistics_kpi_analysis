# ==================================================
# import
# ==================================================
from pathlib import Path
from openpyxl import load_workbook
import sqlite3
import pandas as pd
import pytest

from modules.sql_loader import load_sql, read_sql
from modules.kpi_calculator import calculate_share_ratios, calculate_summary_kpis
from modules.data_loader import read_csv
from modules.validator import validate_kpi_consistency
from scripts.main import main

# ==========================
# output
# ==========================
output_dir = "output"
output_file = "logistics_kpi_report.xlsx"
output_path = Path(output_dir) / output_file

# ==================================================
# db_path
# ==================================================
db_path = Path("database") / "logistics_kpi.db"

# ==================================================
# CSV
# ==================================================
delivery_records_csv = Path("data") / "delivery_records.csv"

# ==================================================
# SQL
# ==================================================
carrier_kpi_summary_sql = Path("sql") / "carrier_kpi_summary.sql"
summary_sql = Path("sql") / "summary.sql"
delivery_detail_sql = Path("sql") / "delivery_detail.sql"


# ==================================================
# test_excel_sheets
# ==================================================
def test_excel_sheets():

    main()

    wb = load_workbook(output_path)

    expected_sheets = [
        "Summary",
        "Carrier",
        "Prefecture",
        "Detail",
        "Check",
    ]
    assert wb.sheetnames == expected_sheets


# ==================================================
# test_carrier_sheet
# ==================================================
def test_carrier_sheet():

    main()

    conn = sqlite3.connect(db_path)

    carrier_kpi_summary_df = read_sql(load_sql(carrier_kpi_summary_sql), conn)

    conn.close()

    carrier_kpi_summary_df_added_kpi = calculate_share_ratios(carrier_kpi_summary_df)

    wb = load_workbook(output_path)
    carrier_ws = wb["Carrier"]

    carrier_names_from_df = carrier_kpi_summary_df_added_kpi["carrier_name"].tolist()

    carrier_names_from_ws = [
        cell.value
        for row in carrier_ws.iter_cols(
            min_row=2, max_row=carrier_ws.max_row, min_col=1, max_col=1
        )
        for cell in row
    ]

    assert carrier_names_from_df == carrier_names_from_ws

    for row in carrier_ws.iter_rows(
        min_row=2, max_row=carrier_ws.max_row, min_col=2, max_col=2
    ):
        for cell in row:
            assert (
                cell.value
                == carrier_kpi_summary_df_added_kpi["delivery_count"].iloc[cell.row - 2]
            )

    for row in carrier_ws.iter_rows(
        min_row=2, max_row=carrier_ws.max_row, min_col=4, max_col=4
    ):
        for cell in row:
            assert (
                cell.value
                == carrier_kpi_summary_df_added_kpi["total_freight"].iloc[cell.row - 2]
            )

    assert (
        carrier_ws["C2"].value
        == carrier_kpi_summary_df_added_kpi["total_quantity"].iloc[0]
    )

    assert carrier_ws["E2"].value == pytest.approx(
        carrier_kpi_summary_df_added_kpi["delivery_share"].iloc[0]
    )

    assert carrier_ws["F2"].value == pytest.approx(
        carrier_kpi_summary_df_added_kpi["freight_share"].iloc[0]
    )


# ==================================================
# test_detail_sheet
# ==================================================
def test_detail_sheet():

    main()

    wb = load_workbook(output_path)
    detail_ws = wb["Detail"]

    for col in detail_ws.iter_rows(
        min_row=2, max_row=detail_ws.max_row, min_col=10, max_col=10
    ):
        for cell in col:
            excepted = f"=I{cell.row}"

            assert cell.value == excepted


# ==================================================
# test_summary_sheet
# ==================================================
def test_summary_sheet():

    main()

    delivery_records_df = read_csv(delivery_records_csv)

    wb = load_workbook(output_path)
    summary_ws = wb["Summary"]
    carrier_ws = wb["Carrier"]

    assert summary_ws["B3"].value == len(delivery_records_df)

    assert (
        summary_ws["B5"].value == f"=SUM({carrier_ws.title}!D2:D{carrier_ws.max_row})"
    )


# ==================================================
# test_check_sheet
# ==================================================
def test_check_sheet():

    main()

    conn = sqlite3.connect(db_path)

    summary_df = read_sql(load_sql(summary_sql), conn)
    delivery_detail_df = read_sql(load_sql(delivery_detail_sql), conn)
    carrier_kpi_summary_df = read_sql(load_sql(carrier_kpi_summary_sql), conn)

    conn.close()

    carrier_kpi_summary_df_added_kpi = calculate_share_ratios(carrier_kpi_summary_df)

    delivery_records_df = read_csv(delivery_records_csv)
    summary_df_added_kpi = calculate_summary_kpis(
        summary_df, carrier_kpi_summary_df_added_kpi, delivery_records_df
    )

    date_cols = ["delivery_date", "completion_date"]
    delivery_detail_df[date_cols] = delivery_detail_df[date_cols].apply(pd.to_datetime)

    wb = load_workbook(output_path, data_only=False)
    ws_check = wb["Check"]
    ws_summary = wb["Summary"]
    ws_detail = wb["Detail"]

    check_item = {
        "B2": f'=IF({ws_summary.title}!B3=COUNTA({ws_detail.title}!A2:A{ws_detail.max_row}),"OK","NG")',
        "B3": f'=IF({ws_summary.title}!B5=SUM({ws_detail.title}!J2:J{ws_detail.max_row}),"OK","NG")',
        "B4": '=IF(SUM(CarrierTable[freight_share])=1,"OK","NG")',
    }

    for row in ws_check.iter_rows(
        min_row=2, max_row=ws_check.max_row, min_col=2, max_col=2
    ):
        for cell in row:
            assert cell.value == check_item[cell.coordinate]

    validate_kpi_consistency(
        summary_df_added_kpi,
        delivery_detail_df,
        carrier_kpi_summary_df_added_kpi,
    )
