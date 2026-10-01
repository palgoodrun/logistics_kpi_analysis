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

    # ==========================
    # dbフォルダ作成
    # ==========================
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # ==========================
    # SQLite接続
    # ==========================
    conn = sqlite3.connect(db_path)

    # ==================================================
    # df SQLite保存
    # ==================================================
    save_df_to_sqlite("area_master", conn, area_master_df)
    save_df_to_sqlite("carrier_master", conn, carrier_master_df)
    save_df_to_sqlite("carrier_rate_master", conn, carrier_rate_master_df)
    save_df_to_sqlite("delivery_records", conn, delivery_records_df)

    # ==========================
    # テーブル件数確認
    # ==========================
    count_table_rows("area_master", conn)
    count_table_rows("carrier_master", conn)
    count_table_rows("carrier_rate_master", conn)
    count_table_rows("delivery_records", conn)

    # ==================================================
    # マスター不一致確認
    # ==================================================
    master_mismatches_df = read_sql(load_sql(master_mismatches_sql), conn)

    if master_mismatches_df.empty:
        print("マスター不整合無し")

    else:
        conn.close()
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
    carrier_kpi_summary_df_added_kpi = calculate_share_ratios(carrier_kpi_summary_df)

    print(carrier_kpi_summary_df_added_kpi)

    # ==========================
    # SQLite接続終了
    # ==========================
    conn.close()


# ==================================================
# entrypoint
# ==================================================
if __name__ == "__main__":
    print("logistics_kpi_analysis\n【処理開始】")

    error = False

    try:
        main()

    except ValueError as e:
        print(f"【異常終了】 {e}")
        error = True

    if not error:
        print("【正常終了】")
