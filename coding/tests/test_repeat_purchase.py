import pandas as pd
from pandas.testing import assert_frame_equal

from coding.lib.repeat_purchase import days_to_second_order


def make_orders(rows):
    df = pd.DataFrame(rows, columns=["user_id", "order_id", "ts", "amount"])
    df["ts"] = pd.to_datetime(df["ts"])
    return df


# Deliberately unsorted, and covering: a user with three orders (only the first
# two count), a user with one order (excluded), and two orders at the same
# instant (zero-day gap).
ORDERS = make_orders(
    [
        ("u2", 5, "2026-03-01 09:00", 10.0),
        ("u1", 1, "2026-01-01 12:00", 20.0),
        ("u1", 3, "2026-01-20 12:00", 5.0),
        ("u3", 6, "2026-02-10 00:00", 15.0),
        ("u1", 2, "2026-01-04 00:00", 30.0),
        ("u2", 4, "2026-03-01 09:00", 12.0),
    ]
)


def test_gap_uses_the_first_two_orders_and_drops_single_order_users():
    expected = pd.DataFrame(
        {
            "user_id": ["u1", "u2"],
            "days_to_second_order": [2.5, 0.0],
        }
    )
    assert_frame_equal(days_to_second_order(ORDERS), expected)


def test_input_is_not_mutated():
    before = ORDERS.copy()
    days_to_second_order(ORDERS)
    assert_frame_equal(ORDERS, before)


def test_no_user_has_a_second_order():
    orders = make_orders([("u1", 1, "2026-01-01 12:00", 20.0)])
    result = days_to_second_order(orders)
    assert list(result.columns) == ["user_id", "days_to_second_order"]
    assert result.empty


def test_row_count_never_exceeds_the_user_count():
    result = days_to_second_order(ORDERS)
    assert len(result) <= ORDERS["user_id"].nunique()
    assert not result["user_id"].duplicated().any()
