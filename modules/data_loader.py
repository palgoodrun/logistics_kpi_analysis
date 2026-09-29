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
