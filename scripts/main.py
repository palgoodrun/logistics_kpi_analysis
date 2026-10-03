# ==================================================
# import
# ==================================================
from pathlib import Path
import sqlite3

# ==========================
# from modules
# ==========================
from modules.data_loader import read_csv, save_df_to_sqlite
from modules.database_validator import count_table_rows
from modules.sql_loader import load_sql, read_sql
from modules.kpi_calculator import calculate_share_ratios
from modules.setting_logging import setup_logging

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
carrier_kpi_summary_sql = Path("sql") / "carrier_kpi_summary.sql"
master_mismatches_sql = Path("sql") / "master_mismatches.sql"

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
        carrier_kpi_summary_df = read_sql(load_sql(carrier_kpi_summary_sql), conn)

        # ==================================================
        # KPI計算
        # ==================================================
        # ==========================
        # share_ratio
        # ==========================
        carrier_kpi_summary_df_added_kpi = calculate_share_ratios(
            carrier_kpi_summary_df
        )

        logger.info("配送会社別KPI集計完了")

        print(carrier_kpi_summary_df_added_kpi)

    # ==========================
    # SQLite接続終了
    # ==========================
    finally:
        conn.close()


# ==================================================
# entrypoint
# ==================================================
if __name__ == "__main__":
    logger.info("【処理開始】logistics_kpi_analysis")

    try:
        main()
        logger.info("【正常終了】")

    except ValueError as e:
        logger.error(f"【異常終了】 {e}")

    except Exception as e:
        logger.exception(f"【異常終了】 {e}")
