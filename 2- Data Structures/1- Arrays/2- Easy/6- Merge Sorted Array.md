# 88. Merge Sorted Array

`Meta` • `Amazon` • `Microsoft`

<br>

## Problem Statement

You are given two integer arrays `nums1` and `nums2`, sorted in non-decreasing order, and two integers `m` and `n`, representing the number of elements in `nums1` and `nums2` respectively.

- Merge `nums1` and `nums2` into a single array sorted in non-decreasing order.
- The result must be stored **inside** `nums1`, not returned.
- `nums1` has a length of `m + n`. The first `m` elements are valid; the last `n` are `0` placeholders to be ignored.

## Examples

**Example 1:**
```
Input:  nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3
Output: [1,2,2,3,5,6]
```

**Example 2:**
```
Input:  nums1 = [1], m = 1, nums2 = [], n = 0
Output: [1]
```

**Example 3:**
```
Input:  nums1 = [0], m = 0, nums2 = [1], n = 1
Output: [1]
```

## Constraints

- `nums1.length == m + n`
- `nums2.length == n`
- `0 <= m, n <= 200`
- `1 <= m + n <= 200`
- `-10^9 <= nums1[i], nums2[j] <= 10^9`

<br><br>

## Approach 1: Naive Merge and Sort

### Intuition

Copy all elements of `nums2` into the empty tail slots of `nums1`, then sort the whole array.

### Solution

```python
from typing import List

class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        # Copy nums2 elements into the empty tail of nums1
        for k in range(n):
            nums1[m + k] = nums2[k]

        # Sort the full array in-place
        nums1.sort()
```

### Explanation

- Fill positions `m` through `m + n - 1` in `nums1` with values from `nums2`.
- Call `.sort()` on the full array. Python's built-in Timsort handles the rest.

### Complexity

| | Complexity |
|---|---|
| **Time** | O((m + n) log(m + n)) |
| **Space** | O(1) |

### Problem with this Approach

Both input arrays are **already sorted**. Sorting from scratch discards that structure entirely and adds an unnecessary log factor. The optimal solution should exploit the pre-sorted property.

<br><br>

## Approach 2: In-Place Two-Pointer from the Back (Optimal)

### Intuition

Merging from the front is dangerous: writing into `nums1` early would overwrite values that have not been read yet. The fix is to **merge from the back**.

The tail of `nums1` (positions `m` to `m + n - 1`) is guaranteed free space. At every step, the largest unplaced element goes into the rightmost free slot. Since we write to the right and read from the left, we can never overwrite an unread value.

### Pointers

| Pointer | Starts at | Role |
|---|---|---|
| `p1` | `m - 1` | Last valid element in `nums1` |
| `p2` | `n - 1` | Last element in `nums2` |
| `idx` | `m + n - 1` | Next write position (rightmost free slot) |

### Solution

```python
from typing import List

class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        p1  = m - 1        # pointer to last valid element in nums1
        p2  = n - 1        # pointer to last element in nums2
        idx = m + n - 1    # pointer to last position in merged array

        # Place the larger of the two current elements at idx, moving backwards
        while p1 >= 0 and p2 >= 0:
            if nums1[p1] >= nums2[p2]:
                nums1[idx] = nums1[p1]
                p1 -= 1
            else:
                nums1[idx] = nums2[p2]
                p2 -= 1
            idx -= 1

        # If p1 elements remain, they are already in place — nothing to do.

        # If p2 elements remain, copy them into the front of nums1
        while p2 >= 0:
            nums1[idx] = nums2[p2]
            p2  -= 1
            idx -= 1
```

### Explanation

**Why no cleanup loop for remaining `nums1` elements?**
If `p2` exhausts first, the leftover elements in `nums1` are already in their correct positions. Nothing needs to move.

**Why do we need a cleanup loop for remaining `nums2` elements?**
If `p1` exhausts first, the remaining `nums2` values are all smaller than everything placed so far. They must be copied into the front of `nums1`.

### Dry Run (Example 1)

```
nums1 = [1, 2, 3, 0, 0, 0]   m = 3
nums2 = [2, 5, 6]             n = 3

Initial : p1=2 (val=3), p2=2 (val=6), idx=5

Step 1  : 6 > 3  -> nums1[5] = 6,  p2=1, idx=4  -> [1,2,3,0,0,6]
Step 2  : 5 > 3  -> nums1[4] = 5,  p2=0, idx=3  -> [1,2,3,0,5,6]
Step 3  : 3 > 2  -> nums1[3] = 3,  p1=1, idx=2  -> [1,2,3,3,5,6]
Step 4  : 2 >= 2 -> nums1[2] = 2,  p1=0, idx=1  -> [1,2,2,3,5,6]
Step 5  : 2 >= 2 -> nums1[1] = 2,  p2=-1         -> [1,2,2,3,5,6]

Loop ends. Final: [1,2,2,3,5,6]
```

### Complexity

| | Complexity |
|---|---|
| **Time** | O(m + n) |
| **Space** | O(1) |

Each element is processed exactly once. No extra memory is used beyond the three pointers.

<br><br>

## Summary

| Approach | Time | Space | Notes |
|---|---|---|---|
| Naive Merge + Sort | O((m+n) log(m+n)) | O(1) | Ignores sorted property |
| In-Place Two-Pointer (Back) | O(m + n) | O(1) | Optimal |

<br><br>

## Related Problems

- [21. Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) - Same merging logic applied to linked lists instead of arrays.
- [23. Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) - Generalizes the two-list merge to k lists using a min-heap.
- [977. Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/) - Uses a two-pointer-from-back strategy on a sorted array with negatives.
- [1768. Merge Strings Alternately](https://leetcode.com/problems/merge-strings-alternately/) - Merging two sequences with a pointer per sequence.