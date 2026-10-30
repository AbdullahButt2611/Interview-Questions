# Floor and Ceil in Sorted Array

`Amazon` • `Google` • `Microsoft` • `Meta`

<br>

## Problem Statement
Given a sorted array `nums` and an integer `x`, find the floor and ceil of `x` in `nums`.

The floor of `x` is the largest element in the array which is smaller than or equal to `x`. The ceil of `x` is the smallest element in the array which is greater than or equal to `x`. If no floor or ceil exists, output `-1`.

## Examples
**Example 1**
Input: `nums = [3, 4, 4, 7, 8, 10]`, `x = 5`
Output: `4 7`
Explanation: The floor of 5 in the array is 4, and the ceil of 5 in the array is 7.

**Example 2**
Input: `nums = [3, 4, 4, 7, 8, 10]`, `x = 8`
Output: `8 8`
Explanation: The floor of 8 in the array is 8, and the ceil of 8 in the array is also 8.

## Constraints
- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^6`
- `1 <= x <= 10^6`
- The array is sorted in non-decreasing order.

<br><br>

## Solution
```python
class Solution:
    def getCeil(self, nums, x):
        ans = -1                       # default answer if no ceil exists
        n = len(nums)
        low = 0
        high = n - 1

        while low <= high:
            mid = (low + high) // 2    # middle index of the current search space
            if nums[mid] >= x:
                ans = nums[mid]        # valid candidate for ceil, store it
                high = mid - 1         # look left for a smaller valid value
            else:
                low = mid + 1          # too small, search the right half

        return ans

    def getFloor(self, nums, x):
        ans = -1                       # default answer if no floor exists
        n = len(nums)
        low = 0
        high = n - 1

        while low <= high:
            mid = (low + high) // 2    # middle index of the current search space
            if nums[mid] <= x:
                ans = nums[mid]        # valid candidate for floor, store it
                low = mid + 1          # look right for a larger valid value
            else:
                high = mid - 1         # too big, search the left half

        return ans

    def getFloorAndCeil(self, nums, x):
        ceil = self.getCeil(nums, x)    # smallest element >= x
        floor = self.getFloor(nums, x)  # largest element <= x
        return [floor, ceil]
```

<br><br>

## Related Problems
- Search Insert Position
- First and Last Position of Element in a Sorted Array
- Ceiling in a Sorted Array
- Floor in a Sorted Array
- Find Smallest Letter Greater Than Target
- Search in Rotated Sorted Array