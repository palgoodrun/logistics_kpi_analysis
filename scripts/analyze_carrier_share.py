# ==================================================
# import
# ==================================================
import pandas as pd

# ==========================
# from modules
# ==========================
from modules import analyze_carrier_kpi


# ==================================================
# calculate_share_ratios
# ==================================================
def calculate_share_ratios(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    delivery_count_of_all = df["delivery_count"].sum()

    total_freight_of_all = df["total_freight"].sum()

    df["delivery_share"] = df["delivery_count"] / delivery_count_of_all

    # NOTE
    # 確認用要削除
    total_ratios_of_delivery_share = df["delivery_share"].sum()
    print(f"1.0になっていることを確認してください->: {total_ratios_of_delivery_share}")

    df["freight_share"] = df["total_freight"] / total_freight_of_all

    # NOTE
    # 確認用要削除
    total_ratios_of_freght_share = df["freight_share"].sum()
    print(f"1.0になっていることを確認してください->: {total_ratios_of_freght_share}")

    return df


# ==================================================
# main
# ==================================================
def main():

    carrier_summary_df = analyze_carrier_kpi.main()

    carrier_summary_added_share_ratios_df = calculate_share_ratios(carrier_summary_df)

    # NOTE
    # 確認用 log置き換え予定
    print(f"実行後件数: {len(carrier_summary_added_share_ratios_df)}")
    print(carrier_summary_added_share_ratios_df)


# ==================================================
# entrypoint
# ==================================================
if __name__ == "__main__":
    main()
