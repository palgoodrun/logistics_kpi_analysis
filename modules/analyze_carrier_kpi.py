# ==================================================
# import
# ==================================================
import pandas as pd
from pathlib import Path
import sqlite3

# ==================================================
# sql
# ==================================================
# ==================================================
# delivery_records_added_carrier_rate
# ==================================================
delivery_records_added_carrier_rate = """
    SELECT
        DR.carrier_name,
        COUNT(*) AS delivery_count,
        SUM(DR.quantity) AS total_quantity,
        SUM(CRM.freight_rate) AS total_freight
    FROM delivery_records AS DR
    LEFT JOIN carrier_master AS CM
        ON DR.carrier_name = CM.carrier_name
    LEFT JOIN area_master AS AM
        ON DR.prefecture = AM.prefecture
    LEFT JOIN carrier_rate_master AS CRM
        ON CM.carrier_code = CRM.carrier_code
        AND AM.area_code = CRM.area_code
    GROUP BY DR.carrier_name;
"""


# ==================================================
# read_sql
# ==================================================
def read_sql(sql: str, conn: sqlite3.Connection) -> pd.DataFrame:

    df = pd.read_sql(sql, conn)

    # NOTE
    # 確認用 log書き替え予定
    print(f"件数: {len(df)}")

    return df


# ==================================================
# main
# ==================================================
def main():

    db_path = Path("database") / "logistics_kpi.db"

    conn = sqlite3.connect(db_path)

    carrier_summary_df = read_sql(
        delivery_records_added_carrier_rate, conn
    )

    conn.close()

    return carrier_summary_df
