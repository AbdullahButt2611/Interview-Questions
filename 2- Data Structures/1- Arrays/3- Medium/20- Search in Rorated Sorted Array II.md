# Search in Rotated Sorted Array II

`Microsoft` • `Amazon` • `Adobe`

## Problem Statement

You are given an integer array `nums` that was originally sorted in ascending order and may contain duplicate values. The array has then been rotated at some unknown pivot point. You are also given a target value `k`.

Return `True` if `k` exists in the array, otherwise return `False`.

## Examples

**Example 1**

- Input: `nums = [7, 8, 1, 2, 3, 3, 3, 4, 5, 6]`, `k = 3`
- Output: `True`
- Explanation: The element `3` is present in the array, so the answer is `True`.

**Example 2**

- Input: `nums = [7, 8, 1, 2, 3, 3, 3, 4, 5, 6]`, `k = 10`
- Output: `False`
- Explanation: The element `10` is not present in the array, so the answer is `False`.

## Constraints

- `1 <= nums.length <= 10^4`
- `-10^4 <= nums[i] <= 10^4`
- `nums` is guaranteed to be rotated at some pivot.
- `-10^4 <= k <= 10^4`

<br><br>

## Understanding the Problem

A rotated sorted array is just a sorted array that was cut at one point, with the front piece moved to the back.

Take the sorted array `[1, 2, 3, 3, 3, 4, 5, 6, 7, 8]`. If we move `7` and `8` to the front, we get the array from Example 1:

```INI
[7, 8, 1, 2, 3, 3, 3, 4, 5, 6]
```

Notice that the array now falls into two sorted runs joined together:

- `[7, 8]`  (the piece that was moved)
- `[1, 2, 3, 3, 3, 4, 5, 6]`  (the rest)

The only place where the order "breaks" is between `8` and `1`. Everywhere else, numbers keep climbing.

The naive way to solve this is to scan every element, which is `O(n)`. Our goal is to be faster by adapting binary search.

<br><br>

## The Core Idea

When we run binary search, we pick a middle index `mid` and split the array into a left part and a right part.

<mark>Even though the full array is not sorted, at least one of the two halves (left of mid or right of mid) is always fully sorted.</mark>

This gives us a simple plan for every step:

1. **Find which half is sorted.**
   - If `nums[low] <= nums[mid]`, the left half is sorted.
   - Otherwise, the right half is sorted.
2. **Use the sorted half's range to decide where to go.**
   - A sorted half has a clear smallest and largest value, so we can check if the target fits inside that range.
   - If the target is inside the sorted half, search there. If not, search the other half.

Because each step removes half of the remaining elements, this runs in `O(log n)` when the values are distinct.

<br><br>

## Where Duplicates Break the Idea

Everything above works cleanly only when values are distinct. Duplicates ruin step 1, because the check `nums[low] <= nums[mid]` can no longer tell us which half is truly sorted.

The trouble shows up when `nums[low]`, `nums[mid]`, and `nums[high]` are all the same value. Watch the simple approach fail on this input:

```INI
nums = [3, 1, 2, 3, 3, 3, 3]   (indexes 0..6)
target = 1

Step 1:  low=0  high=6  mid=3
         nums[low]=3 <= nums[mid]=3
         The simple rule concludes "left half is sorted".
         But [3, 1, 2, 3] is NOT actually sorted, so this conclusion is wrong.
         Is target 1 inside the range [3 .. 3]?  No
         => low = 4   (this throws away indexes 0..3, where 1 was hiding)

Step 2:  low=4  high=6  mid=5
         nums[low]=3 <= nums[mid]=3  ->  "left half sorted" again
         Is target 1 inside [3 .. 3]?  No
         => low = 6

Step 3:  low=6  high=6  mid=6
         Is target 1 inside range?  No
         => low = 7

End:     low=7 > high=6  ->  returns False
         This is WRONG. The value 1 was sitting at index 1 the whole time.
```

The equal values at the two ends fooled the algorithm into deleting the exact half that held the answer.

<br><br>

## The Fix and Full Solution

The fix is one extra check placed at the top of the loop. When `nums[low]`, `nums[mid]`, and `nums[high]` are all equal, we admit that we cannot tell which side is sorted, so we simply trim one element from each end and try again:

```python
if nums[low] == nums[mid] and nums[mid] == nums[high]:
    low = low + 1
    high = high - 1
    continue
```

This is safe because the values we trim are copies of `nums[mid]`, and we already know `nums[mid]` is not the target at that point, so dropping them costs us nothing.

Here is the complete solution with that guard in place:

```python
class Solution:
    def search(self, nums: List[int], target: int) -> bool:
        low = 0
        high = len(nums) - 1

        while low <= high:
            mid = (low + high) // 2
            if nums[mid] == target: return True

            if nums[low] == nums[mid] and nums[mid] == nums[high]: 
                low = low + 1
                high = high - 1
                continue
            
            if nums[low] <= nums[mid]:
                if nums[low] <= target and target <= nums[mid]:
                    high = mid - 1
                else:
                    low = mid + 1
            else:
                if nums[mid] <= target and target <= nums[high]:
                    low = mid + 1
                else:
                    high = mid - 1
        
        return False
```

<br><br>

## Dry Run

Let us run the full solution on the same input that broke the simple version. Watch how the new guard saves it.

```INI
nums = [3, 1, 2, 3, 3, 3, 3]   (indexes 0..6)
target = 1

Step 1:  low=0  high=6  mid=3
         window = [3, 1, 2, 3, 3, 3, 3]
         nums[mid]=3, which is not the target.
         nums[low]=3, nums[mid]=3, nums[high]=3  ->  all three are equal.
         We cannot tell which half is sorted, so trim both ends.
         => low = 1, high = 5

Step 2:  low=1  high=5  mid=3
         window = [1, 2, 3, 3, 3]   (indexes 1..5)
         nums[mid]=3, which is not the target.
         nums[low]=1 <= nums[mid]=3  ->  the LEFT half is sorted.
         Is target 1 inside the range [1 .. 3]?  Yes
         So the answer must be in the left half.
         => high = 2

Step 3:  low=1  high=2  mid=1
         window = [1, 2]   (indexes 1..2)
         nums[mid]=1 == target=1  ->  FOUND
         => return True
```

The guard removed the confusing duplicates first, and after that ordinary binary search took over and landed on the answer.

<br><br>

## Time Complexity

| Case | Time | Why |
| :-- | :-- | :-- |
| Best | O(1) | The target happens to be at the first `mid` we check |
| Average | O(log n) | Each step removes half of the remaining elements, exactly like standard binary search |
| Worst | O(n), about n/2 | When `low`, `mid`, and `high` are all equal (for example an array like `[3, 3, 3, 3, 3]`), we can only trim one element from each end per step instead of halving. Removing two per step from n elements takes roughly n/2 steps, which is O(n) |

<br><br>

## Related Problems

- [Search in Rotated Sorted Array (LeetCode 33)](https://leetcode.com/problems/search-in-rotated-sorted-array/)
- [Find Minimum in Rotated Sorted Array (LeetCode 153)](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)
- [Find Minimum in Rotated Sorted Array II (LeetCode 154)](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/)
- [Binary Search (LeetCode 704)](https://leetcode.com/problems/binary-search/)
- [Find Peak Element (LeetCode 162)](https://leetcode.com/problems/find-peak-element/)