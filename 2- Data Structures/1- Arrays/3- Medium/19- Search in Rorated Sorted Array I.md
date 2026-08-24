# Search in Rotated Sorted Array I

`Google` • `Amazon` • `Meta` • `Microsoft` • `Bloomberg` • `Goldman Sachs` • `LinkedIn` • `ByteDance`

## Problem Statement

There is an integer array `nums` sorted in ascending order (with distinct values).

Prior to being passed to your function, `nums` is possibly left rotated at an unknown index `k` (`1 <= k < nums.length`) such that the resulting array is `[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]` (0-indexed). For example, `[0,1,2,4,5,6,7]` might be left rotated by 3 indices and become `[4,5,6,7,0,1,2]`.

Given the array `nums` after the possible rotation and an integer `target`, return the index of `target` if it is in `nums`, or `-1` if it is not in `nums`.

You must write an algorithm with `O(log n)` runtime complexity.

## Examples

**Example 1:**
```
Input: nums = [4,5,6,7,0,1,2], target = 0
Output: 4
```

**Example 2:**
```
Input: nums = [4,5,6,7,0,1,2], target = 3
Output: -1
```

**Example 3:**
```
Input: nums = [1], target = 0
Output: -1
```

## Constraints

- `1 <= nums.length <= 5000`
- `-10^4 <= nums[i] <= 10^4`
- All values of `nums` are unique.
- `nums` is an ascending array that is possibly rotated.
- `-10^4 <= target <= 10^4`

<br><br>

## Approach 1: Linear Search

The simplest idea: check every number until you find the target.

- Look at each element one by one.
- If an element equals the target, return its index.
- If you reach the end and find nothing, return `-1`.

This works, but it ignores the sorted order, so it is slow and does not meet the `O(log n)` requirement.

**Time Complexity:** `O(n)`
**Space Complexity:** `O(1)`

```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        # Walk through each index one by one
        for i in range(len(nums)):
            # Return the index as soon as we hit the target
            if nums[i] == target:
                return i
        # Target was never found in the array
        return -1
```

<br><br>

## Approach 2: Modified Binary Search

Even after rotation, one half of the array is always sorted. We use that fact to throw away half of the array on every step.

- Look at the middle element.
- If it is the target, we are done.
- Decide which half is sorted (left or right).
- Check if the target fits inside that sorted half's range:
  - If yes, keep searching that half.
  - If no, search the other half.
- Repeat until the target is found or the range is empty.

Because we cut the search space in half each time, it runs in `O(log n)`.

**Time Complexity:** `O(log n)`
**Space Complexity:** `O(1)`

```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        low = 0
        high = len(nums) - 1

        while low <= high:
            mid = (low + high) // 2

            # Target found at the middle
            if nums[mid] == target:
                return mid

            # Left half [low..mid] is sorted
            if nums[low] <= nums[mid]:
                # Target lies within the sorted left half, so search left
                if nums[low] <= target and target <= nums[mid]:
                    high = mid - 1
                # Otherwise the target must be in the right half
                else:
                    low = mid + 1

            # Right half [mid..high] is sorted
            else:
                # Target lies within the sorted right half, so search right
                if nums[mid] <= target and target <= nums[high]:
                    low = mid + 1
                # Otherwise the target must be in the left half
                else:
                    high = mid - 1

        # Target was not present in the array
        return -1
```

<br><br>

## Dry Run

Input: `nums = [4, 5, 6, 7, 0, 1, 2]`, `target = 0`

```
Start
low  = 0
high = 6

Step 1
mid = 3
nums[3] = 7
Left half is sorted
0 is not between 4 and 7
Go right: low = 4

Step 2
mid = 5
nums[5] = 1
Left half is sorted
0 is between 0 and 1
Go left: high = 4

Step 3
mid = 4
nums[4] = 0
Match found
Return 4
```

Output: `4`

<br><br>

## Related Problems

- [Search in Rotated Sorted Array II (LeetCode 81)](https://leetcode.com/problems/search-in-rotated-sorted-array-ii/)
- [Find Minimum in Rotated Sorted Array (LeetCode 153)](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)
- [Find Minimum in Rotated Sorted Array II (LeetCode 154)](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/)
- [Binary Search (LeetCode 704)](https://leetcode.com/problems/binary-search/)
- [Find Peak Element (LeetCode 162)](https://leetcode.com/problems/find-peak-element/)