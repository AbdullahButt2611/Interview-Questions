# Count Occurrences in a Sorted Array

`Google` • `Meta` • `Bloomberg`

<br>

## Problem Statement
You are given a sorted array of integers `arr` and an integer `target`. Determine how many times `target` appears in `arr`.

Return the count of occurrences of `target` in the array. If the target is not present, the count is `0`.

## Examples
**Example 1:**
```
Input:  arr = [0, 0, 1, 1, 1, 2, 3], target = 1
Output: 3
Explanation: The number 1 appears 3 times in the array.
```

**Example 2:**
```
Input:  arr = [5, 5, 5, 5, 5, 5], target = 5
Output: 6
Explanation: All elements in the array are 5, so the target appears 6 times.
```

## Constraints
- `1 <= arr.length <= 10^5`
- `-10^9 <= arr[i] <= 10^9`
- `arr` is sorted in non-decreasing order.
- `-10^9 <= target <= 10^9`

<br><br>

## Approach 1: Linear Scan
Walk through the array once and increment a counter every time an element equals the target. This ignores the sorted property and runs in linear time, but it is the simplest correct baseline.

```python
class Solution:
    def countOccurrences(self, arr: List[int], target: int) -> int:
        count = 0
        for num in arr:
            if num == target:   # every match adds one to the tally
                count += 1
        return count
```

**Time:** `O(n)`  |  **Space:** `O(1)`

<br><br>

## Approach 2: Lower Bound and Upper Bound
Since the array is sorted, all copies of the target sit in one contiguous block. We can find where that block starts and where it ends using two binary search helpers.

- `lower_bound` returns the first index where `arr[i] >= target` (the start of the block).
- `upper_bound` returns the first index where `arr[i] > target` (one past the end of the block).

The count is simply the width of that block, `upper_bound - lower_bound`. A nice property: if the target is absent, both bounds land on the same index, so the subtraction naturally gives `0` and we need no special case.

```python
class Solution:
    def countOccurrences(self, arr: List[int], target: int) -> int:
        lb = self.lower_bound(arr, target)   # first index with value >= target
        ub = self.upper_bound(arr, target)   # first index with value >  target

        # ub - lb is the width of the block of targets.
        # If target is absent, lb and ub land on the same index, so this is 0.
        return ub - lb

    def lower_bound(self, arr: List[int], target: int) -> int:
        # First index i where arr[i] >= target
        lo, hi = 0, len(arr)   # hi is exclusive
        while lo < hi:
            mid = (lo + hi) // 2
            if arr[mid] < target:
                lo = mid + 1   # target must be to the right
            else:
                hi = mid       # mid could be the answer, keep it in range
        return lo

    def upper_bound(self, arr: List[int], target: int) -> int:
        # First index i where arr[i] > target
        lo, hi = 0, len(arr)   # hi is exclusive
        while lo < hi:
            mid = (lo + hi) // 2
            if arr[mid] <= target:
                lo = mid + 1   # need a value strictly greater, move right
            else:
                hi = mid
        return lo
```

**Time:** `O(log n)`  |  **Space:** `O(1)`

<br><br>

## Approach 3: Plain Binary Search (No Bound Helpers)
If the interviewer does not allow the lower bound and upper bound idea, run two ordinary binary searches, one biased left to find the first occurrence and one biased right to find the last. Once both indices are known, the count is `last - first + 1`. This directly reuses the first and last position logic from the related problem.

```python
class Solution:
    def countOccurrences(self, arr: List[int], target: int) -> int:
        first = self.find_first(arr, target)

        # Target never appears, so the count is zero.
        if first == -1:
            return 0

        last = self.find_last(arr, target)

        # Every index from first to last (inclusive) holds the target.
        return last - first + 1

    def find_first(self, arr: List[int], target: int) -> int:
        lo, hi = 0, len(arr) - 1
        result = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if arr[mid] == target:
                result = mid     # candidate found, keep looking left
                hi = mid - 1
            elif arr[mid] < target:
                lo = mid + 1     # go right
            else:
                hi = mid - 1     # go left
        return result

    def find_last(self, arr: List[int], target: int) -> int:
        lo, hi = 0, len(arr) - 1
        result = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if arr[mid] == target:
                result = mid     # candidate found, keep looking right
                lo = mid + 1
            elif arr[mid] < target:
                lo = mid + 1     # go right
            else:
                hi = mid - 1     # go left
        return result
```

**Time:** `O(log n)`  |  **Space:** `O(1)`

<br><br>

## Related Problems
- [Find First and Last Position of Element in Sorted Array (LeetCode 34)](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/)
- [Binary Search (LeetCode 704)](https://leetcode.com/problems/binary-search/)
- [Search Insert Position (LeetCode 35)](https://leetcode.com/problems/search-insert-position/)
- [First Bad Version (LeetCode 278)](https://leetcode.com/problems/first-bad-version/)
- [Search in Rotated Sorted Array (LeetCode 33)](https://leetcode.com/problems/search-in-rotated-sorted-array/)

<br><br>

## Related Concepts
- Lower Bound
- Upper Bound
- Binary Search