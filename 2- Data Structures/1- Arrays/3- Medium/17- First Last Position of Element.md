# Find First and Last Position of Element in Sorted Array

`Amazon` • `Google` • `Microsoft` • `Meta` • `Apple` • `Bloomberg` • `LinkedIn` • `Uber` • `Oracle`

<br>

## Problem Statement
Given an array of integers `nums` sorted in non-decreasing order, find the starting and ending index of a given `target` value.

If the target is not found in the array, return `[-1, -1]`.

You must write an algorithm with `O(log n)` runtime complexity.

## Examples
**Example 1:**
```
Input:  nums = [5,7,7,8,8,10], target = 8
Output: [3,4]
```

**Example 2:**
```
Input:  nums = [5,7,7,8,8,10], target = 6
Output: [-1,-1]
```

**Example 3:**
```
Input:  nums = [], target = 0
Output: [-1,-1]
```

## Constraints
- `0 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`
- `nums` is a non-decreasing array.
- `-10^9 <= target <= 10^9`

<br><br>

## Approach 1: Linear Scan
The most direct idea is to walk through the array once. The first index where we see the target becomes the start, and we keep overwriting the end index every time we see the target again. This does not meet the required `O(log n)` bound, but it is a good baseline to reason about correctness.

```python
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        req_range = [-1, -1]
        first_occurence_found = False

        for i, num in enumerate(nums):
            if num == target:
                req_range[1] = i               # always update the end index
                if not first_occurence_found:  # record the start only once
                    req_range[0] = i
                    first_occurence_found = True

        return req_range
```

**Time:** `O(n)`  |  **Space:** `O(1)`

<br><br>

## Approach 2: Lower Bound and Upper Bound
Because the array is sorted, we can use two classic binary search helpers instead of scanning.

- `lower_bound` returns the first index where `nums[i] >= target`. If the target exists, this is exactly its first occurrence.
- `upper_bound` returns the first index where `nums[i] > target`. The last occurrence of the target therefore sits at `upper_bound - 1`.

**The two cases where the target does not exist**

After computing the lower bound, there are exactly two situations that tell us the target is absent. In both, we return `[-1, -1]` immediately and never bother computing the upper bound.

1. **The lower bound equals the length of the array.** This means every element is smaller than the target, so the target would sit past the last index. It simply is not in the array.
2. **The lower bound is a valid index, but `nums[lower_bound] != target`.** The lower bound only guarantees the first position whose value is greater than or equal to the target. If that value is strictly greater than the target, then the target itself never appears.

```python
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        lb = self.lower_bound(nums, target)

        # Case 1: lb ran past the end   -> target is larger than every element
        # Case 2: value at lb != target -> target is missing entirely
        # Either way the element does not exist, so skip the upper bound search.
        if lb == len(nums) or nums[lb] != target:
            return [-1, -1]

        # ub is the first index strictly greater than target,
        # so the last occurrence lives at ub - 1.
        ub = self.upper_bound(nums, target)
        return [lb, ub - 1]

    def lower_bound(self, nums: List[int], target: int) -> int:
        # First index i where nums[i] >= target
        lo, hi = 0, len(nums)   # hi is exclusive
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] < target:
                lo = mid + 1    # target must be to the right
            else:
                hi = mid        # mid could be the answer, keep it in range
        return lo

    def upper_bound(self, nums: List[int], target: int) -> int:
        # First index i where nums[i] > target
        lo, hi = 0, len(nums)   # hi is exclusive
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] <= target:
                lo = mid + 1    # need a value strictly greater, move right
            else:
                hi = mid
        return lo
```

**Time:** `O(log n)`  |  **Space:** `O(1)`

<br><br>

## Approach 3: Plain Binary Search (No Bound Helpers)
An interviewer may ask you to solve this without leaning on the lower bound and upper bound idea. In that case we run two ordinary binary searches, each one biased toward a different side.

- To find the **first** occurrence: when `nums[mid] == target`, record `mid` as a candidate, then keep searching to the **left** in case an earlier match exists.
- To find the **last** occurrence: when `nums[mid] == target`, record `mid` as a candidate, then keep searching to the **right** in case a later match exists.

If the first occurrence comes back as `-1`, the target is absent, so the last occurrence is absent too and we can return early.

```python
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        first = self.find_first(nums, target)

        # If there is no first occurrence, there is no last one either.
        if first == -1:
            return [-1, -1]

        last = self.find_last(nums, target)
        return [first, last]

    def find_first(self, nums: List[int], target: int) -> int:
        lo, hi = 0, len(nums) - 1
        result = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                result = mid     # candidate found, keep looking left
                hi = mid - 1
            elif nums[mid] < target:
                lo = mid + 1     # go right
            else:
                hi = mid - 1     # go left
        return result

    def find_last(self, nums: List[int], target: int) -> int:
        lo, hi = 0, len(nums) - 1
        result = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                result = mid     # candidate found, keep looking right
                lo = mid + 1
            elif nums[mid] < target:
                lo = mid + 1     # go right
            else:
                hi = mid - 1     # go left
        return result
```

**Time:** `O(log n)`  |  **Space:** `O(1)`

<br><br>

## Related Problems
- [Binary Search (LeetCode 704)](https://leetcode.com/problems/binary-search/)
- [Search Insert Position (LeetCode 35)](https://leetcode.com/problems/search-insert-position/)
- [First Bad Version (LeetCode 278)](https://leetcode.com/problems/first-bad-version/)
- [Search in Rotated Sorted Array (LeetCode 33)](https://leetcode.com/problems/search-in-rotated-sorted-array/)
- [Find Minimum in Rotated Sorted Array (LeetCode 153)](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)
- [Sqrt(x) (LeetCode 69)](https://leetcode.com/problems/sqrtx/)

<br><br>

## Related Concepts
- Lower Bound
- Upper Bound
- Binary Search