# ==================================================
# import
# ==================================================
from pathlib import Path
import sqlite3
from openpyxl import Workbook, load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.worksheet.table import TableStyleInfo
from openpyxl.formatting.rule import CellIsRule, Rule
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
import pandas as pd

# ==========================
# from modules
# ==========================
from modules.data_loader import read_csv, save_df_to_sqlite
from modules.database_validator import count_table_rows
from modules.sql_loader import load_sql, read_sql
from modules.kpi_calculator import calculate_share_ratios, calculate_summary_kpis
from modules.setting_logging import setup_logging
from modules.excel_exporter import (
    build_summary_sheet,
    build_carrier_sheet,
    build_prefecture_sheet,
    build_detail_sheet,
    build_check_sheet,
)
from modules.validator import (
    validate_kpi_consistency,
    validate_excel_sheets,
    validate_excel_formulas,
)

# ==================================================
# paths
# ==================================================
# ==========================
# CSV
# ==========================
area_master_csv = Path("data") / "area_master.csv"
carrier_master_csv = Path("data") / "carrier_master.csv"
carrier_rate_master_csv = Path("data") / "carrier_rate_master.csv"
delivery_records_csv = Path("data") / "delivery_records.csv"

# ==========================
# database
# ==========================
db_path = Path("database") / "logistics_kpi.db"

# ==========================
# SQL
# ==========================
summary_sql = Path("sql") / "summary.sql"
carrier_kpi_summary_sql = Path("sql") / "carrier_kpi_summary.sql"
prefecture_summary_sql = Path("sql") / "prefecture_summary.sql"
delivery_detail_sql = Path("sql") / "delivery_detail.sql"
master_mismatches_sql = Path("sql") / "master_mismatches.sql"

# ==========================
# # output
# ==========================
output_dir = "output"
output_file = "logistics_kpi_report.xlsx"
output_path = Path(output_dir) / output_file

# ==================================================
# openpyxl設定
# ==================================================
# ==========================
# table_style
# ==========================
TABLE_STYLE = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)

# ==========================
# font_style
# ==========================
TITLE_FONT = Font(
    size=16,
    bold=True,
    color="FFFFFF",
)
HEADING_FONT = Font(bold=True, color="FFFFFF")

# ==========================
# fill_style
# ==========================
TITLE_FILL = PatternFill(fill_type="solid", fgColor="4F81BD")
HEADING_FILL = PatternFill(fill_type="solid", fgColor="4F81BD")

# ==========================
# SECTION
# ==========================
ALIGN_CENTER = Alignment(horizontal="center", vertical="center")


# ==========================
# format
# ==========================
THOUSANDS_FORMAT = "#,##0"
PERCENT_FORMAT = "0.0%"
DECIMAL_2_FORMAT = "#,##0.00"
DATE_FORMAT = "yyyy/mm/dd"

# ==========================
# border
# ==========================
# side --------------------
THIN_SIDE = Side(style="thin", color="000000")
# border --------------------
BORDER_BOTTOM = Border(bottom=THIN_SIDE)


# ==================================================
# rules
# ==================================================
# ==========================
# carrier_rule
# ==========================
def create_carrier_rule(max_row: int) -> Rule:
    return CellIsRule(
        operator="greaterThanOrEqual",
        # NOTE
        # summary作成後に差し替え検討
        formula=[f"AVERAGE($D$2:$D${max_row})"],
        fill=PatternFill(
            fill_type="solid",
            fgColor="FFC7CE",
            bgColor="FFC7CE",
        ),
    )


# ==========================
# check_rule
# ==========================
def create_check_rule(text: str, fill: PatternFill) -> Rule:
    return CellIsRule(
        operator="equal",
        formula=[f'"{text}"'],
        fill=fill,
    )


ng_fill = PatternFill(
    fill_type="solid",
    fgColor="FFC7CE",
    bgColor="FFC7CE",
)

ok_fill = PatternFill(
    fill_type="solid",
    fgColor="B5D8ED",
    bgColor="B5D8ED",
)


# ==================================================
# logger設定
# ==================================================
log_config = {"level": "INFO", "file_path": "logs/app.log"}

logger = setup_logging(log_config)


