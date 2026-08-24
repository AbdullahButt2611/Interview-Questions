# Find Minimum in Rotated Sorted Array

`Amazon` • `Google` • `Microsoft` • `Apple` • `Facebook` • `Bloomberg` • `Goldman Sachs` • `LinkedIn` • `Salesforce` • `Uber` • `VMware` • `Walmart Labs` • `Adobe`

## Problem Statement

Suppose an array of length `n` sorted in ascending order is rotated between `1` and `n` times.

For example, the array `nums = [0,1,2,4,5,6,7]` might become:

- `[4,5,6,7,0,1,2]` if it was rotated 4 times
- `[0,1,2,4,5,6,7]` if it was rotated 7 times

Notice that rotating an array `[a[0], a[1], a[2], ..., a[n-1]]` 1 time results in the array `[a[n-1], a[0], a[1], a[2], ..., a[n-2]]`.

Given the sorted rotated array `nums` of unique elements, return the minimum element of this array.

<mark>You must write an algorithm that runs in O(log n) time.</mark>

## Examples

**Example 1**

```ini
Input: nums = [3,4,5,1,2]
Output: 1
Explanation: The original array was [1,2,3,4,5] rotated 3 times.
```

**Example 2**

```ini
Input: nums = [4,5,6,7,0,1,2]
Output: 0
Explanation: The original array was [0,1,2,4,5,6,7] and it was rotated 4 times.
```

**Example 3**

```ini
Input: nums = [11,13,15,17]
Output: 11
Explanation: The original array was [11,13,15,17] and it was rotated 4 times.
```

## Constraints

- `n == nums.length`
- `1 <= n <= 5000`
- `-5000 <= nums[i] <= 5000`
- All the integers of `nums` are unique
- `nums` is sorted and rotated between `1` and `n` times

<br><br>

## Intuition

- A rotated sorted array is really two sorted segments joined at a pivot (for example `[4,5,6]` and `[0,1,2]`).
- The minimum element is exactly the first element of the second segment, so finding the minimum means finding the pivot.
- A linear scan is O(n), so the O(log n) requirement pushes us straight to <mark>binary search</mark>.
- Key observation: for any `mid`, at least one of the two halves is guaranteed to be fully sorted.
- Once we identify the sorted half, its smallest element is known instantly (it is the leftmost element of that half), so we record it as a candidate and discard that half.
- The unsorted half must contain the pivot, so we keep searching there.

<br><br>

## Approach

- Maintain `low`, `high`, and a running `min_element` initialised to infinity.
- Compute `mid = (low + high) // 2`.
- If `nums[low] <= nums[mid]`, the left half is sorted:
  - The smallest value in that half is `nums[low]`, so update `min_element`.
  - Discard the left half by setting `low = mid + 1`.
- Otherwise the right half is sorted:
  - The smallest value in that half is `nums[mid]`, so update `min_element`.
  - Discard the right half by setting `high = mid - 1`.
- Every iteration eliminates half of the search space, which gives O(log n).

<br><br>

## Solution

```python
class Solution:
    def findMin(self, nums: List[int]) -> int:
        low = 0
        high = len(nums) - 1
        min_element = float('inf')

        while low <= high:
            mid = (low + high) // 2

            if nums[low] <= nums[mid]:  # Left half is sorted
                min_element = min(min_element, nums[low])
                low = mid + 1
            else:                       # Right half is sorted
                min_element = min(min_element, nums[mid])
                high = mid - 1

        return min_element
```

<br><br>

## Dry Run

Input: `nums = [4,5,6,7,0,1,2]`

```ini
Initial : low = 0, high = 6, min_element = inf

Step 1  : mid = 3
          nums[low] = 4, nums[mid] = 7  -> 4 <= 7, left half sorted
          min_element = min(inf, 4) = 4
          low = 4

Step 2  : low = 4, high = 6, mid = 5
          nums[low] = 0, nums[mid] = 1  -> 0 <= 1, left half sorted
          min_element = min(4, 0) = 0
          low = 6

Step 3  : low = 6, high = 6, mid = 6
          nums[low] = 2, nums[mid] = 2  -> 2 <= 2, left half sorted
          min_element = min(0, 2) = 0
          low = 7

Loop ends (low > high)
Output  : 0
```

<br><br>

## Optimisation (Early Exit)

- If the current search space `nums[low..high]` is already fully sorted, then `nums[low]` is its minimum and there is no need to keep splitting.
- This does not change the worst case, but it cuts the work on nearly sorted or lightly rotated inputs.

```python
class Solution:
    def findMin(self, nums: List[int]) -> int:
        low = 0
        high = len(nums) - 1
        min_element = float('inf')

        while low <= high:
            # Whole search space is already sorted
            if nums[low] <= nums[high]:
                min_element = min(min_element, nums[low])
                break

            mid = (low + high) // 2

            if nums[low] <= nums[mid]:  # Left half is sorted
                min_element = min(min_element, nums[low])
                low = mid + 1
            else:                       # Right half is sorted
                min_element = min(min_element, nums[mid])
                high = mid - 1

        return min_element
```

<br><br>

## Complexity

- **Time Complexity:** `O(log n)` because half of the remaining search space is discarded in every iteration.
- **Space Complexity:** `O(1)` since only a few pointers and a single tracking variable are used.

<br><br>

## Edge Cases

- **Single element array** (`[5]`): loop runs once and returns `5`.
- **Not rotated / rotated n times** (`[11,13,15,17]`): the left half is always sorted, so `nums[0]` is captured as the minimum.
- **Rotated by n-1** (`[2,3,4,5,1]`): the pivot sits at the very end and the right half branch handles it.
- **Negative values** (`[0,1,2,-3,-2]`): the logic is purely comparison based, so signs do not matter.
- <mark>Duplicates are not allowed here</mark>. If they were, `nums[low] <= nums[mid]` could no longer identify a sorted half reliably, which is exactly what the harder variant (LeetCode 154) tests.

<br><br>

## Related Problems

- [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/)
- [Search in Rotated Sorted Array II](https://leetcode.com/problems/search-in-rotated-sorted-array-ii/)
- [Find Minimum in Rotated Sorted Array II](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/)
- [Find Peak Element](https://leetcode.com/problems/find-peak-element/)
- [Single Element in a Sorted Array](https://leetcode.com/problems/single-element-in-a-sorted-array/)
- [Rotate Array](https://leetcode.com/problems/rotate-array/)