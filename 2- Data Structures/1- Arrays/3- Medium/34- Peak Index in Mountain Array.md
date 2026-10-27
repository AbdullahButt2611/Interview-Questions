# Peak Index in a Mountain Array

`Meta` • `Apple` • `Uber` • `SoFi`

## Problem Statement

You are given an integer **mountain array** `arr` of length `n`. The values go **up** until they reach a peak, and then they go **down**.

- Return the **index** of the peak element.
- You must solve it in <mark>O(log n)</mark> time.

## Examples

**Example 1:**

```ini
Input:  arr = [0, 1, 0]
Output: 1
Explanation: arr[1] = 1 is bigger than both its neighbors.
```

**Example 2:**

```ini
Input:  arr = [0, 2, 1, 0]
Output: 1
Explanation: arr[1] = 2 is the highest point of the mountain.
```

**Example 3:**

```ini
Input:  arr = [0, 10, 5, 2]
Output: 1
Explanation: arr[1] = 10 is the highest point of the mountain.
```

## Constraints

- `3 <= arr.length <= 10^5`
- `0 <= arr[i] <= 10^6`
- `arr` is guaranteed to be a mountain array.

<br><br>

## Approach

### Picture It as a Hiking Trail

Imagine the array is a trail over a mountain. You drop onto some spot and look at the steps next to you.

- **Step behind you is lower?** You are climbing up. The top is still ahead, on the **right**.
- **Step behind you is higher?** You are walking down. You already passed the top. It is on the **left**.
- **Both neighbors are lower?** You are standing on the top. Done.

<mark>Going up? Move right. Going down? Move left. Both sides lower? That's the peak.</mark>

### Why Binary Search Fits

- Every time we look at the middle spot, we learn which side holds the peak.
- So we can throw away the other half without ever checking it.
- Cutting the array in half again and again gives `O(log n)` time.

### Why We Start at `1` and `n - 2`

- The first and last elements can never be the peak. A mountain has to go up first and come down after.
- Keeping `mid` inside this range also means `arr[mid - 1]` and `arr[mid + 1]` always exist. No index errors.

### The Steps

1. Set `left = 1` and `right = n - 2`.
2. While `left < right`:
   - Find the middle: `mid = (left + right) // 2`.
   - If `arr[mid]` is bigger than **both** neighbors, return `mid`.
   - Else if `arr[mid] > arr[mid - 1]`, we are going uphill. Move right with `left = mid + 1`.
   - Otherwise we are going downhill. Move left with `right = mid - 1`.
3. When the loop stops, `left` and `right` point to the same spot. Return `left`.

### Why Returning `left` at the End Is Safe

- We only skip `mid` once we know for sure it isn't the peak.
- So the peak always stays somewhere between `left` and `right`.
- When the two pointers meet, only one spot remains, and it must be the peak.

<br><br>

## Code

```python
class Solution:
  def peakIndexInMountainArray(self, arr: list[int]) -> int:
    left = 1
    right = len(arr) - 2

    while left < right:
      mid = (left + right) // 2

      if arr[mid] > arr[mid - 1] and arr[mid] > arr[mid + 1]:
        return mid
      elif arr[mid] > arr[mid - 1]:
        left = mid + 1
      else:
        right = mid - 1

    return left
```

<br><br>

## Dry Run

```ini
==================== EXAMPLE A ====================

index :  0   1   2   3   4   5   6   7   8   9   10  11
arr   :  0   2   4   9   7   6   5   4   3   2   1   0

Expected peak: index 3 (value 9)

Starting values:
left  = 1
right = len(arr) - 2 = 12 - 2 = 10


Iteration 1
Loop check     : left (1) < right (10)  ->  True, keep going
mid            : (1 + 10) // 2 = 11 // 2 = 5
arr[mid]       : arr[5] = 6
Left neighbor  : arr[4] = 7
Right neighbor : arr[6] = 5

Is 6 > 7 AND 6 > 5 ?   No (6 is smaller than 7)
Is 6 > 7 ?             No
-> We are walking DOWNHILL. The peak is behind us (on the left).
-> right = mid - 1 = 5 - 1 = 4

Now searching index 1 to 4  ->  [2, 4, 9, 7]


Iteration 2
Loop check     : left (1) < right (4)  ->  True, keep going
mid            : (1 + 4) // 2 = 5 // 2 = 2
arr[mid]       : arr[2] = 4
Left neighbor  : arr[1] = 2
Right neighbor : arr[3] = 9

Is 4 > 2 AND 4 > 9 ?   No (4 is smaller than 9)
Is 4 > 2 ?             Yes
-> We are climbing UPHILL. The peak is ahead of us (on the right).
-> left = mid + 1 = 2 + 1 = 3

Now searching index 3 to 4  ->  [9, 7]


Iteration 3
Loop check     : left (3) < right (4)  ->  True, keep going
mid            : (3 + 4) // 2 = 7 // 2 = 3
arr[mid]       : arr[3] = 9
Left neighbor  : arr[2] = 4
Right neighbor : arr[4] = 7

Is 9 > 4 AND 9 > 7 ?   Yes
-> Both neighbors are lower. We are on the TOP.
-> return mid = 3


Final Answer: 3


==================== EXAMPLE B ====================

index :  0   1   2   3   4
arr   :  0   1   2   3   2

Expected peak: index 3 (value 3)

Starting values:
left  = 1
right = len(arr) - 2 = 5 - 2 = 3


Iteration 1
Loop check     : left (1) < right (3)  ->  True, keep going
mid            : (1 + 3) // 2 = 4 // 2 = 2
arr[mid]       : arr[2] = 2
Left neighbor  : arr[1] = 1
Right neighbor : arr[3] = 3

Is 2 > 1 AND 2 > 3 ?   No (2 is smaller than 3)
Is 2 > 1 ?             Yes
-> We are climbing UPHILL. The peak is ahead of us (on the right).
-> left = mid + 1 = 2 + 1 = 3

Now searching index 3 to 3  ->  [3]


Iteration 2
Loop check     : left (3) < right (3)  ->  False, loop stops

Only one spot is left, so it has to be the peak.
-> return left = 3


Final Answer: 3
```

<br><br>

## Complexity Analysis

- **Time Complexity:** `O(log n)`
  - Each loop cuts the search space in half.
- **Space Complexity:** `O(1)`
  - We only use three variables: `left`, `right`, and `mid`.

<br><br>

## Related Problems

- [Find Peak Element (162)](https://leetcode.com/problems/find-peak-element/)
- [Find in Mountain Array (1095)](https://leetcode.com/problems/find-in-mountain-array/)
- [Valid Mountain Array (941)](https://leetcode.com/problems/valid-mountain-array/)
- [Longest Mountain in Array (845)](https://leetcode.com/problems/longest-mountain-in-array/)
- [Minimum Number of Removals to Make Mountain Array (1671)](https://leetcode.com/problems/minimum-number-of-removals-to-make-mountain-array/)
- [Find a Peak Element II (1901)](https://leetcode.com/problems/find-a-peak-element-ii/)
