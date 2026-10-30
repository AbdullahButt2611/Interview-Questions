# Bubble Sort

`Capgemini`

## Problem Statement

Given an array of integers `arr`, sort it in **ascending order** using **Bubble Sort**.

## Examples

**Example 1:**  
Input: `arr = [5, 1, 4, 2, 8]`  
Output: `[1, 2, 4, 5, 8]`

**Example 2:**  
Input: `arr = [1, 2, 3]`  
Output: `[1, 2, 3]`

**Example 3:**  
Input: `arr = [7]`  
Output: `[7]`

## Constraints

- `1 <= arr.length <= 10^4`
- `-10^5 <= arr[i] <= 10^5`

<br><br>

## Approach

<mark>Compare each pair of neighbours. If the left one is bigger, swap them.</mark>

- After the first pass, the **largest** element has moved ("bubbled") to the end.
- After the second pass, the second largest is in place, and so on.
- So each pass can stop one position earlier than the last.
- If a full pass makes **no swaps**, the array is already sorted, so stop early.

<br><br>

## Code

```python
class Solution:
    def bubbleSort(self, arr):
        n = len(arr)

        for i in range(n - 1):
            swapped = False

            # The last i elements are already in place
            for j in range(n - 1 - i):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True

            # No swaps means the array is sorted
            if not swapped:
                break

        return arr
```

<br><br>

## Dry Run

```ini
Input: arr = [5, 1, 4, 2, 8]

Pass 1 (i = 0)
  5 > 1  swap  -> [1, 5, 4, 2, 8]
  5 > 4  swap  -> [1, 4, 5, 2, 8]
  5 > 2  swap  -> [1, 4, 2, 5, 8]
  5 < 8  no swap
  8 is now in its final place

Pass 2 (i = 1)
  1 < 4  no swap
  4 > 2  swap  -> [1, 2, 4, 5, 8]
  4 < 5  no swap

Pass 3 (i = 2)
  1 < 2  no swap
  2 < 4  no swap
  No swaps in this pass, so stop

Final Answer: [1, 2, 4, 5, 8]
```

<br><br>

## Complexity

- **Best Case:** `O(n)`, when the array is already sorted (one pass, no swaps).
- **Average / Worst Case:** `O(n^2)`, worst when the array is in reverse order.
- **Space Complexity:** `O(1)`, sorts in place.
- **Stable:** Yes. Equal elements are never swapped, so they keep their order.

<br><br>

## Related Problems

- [Sort an Array (912)](https://leetcode.com/problems/sort-an-array/)
- [Sort Colors (75)](https://leetcode.com/problems/sort-colors/)
- [Move Zeroes (283)](https://leetcode.com/problems/move-zeroes/)
