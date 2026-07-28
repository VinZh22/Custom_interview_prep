import pytest

from coding.lib.two_sum import two_sum, two_sum_sorted


@pytest.mark.parametrize(
    "nums,target",
    [
        ([2, 7, 11, 15], 9),
        ([3, 2, 4], 6),
        ([3, 3], 6),          # duplicate values, distinct indices
        ([-1, -2, -3, -4], -7),
        ([0, 0], 0),
    ],
)
def test_two_sum_finds_a_valid_pair(nums, target):
    i, j = two_sum(nums, target)
    assert i != j
    assert nums[i] + nums[j] == target


def test_two_sum_raises_when_absent():
    with pytest.raises(ValueError):
        two_sum([1, 2, 3], 100)


def test_does_not_reuse_the_same_element():
    # 4 appears once; 4 + 4 == 8 must not be accepted.
    with pytest.raises(ValueError):
        two_sum([4, 1, 2], 8)


@pytest.mark.parametrize(
    "nums,target",
    [
        ([1, 2, 3, 4, 6], 10),
        ([-5, -2, 0, 3, 9], 1),
        ([1, 1], 2),
    ],
)
def test_two_sum_sorted_matches(nums, target):
    lo, hi = two_sum_sorted(nums, target)
    assert lo < hi
    assert nums[lo] + nums[hi] == target
