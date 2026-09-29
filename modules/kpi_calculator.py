# ==================================================
# import
# ==================================================
import pandas as pd


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
