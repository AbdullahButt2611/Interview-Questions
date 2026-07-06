# Search Insert Position

`Amazon` • `Apple` • `Facebook` • `Microsoft` • `VMware` • `Adobe` • `Uber` • `Google` • `Bloomberg` • `LinkedIn`

## Problem Statement

Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.

You must write an algorithm with O(log n) runtime complexity.

## Examples

Example 1:
```
Input: nums = [1,3,5,6], target = 5
Output: 2
```

Example 2:
```
Input: nums = [1,3,5,6], target = 2
Output: 1
```

Example 3:
```
Input: nums = [1,3,5,6], target = 7
Output: 4
```

## Constraints

- `1 <= nums.length <= 10^4`
- `-10^4 <= nums[i] <= 10^4`
- `nums` contains distinct values sorted in ascending order
- `-10^4 <= target <= 10^4`

<br><br>

## Approach: Binary Search (Lower Bound)

**Idea**

The insert position is simply the first index whose value is greater than or equal to `target`.

- If `target` exists in the array, that first index is exactly where it sits.
- If `target` is missing, that same index is where it would slot in to keep the array sorted.
- If every element is smaller than `target`, the answer is `n` (it goes at the very end).

Because the array is sorted, we can binary search for this boundary in O(log n) instead of scanning linearly.

**Solution Code**

```python
class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        n = len(nums)
        low = 0
        high = n - 1
        ans = n
        while low <= high:
            mid = (low + high) // 2
            if nums[mid] >= target:
                ans = mid
                high = mid - 1
            else:
                low = mid + 1
        
        return ans
```

**Explanation**

- Start with `low = 0`, `high = n - 1`, and `ans = n`.

- `ans = n` is the safe default. It covers the case where `target` is larger than every element, so nothing satisfies the condition and the value is inserted at the end.

- Each step looks at the middle element:
  - If `nums[mid] >= target`, then `mid` is a valid candidate for the insert position. Record it in `ans`, then move `high` to `mid - 1` to search for an even earlier index that still works.
  - If `nums[mid] < target`, then `mid` and everything to its left is too small. Move `low` to `mid + 1`.

- The loop ends when `low > high`. At that point `ans` holds the smallest index with a value greater than or equal to `target`, which is exactly the insert position.

**Complexity**

- Time: O(log n), the search space halves on every iteration.
- Space: O(1), only a few pointer variables are used.

**Dry Run**

Example 2 (target found via boundary, inserted in the middle):

```
nums = [1, 3, 5, 6]   target = 2        Expected: 1

Initial state:  low = 0,  high = 3,  ans = 4  (default n)

Step 1
  State:   low = 0, high = 3, ans = 4
  mid    = (0 + 3) // 2 = 1
  nums[mid] = nums[1] = 3
  test:    nums[mid] >= target  ->  3 >= 2  ->  True
  update:  ans = mid = 1,  high = mid - 1 = 0
  State:   low = 0, high = 0, ans = 1

Step 2
  State:   low = 0, high = 0, ans = 1
  mid    = (0 + 0) // 2 = 0
  nums[mid] = nums[0] = 1
  test:    nums[mid] >= target  ->  1 >= 2  ->  False
  update:  low = mid + 1 = 1
  State:   low = 1, high = 0, ans = 1

Loop ends:  low (1) > high (0)
Return ans = 1
```

Example 3 (target larger than all elements, uses the default):

```
nums = [1, 3, 5, 6]   target = 7        Expected: 4

Initial state:  low = 0,  high = 3,  ans = 4  (default n)

Step 1
  State:   low = 0, high = 3, ans = 4
  mid    = (0 + 3) // 2 = 1
  nums[mid] = nums[1] = 3
  test:    nums[mid] >= target  ->  3 >= 7  ->  False
  update:  low = mid + 1 = 2
  State:   low = 2, high = 3, ans = 4

Step 2
  State:   low = 2, high = 3, ans = 4
  mid    = (2 + 3) // 2 = 2
  nums[mid] = nums[2] = 5
  test:    nums[mid] >= target  ->  5 >= 7  ->  False
  update:  low = mid + 1 = 3
  State:   low = 3, high = 3, ans = 4

Step 3
  State:   low = 3, high = 3, ans = 4
  mid    = (3 + 3) // 2 = 3
  nums[mid] = nums[3] = 6
  test:    nums[mid] >= target  ->  6 >= 7  ->  False
  update:  low = mid + 1 = 4
  State:   low = 4, high = 3, ans = 4

Loop ends:  low (4) > high (3)
Return ans = 4  (ans stays at default n)
```

<br><br>

## Related Problems

- Binary Search (LeetCode 704)
- First Bad Version (LeetCode 278)
- Find First and Last Position of Element in Sorted Array (LeetCode 34)
- Sqrt(x) (LeetCode 69)
- Find Smallest Letter Greater Than Target (LeetCode 744)

<br><br>

## Related Concepts

- Lower Bound
- Binary Search