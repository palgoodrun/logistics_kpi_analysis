import pandas as pd
from pathlib import Path
from openpyxl import Workbook, load_workbook
from zipfile import BadZipFile

from excel_report import build_carrier_sheet, build_raw_data_sheet, build_summary_sheet

# ==================================================
# input_data
# ==================================================
input_data = pd.DataFrame(
    [
        ["佐川急便", 1500, 160],
        ["ヤマト運輸", 1100, 175],
        ["日本郵便", 2000, 140],
        ["西濃運輸", 800, 190],
        ["その他", 500, 150],
    ],
    columns=["配送会社", "出荷個数", "単価"],
)

# ==================================================
# output_path
# ==================================================
output_path = Path("output/lesson8_report.xlsx")


# ==================================================
# main
# ==================================================
def main():

    wb = Workbook()

    ws_carrier = wb.active
    ws_carrier.title = "Carrier"
    ws_raw_data = wb.create_sheet("RawData")
    ws_summary = wb.create_sheet("Summary")

    build_carrier_sheet(ws_carrier, input_data)

    build_raw_data_sheet(ws_raw_data, ws_carrier)

    build_summary_sheet(ws_summary, ws_carrier)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    wb.save(output_path)

    try:
        loaded_wb = load_workbook(output_path)

    except FileNotFoundError:
        raise FileNotFoundError(
            f"指定されたファイルが見つかりません file {output_path}"
        )

    except BadZipFile as e:
        raise BadZipFile(f"Excelファイルの読み込みに失敗しました: {e}")

    expected_sheets = ["Carrier", "RawData", "Summary"]

    missing_sheets = [
        sheet for sheet in expected_sheets if sheet not in loaded_wb.sheetnames
    ]

    if missing_sheets:
        raise ValueError(
            f"指定されたシートが存在しません 不足シート: {",".join(missing_sheets)}"
        )


# ==================================================
# entrypoint
# ==================================================
if __name__ == "__main__":
    main()
