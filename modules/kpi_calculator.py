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


# ==================================================
# calculate_summary_kpis
# ==================================================
def calculate_summary_kpis(
    summary_df: pd.DataFrame,
    carrier_kpi_summary_df_added_kpi: pd.DataFrame,
    delivery_records_df: pd.DataFrame,
) -> pd.DataFrame:

    summary_df_added_kpi = summary_df.copy()

    summary_df_added_kpi["carrier_counts"] = len(carrier_kpi_summary_df_added_kpi)

    min_date = min(pd.to_datetime(delivery_records_df["delivery_date"]))
    max_date = max(pd.to_datetime(delivery_records_df["delivery_date"]))

    summary_df_added_kpi["min_date"] = min_date
    summary_df_added_kpi["max_date"] = max_date

    return summary_df_added_kpi
