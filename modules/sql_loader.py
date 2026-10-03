# ==================================================
# import
# ==================================================
from pathlib import Path
import sqlite3
import pandas as pd


# ==================================================
# load_sql
# ==================================================
def load_sql(path: Path) -> str:

    sql = path.read_text(encoding="utf-8")

    return sql


# ==================================================
# read_sql
# ==================================================
def read_sql(sql: str, conn: sqlite3.Connection) -> pd.DataFrame:

    df = pd.read_sql(sql, conn)

    return df
