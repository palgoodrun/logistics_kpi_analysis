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
# inner_join
# ==========================
delivery_records_by_innner_join = """
    SELECT
        DR.delivery_id,
        DR.carrier_name,
        CM.carrier_code,
        DR.prefecture,
        DR.quantity
    FROM delivery_records AS DR
    INNER JOIN carrier_master AS CM
        ON DR.carrier_name = CM.carrier_name;
"""
# ==========================
# left_join
# ==========================
delivery_records_by_left_join = """
    SELECT
        DR.delivery_id,
        DR.carrier_name,
        CM.carrier_code,
        DR.prefecture,
        DR.quantity
    FROM delivery_records AS DR
    LEFT JOIN carrier_master AS CM
        ON DR.carrier_name = CM.carrier_name;
"""
# ==========================
# is_null
# ==========================
delivery_records_carrier_code_is_null = """
    SELECT
        DR.delivery_id,
        DR.carrier_name,
        CM.carrier_code,
        DR.prefecture,
        DR.quantity
    FROM delivery_records AS DR
    LEFT JOIN carrier_master AS CM
        ON DR.carrier_name = CM.carrier_name
    WHERE carrier_code IS NULL
"""


# ==================================================
# read_sql
# ==================================================
def read_sql(sql: str, conn: sqlite3.Connection) -> pd.DataFrame:

    df = pd.read_sql(sql, conn)

    # NOTE
    # 確認用 logへ書き変え予定
    print(f"件数: {len(df)}件")

    return df


# ==================================================
# main
# ==================================================
def main():

    db_path = Path("database") / "logistics_kpi.db"

    conn = sqlite3.connect(db_path)

    delivery_records_by_innner_join_df = read_sql(delivery_records_by_innner_join, conn)

    delivery_records_by_left_join_df = read_sql(delivery_records_by_left_join, conn)

    delivery_records_carrier_code_is_null_df = read_sql(
        delivery_records_carrier_code_is_null, conn
    )

    print(delivery_records_carrier_code_is_null_df)

    conn.close()


# ==================================================
# entrypoint
# ==================================================
if __name__ == "__main__":
    main()