# ==================================================
# main
# ==================================================
def main():

    # ==========================
    # マスターCSV読み込み
    # ==========================
    area_master_df = read_csv(area_master_csv)
    carrier_master_df = read_csv(carrier_master_csv)
    carrier_rate_master_df = read_csv(carrier_rate_master_csv)
    delivery_records_df = read_csv(delivery_records_csv)

    logger.info("CSV読み込み完了")

    # ==========================
    # dbフォルダ作成
    # ==========================
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # ==========================
    # SQLite接続
    # ==========================
    conn = sqlite3.connect(db_path)

    try:
        # ==================================================
        # df SQLite保存
        # ==================================================
        table_name_df_pairs = {
            "area_master": area_master_df,
            "carrier_master": carrier_master_df,
            "carrier_rate_master": carrier_rate_master_df,
            "delivery_records": delivery_records_df,
        }

        for table_name, df in table_name_df_pairs.items():
            save_df_to_sqlite(table_name, conn, df)

        logger.info("SQLite保存完了")

        # ==========================
        # テーブル件数確認
        # ==========================
        logger.info("各テーブルの件数")

        for table_name, df in table_name_df_pairs.items():
            table_rows = count_table_rows(table_name, conn)
            logger.info(f"{table_name}: {table_rows} 件")

        # ==================================================
        # マスター不一致確認
        # ==================================================
        master_mismatches_df = read_sql(load_sql(master_mismatches_sql), conn)

        if master_mismatches_df.empty:
            logger.info("マスター不整合無し")

        else:
            raise ValueError(
                f"マスター不一致 値の無い列を確認してください\n{master_mismatches_df}"
            )

        # ==================================================
        # SQL読み込み
        # ==================================================
        summary_df = read_sql(load_sql(summary_sql), conn)
        carrier_kpi_summary_df = read_sql(load_sql(carrier_kpi_summary_sql), conn)
        prefecture_summary_df = read_sql(load_sql(prefecture_summary_sql), conn)
        delivery_detail_df = read_sql(load_sql(delivery_detail_sql), conn)

        # ==================================================
        # KPI計算
        # ==================================================
        # ==========================
        # carrier_kpi_summary
        # ==========================
        # --------------------------
        # share_ratio
        # --------------------------
        carrier_kpi_summary_df_added_kpi = calculate_share_ratios(
            carrier_kpi_summary_df
        )

        logger.info("配送会社別KPI集計完了")

        print(carrier_kpi_summary_df_added_kpi["carrier_name"].tolist())
        print(carrier_kpi_summary_df_added_kpi)

        # ==========================
        # summary
        # ==========================
        summary_df_added_kpi = calculate_summary_kpis(
            summary_df, carrier_kpi_summary_df_added_kpi, delivery_records_df
        )

        logger.info("Summary(全体KPI)集計完了")

        print(summary_df_added_kpi)

        # ==========================
        # prefecture_summary
        # ==========================
        prefecture_summary_added_kpi_df = calculate_share_ratios(prefecture_summary_df)

        logger.info("都道府県別KPI集計完了")

        print(prefecture_summary_added_kpi_df)

        # ==================================================
        # detail
        # ==================================================
        date_cols = ["delivery_date", "completion_date"]
        delivery_detail_df[date_cols] = delivery_detail_df[date_cols].apply(
            pd.to_datetime
        )

    # ==========================
    # SQLite接続終了
    # ==========================
    finally:
        conn.close()

    # ==================================================
    # Excel書き込み
    # ==================================================
    wb = Workbook()

    ws_summary: Worksheet = wb.active
    ws_summary.title = "Summary"
    ws_carrier: Worksheet = wb.create_sheet("Carrier")
    ws_prefecture: Worksheet = wb.create_sheet("Prefecture")
    ws_detail: Worksheet = wb.create_sheet("Detail")
    ws_check: Worksheet = wb.create_sheet("Check")

    # ==========================
    # Carrierシート
    # ==========================
    build_carrier_sheet(
        carrier_kpi_summary_df_added_kpi,
        ws_carrier,
        TABLE_STYLE,
        THOUSANDS_FORMAT,
        PERCENT_FORMAT,
        HEADING_FONT,
        rule=create_carrier_rule,
    )

    # ==========================
    # Summaryシート
    # ==========================
    build_summary_sheet(
        summary_df_added_kpi,
        ws_carrier,
        ws_summary,
        TITLE_FONT,
        TITLE_FILL,
        ALIGN_CENTER,
        BORDER_BOTTOM,
        THOUSANDS_FORMAT,
        DECIMAL_2_FORMAT,
        DATE_FORMAT,
    )

    # ==========================
    # Prefectureシート
    # ==========================
    build_prefecture_sheet(
        prefecture_summary_added_kpi_df,
        ws_prefecture,
        HEADING_FONT,
        HEADING_FILL,
        BORDER_BOTTOM,
        THOUSANDS_FORMAT,
        PERCENT_FORMAT,
    )

    # ==========================
    # Detailシート
    # ==========================
    build_detail_sheet(
        delivery_detail_df,
        ws_detail,
        HEADING_FONT,
        HEADING_FILL,
        ALIGN_CENTER,
        DATE_FORMAT,
        THOUSANDS_FORMAT,
    )

    # ==========================
    # Checkシート
    # ==========================
    build_check_sheet(
        ws_check,
        ws_summary,
        ws_detail,
        HEADING_FONT,
        HEADING_FILL,
        ALIGN_CENTER,
        create_check_rule,
        ok_fill,
        ng_fill,
    )

    # ==========================
    # check_by_python
    # ==========================
    validate_kpi_consistency(
        summary_df_added_kpi, delivery_detail_df, carrier_kpi_summary_df_added_kpi
    )

    # ==========================
    # Excel保存
    # ==========================
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        wb.save(output_path)

    except OSError as e:
        raise OSError(f"ファイル保存に失敗しました: {output_path}") from e

    # ==================================================
    # Excel読み込み/検証
    # ==================================================
    try:
        loaded_wb = load_workbook(output_path, data_only=False)

    except FileNotFoundError as e:
        raise FileNotFoundError(f"ファイルが見つかりません: {output_path}") from e

    validate_excel_sheets(loaded_wb)
    validate_excel_formulas(loaded_wb)


# ==================================================
# entrypoint
# ==================================================
if __name__ == "__main__":
    logger.info("【処理開始】logistics_kpi_analysis")

    try:
        main()

    except ValueError as e:
        logger.error(f"【異常終了】 {e}")

    except OSError as e:
        logger.error(f"【異常終了】 {e}")

    except FileNotFoundError as e:
        logger.error(f"【異常終了】 {e}")

    except Exception as e:
        logger.exception(f"【異常終了】 {e}")

    else:
        logger.info("【正常終了】")
