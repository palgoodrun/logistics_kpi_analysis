# ==================================================
# import
# ==================================================
import sqlite3


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
