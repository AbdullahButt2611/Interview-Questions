# Find Peak Element

`Meta` • `Amazon` • `Google` • `Bloomberg` • `Hudson River Trading` • `Quora`

## Problem Statement
A peak element is an element that is strictly greater than its neighbors.

Given a 0-indexed integer array `nums`, find a peak element and return its index. If the array contains multiple peaks, return the index to **any** of the peaks.

You may imagine that `nums[-1] = nums[n] = -∞`. In other words, an element is always considered to be strictly greater than a neighbor that is outside the array.

<mark>You must write an algorithm that runs in O(log n) time.</mark>

## Examples
**Example 1:**

```
Input: nums = [1,2,3,1]
Output: 2
Explanation: 3 is a peak element and your function should return the index number 2.
```

**Example 2:**

```
Input: nums = [1,2,1,3,5,6,4]
Output: 5
Explanation: Your function can return either index 1 (value 2) or index 5 (value 6).
```

## Constraints
- `1 <= nums.length <= 1000`
- `-2^31 <= nums[i] <= 2^31 - 1`
- `nums[i] != nums[i + 1]` for all valid `i`.

<br><br>

## Approach 1: Linear Search
The most direct idea is to walk through the array once and check every element against its neighbors.

Key observations:

- A single element is always a peak because both of its sides are treated as `-∞`.
- For any index, the left neighbor is `-∞` when it is the first index, and the right neighbor is `-∞` when it is the last index.
- The first index where an element beats both its neighbors is a valid answer.

```python
class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        n = len(nums)

        # A single element is always a peak (both sides are -infinity)
        if n == 1:
            return 0

        for i in range(n):
            # Left side is fine if i is the first index or current beats left
            left_ok = i == 0 or nums[i] > nums[i - 1]
            # Right side is fine if i is the last index or current beats right
            right_ok = i == n - 1 or nums[i] > nums[i + 1]

            if left_ok and right_ok:
                return i

        return -1
```

**Complexity**

- Time: `O(n)` since we may scan the whole array.
- Space: `O(1)` as we only use a loop variable.

This is simple and correct, but it does not meet the required `O(log n)` bound, so we optimize next.

<br><br>

## Approach 2: Binary Search (Final)
Even though the array is not sorted, we can still binary search on the **slope**.

Core intuition:

- If `nums[mid] > nums[mid + 1]`, we are on a downward slope, so a peak lies at `mid` or to its left.
- If `nums[mid] < nums[mid + 1]`, we are on an upward slope, so a peak must lie to the right.
- Moving toward the larger neighbor always keeps us on a rising path that must eventually fall, which guarantees a peak.

<mark>Always move toward the greater neighbor, because a peak is guaranteed to exist on that side.</mark>

We first handle the boundary peaks (single element, first, and last), then binary search on the inner elements.

```python
class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        n = len(nums)

        # If Only one element in array
        if n == 1:
            return 0

        # If first element is the peak: On left its -infinity < nums[0] > nums[1]
        if nums[0] > nums[1]:
            return 0

        # If last element is the peak: On left its nums[n-1] < nums[n-1] > -infinity
        if nums[n-1] > nums[n-2]:
            return n-1

        # Iterate for the rest of the elements
        low = 1
        high = n - 2

        while low <= high:
            mid = (low + high) // 2

            if nums[mid - 1] < nums[mid] and nums[mid] > nums[mid + 1]:
                return mid
            elif nums[mid - 1] < nums[mid]:
                low = mid + 1
            else:
                high = mid - 1

        return -1
```

**Dry Run** on `nums = [1, 2, 1, 3, 5, 6, 4]`

```txt
nums = [1, 2, 1, 3, 5, 6, 4], n = 7

Boundary checks:
  n == 1?              No
  nums[0] > nums[1]?   1 > 2  -> No
  nums[6] > nums[5]?   4 > 6  -> No

low = 1, high = 5

Iteration 1: mid = 3   (values around mid: 1, 3, 5)
  nums[2] < nums[3] and nums[3] > nums[4]?  1 < 3 and 3 > 5  -> No
  nums[2] < nums[3]?  Yes  -> move right, low = 4

Iteration 2: mid = 4   (values around mid: 3, 5, 6)
  nums[3] < nums[4] and nums[4] > nums[5]?  3 < 5 and 5 > 6  -> No
  nums[3] < nums[4]?  Yes  -> move right, low = 5

Iteration 3: mid = 5   (values around mid: 5, 6, 4)
  nums[4] < nums[5] and nums[5] > nums[6]?  5 < 6 and 6 > 4  -> Yes
  Peak found at index 5

Return 5
```

**Complexity**

- Time: `O(log n)` since we halve the search space each step.
- Space: `O(1)` as we only use pointers.

<br><br>

## Related Problems
- [Find a Peak Element II](https://leetcode.com/problems/find-a-peak-element-ii/)
- [Peak Index in a Mountain Array](https://leetcode.com/problems/peak-index-in-a-mountain-array/)
- [Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)
- [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/)
- [Single Element in a Sorted Array](https://leetcode.com/problems/single-element-in-a-sorted-array/)