# ==================================================
# import
# ==================================================
import sqlite3
import pandas as pd
from pathlib import Path

# ==================================================
# SQL
# ==================================================
# ==========================
# delivery_records_added_codes
# ==========================
delivery_records_added_codes = """
    SELECT
        DR.delivery_id,
        DR.carrier_name,
        CM.carrier_code,
        DR.prefecture,
        AM.area_code,
        DR.quantity
    FROM delivery_records AS DR
    LEFT JOIN carrier_master AS CM
        ON DR.carrier_name = CM.carrier_name
    JOIN area_master AS AM
        ON DR.prefecture = AM.prefecture;
"""


# ==================================================
# read_sql
# ==================================================
def read_sql(sql: str, conn: sqlite3.Connection) -> pd.DataFrame:

    df = pd.read_sql(sql, conn)

    print(f"SQL読み取り成功 件数: {len(df)}件")

    return df


# ==================================================
# main
# ==================================================
def main():
    db_path = Path("database") / "logistics_kpi.db"

    conn = sqlite3.connect(db_path)

    delivery_records_added_codes_df = read_sql(delivery_records_added_codes, conn)

    # NOTE
    # 結果確認用 logに書き替え予定
    print(delivery_records_added_codes_df)

    conn.close()


# ==================================================
# entrypoint
# ==================================================
if __name__ == "__main__":
    main()
