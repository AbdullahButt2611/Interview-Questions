# Left Rotate Array by K Places

`Tekion Corp` • `Credex Technology` • `Amazon` • `Bloomberg` • `Cognizant`

## Problem Statement

Given an integer array `nums` and a non-negative integer `k`, rotate the array to the **left** by `k` steps **in-place**.

## Examples

**Example 1**
```
Input:  nums = [1, 2, 3, 4, 5, 6], k = 2
Output: nums = [3, 4, 5, 6, 1, 2]
```
```
Rotate 1 step  -> [2, 3, 4, 5, 6, 1]
Rotate 2 steps -> [3, 4, 5, 6, 1, 2]
```

**Example 2**
```
Input:  nums = [3, 4, 1, 5, 3, -5], k = 8
Output: nums = [1, 5, 3, -5, 3, 4]
```
```
k = 8, len = 6 -> effective rotation = 8 % 6 = 2
Rotate 1 step  -> [4, 1, 5, 3, -5, 3]
Rotate 2 steps -> [1, 5, 3, -5, 3, 4]
```

## Constraints

- `1 <= nums.length <= 10^5`
- `-10^4 <= nums[i] <= 10^4`
- `0 <= k`

## Approach 1: Brute Force (One Step at a Time)

### Intuition

Simulate the rotation literally: perform exactly `k` single-step left rotations. In each step, save the first element, shift every element one position to the left, and place the saved element at the end.

### Solution

```python
class Solution:
    def rotateArray(self, nums: list[int], k: int) -> None:
        n = len(nums)
        k = k % n  # handle k >= n
        for _ in range(k):
            first = nums[0]
            for i in range(n - 1):
                nums[i] = nums[i + 1]
            nums[n - 1] = first
```

### Complexity

| | |
|---|---|
| **Time** | O(n x k) — each of the k rotations touches every element |
| **Space** | O(1) — in-place, no extra array |

### Problem with this Approach

When `k` is large (e.g., `k ≈ n`), the nested loop runs O(n²) operations. For `n = 10^5` this is **10 billion** operations, which is far too slow. We need to rotate in a single pass.

## Approach 2: Extra Array (Slice and Concatenate)

### Intuition

After a left rotation by `k`, the element at index `k` moves to index `0`. In other words, the final array is simply `nums[k:]` followed by `nums[:k]`. We can build this in one line using slicing.

### Solution

```python
class Solution:
    def rotateArray(self, nums: list[int], k: int) -> None:
        n = len(nums)
        k = k % n
        rotated = nums[k:] + nums[:k]
        nums[:] = rotated   # write back in-place
```

### Complexity

| | |
|---|---|
| **Time** | O(n) — single pass to build the new array and copy back |
| **Space** | O(n) — a full extra copy of the array |

### Problem with this Approach

This is already O(n) time, which is optimal. The only cost is **O(n) extra space** for the temporary array. If the problem requires a true in-place solution (e.g., embedded systems or very large arrays), we need to do better on space.

## Approach 3: Reversal Algorithm (Optimal) ✅

### Intuition

Observe what a left rotation by `k` does to the two natural segments of the array:

```
Original : [ A | B ]   where A = nums[0..k-1], B = nums[k..n-1]
Rotated  : [ B | A ]
```

We need to swap the two halves **without** an extra array. The key insight is that **reversing** a segment is an O(n) in-place operation. Three reversals achieve the swap:

```
Step 1 - Reverse A:        [ A' | B  ]
Step 2 - Reverse B:        [ A' | B' ]
Step 3 - Reverse all:      [ B  | A  ]   ✓
```

Why does this work? Reversing both halves individually scrambles them; reversing the whole array un-scrambles them in the correct (swapped) order.

### Walkthrough (Example 1)

```
nums = [1, 2, 3, 4, 5, 6],  k = 2

Step 1 - reverse nums[0..1]:   [2, 1, 3, 4, 5, 6]
Step 2 - reverse nums[2..5]:   [2, 1, 6, 5, 4, 3]
Step 3 - reverse nums[0..5]:   [3, 4, 5, 6, 1, 2]  ✓
```

### Solution

```python
class Solution:
    def reverse(self, arr: list[int], start: int, end: int) -> None:
        while start < end:
            arr[start], arr[end] = arr[end], arr[start]
            start += 1
            end -= 1

    def rotateArray(self, nums: list[int], k: int) -> None:
        n = len(nums)
        k = k % n           # handle k >= n (e.g., Example 2: 8 % 6 = 2)
        if k == 0:
            return          # no rotation needed

        self.reverse(nums, 0, k - 1)        # reverse first k elements
        self.reverse(nums, k, n - 1)        # reverse remaining elements
        self.reverse(nums, 0, n - 1)        # reverse entire array
```

### Complexity

| | |
|---|---|
| **Time** | O(n) — each element is touched at most twice across the three reversals |
| **Space** | O(1) — purely in-place, only swap variables used |

## Comparison of All Approaches

| Approach | Time | Space | In-Place |
|---|---|---|---|
| Brute Force | O(n x k) | O(1) | ✅ |
| Extra Array (Slice) | O(n) | O(n) | ❌ |
| **Reversal Algorithm** | **O(n)** | **O(1)** | **✅** |

## Key Takeaways

- **Always reduce `k`**: `k = k % n` handles cases where `k >= n` and avoids unnecessary rotations (Example 2).
- **The reversal trick** is a classic pattern applicable to both left and right rotations, worth memorising.
- **Right rotation by `k`** is equivalent to left rotation by `n - k`; the same three-reversal approach applies.