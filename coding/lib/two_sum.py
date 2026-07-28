"""Two Sum — see coding/algorithms/001-example-two-sum.md."""


def two_sum(nums: list[int], target: int) -> tuple[int, int]:
    """Return indices of the two entries of `nums` summing to `target`.

    One pass, checking the complement before inserting so an element is never
    paired with itself.

    Raises:
        ValueError: if no such pair exists.
    """
    seen: dict[int, int] = {}
    for i, x in enumerate(nums):
        j = seen.get(target - x)
        if j is not None:
            return j, i
        seen[x] = i
    raise ValueError("no pair sums to target")


def two_sum_sorted(nums: list[int], target: int) -> tuple[int, int]:
    """Same, for sorted input: O(n) time, O(1) extra space."""
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        total = nums[lo] + nums[hi]
        if total == target:
            return lo, hi
        if total < target:
            lo += 1
        else:
            hi -= 1
    raise ValueError("no pair sums to target")
