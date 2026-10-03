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

    df["freight_share"] = df["total_freight"] / total_freight_of_all

    return df
