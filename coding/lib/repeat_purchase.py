"""Repeat-purchase latency — see coding/data-manipulation/001-example-repeat-purchase-latency.md."""

import pandas as pd


def days_to_second_order(orders: pd.DataFrame) -> pd.DataFrame:
    """Days between each user's first and second order.

    Args:
        orders: columns `user_id`, `order_id`, `ts` (datetime64), `amount`.
            Rows may arrive in any order.

    Returns:
        DataFrame with columns `user_id` and `days_to_second_order` (float),
        one row per user who placed at least two orders, sorted by `user_id`.
        Users with a single order are excluded rather than reported as NaN.
    """
    ranked = orders.sort_values(["user_id", "ts"], kind="stable").assign(
        k=lambda df: df.groupby("user_id").cumcount()
    )
    first_two = ranked.loc[ranked["k"] < 2]

    # diff() within the group is NaT on each user's first row, so the rows that
    # survive notna() are exactly the second orders — single-order users drop out
    # without a special case.
    gap = first_two.groupby("user_id")["ts"].diff()
    return (
        first_two.loc[gap.notna(), ["user_id"]]
        .assign(days_to_second_order=gap.dropna().dt.total_seconds() / 86400)
        .sort_values("user_id", kind="stable")
        .reset_index(drop=True)
    )
