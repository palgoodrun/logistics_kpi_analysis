# ==================================================
# import
# ==================================================
from pathlib import Path
import pandas as pd
import sqlite3


# ==================================================
# read_csv
# ==================================================
def read_csv(data: Path) -> pd.DataFrame:
    df = pd.read_csv(data)

    return df


# ==================================================
# save_df_to_sqlite
# ==================================================
def save_df_to_sqlite(
    table_name: str,
    con: sqlite3.Connection,
    df: pd.DataFrame,
) -> None:

    df.to_sql(table_name, con, if_exists="replace")


# ==================================================
# count_table_rows()
# ==================================================
def count_table_rows(table_name: str, conn: sqlite3.Connection) -> None:

    table_rows = f"""
        SELECT COUNT(*)
        FROM {table_name}
    """

    cursor = conn.execute(table_rows)
    result = cursor.fetchone()
    result = result[0]

    print(f"件数確認 {table_name}: {result} 件")


# ==================================================
# main
# ==================================================
def main():
    area_master_csv = Path("data") / "area_master.csv"
    carrier_master_csv = Path("data") / "carrier_master.csv"
    carrier_rate_master_csv = Path("data") / "carrier_rate_master.csv"
    delivery_records_csv = Path("data") / "delivery_records.csv"

    area_master_df = read_csv(area_master_csv)
    carrier_master_df = read_csv(carrier_master_csv)
    carrier_rate_master_df = read_csv(carrier_rate_master_csv)
    delivery_records_df = read_csv(delivery_records_csv)

    db_path = Path("database") / "logistics_kpi.db"

    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)

    save_df_to_sqlite("area_master", conn, area_master_df)
    save_df_to_sqlite("carrier_master", conn, carrier_master_df)
    save_df_to_sqlite("carrier_rate_master", conn, carrier_rate_master_df)
    save_df_to_sqlite("delivery_records", conn, delivery_records_df)

    count_table_rows("area_master", conn)
    count_table_rows("carrier_master", conn)
    count_table_rows("carrier_rate_master", conn)
    count_table_rows("delivery_records", conn)

    conn.close()


# ==================================================
# entrypoint
# ==================================================

if __name__ == "__main__":
    main()
