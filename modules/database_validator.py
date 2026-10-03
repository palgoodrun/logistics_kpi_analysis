# ==================================================
# import
# ==================================================
import sqlite3


# ==================================================
# count_table_rows()
# ==================================================
def count_table_rows(table_name: str, conn: sqlite3.Connection) -> int:

    table_rows = f"""
        SELECT COUNT(*)
        FROM {table_name}
    """

    cursor = conn.execute(table_rows)
    result = cursor.fetchone()
    result = result[0]

    return result
