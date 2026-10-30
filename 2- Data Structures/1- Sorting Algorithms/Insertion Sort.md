# Insertion Sort

`Capgemini`

## Problem Statement

Given an array of integers `arr`, sort it in **ascending order** using **Insertion Sort**.

## Examples

**Example 1:**  
Input: `arr = [5, 2, 4, 1]`  
Output: `[1, 2, 4, 5]`

**Example 2:**  
Input: `arr = [1, 2, 3, 4]`  
Output: `[1, 2, 3, 4]`

**Example 3:**  
Input: `arr = [7]`  
Output: `[7]`

## Constraints

- `1 <= arr.length <= 10^4`
- `-10^5 <= arr[i] <= 10^5`

<br><br>

## Approach

<mark>Take the next element and insert it into its correct spot in the already-sorted left part.</mark>

It works like sorting cards in your hand: pick up one card and slide it left until it fits.

- The first element on its own is already "sorted".
- For each element from index `1` onward:
  - Save it as `key`.
  - Shift every bigger element in the sorted part **one step right**.
  - Drop `key` into the gap that opens up.

<br><br>

## Code

```python
class Solution:
    def insertionSort(self, arr):
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1

            # Shift bigger elements one step right
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1

            # Place key in the gap
            arr[j + 1] = key

        return arr
```

<br><br>

## Dry Run

```ini
Input: arr = [5, 2, 4, 1]

i = 1  key = 2   sorted part = [5]
  5 > 2  shift  -> [5, 5, 4, 1]
  place 2 at index 0  -> [2, 5, 4, 1]

i = 2  key = 4   sorted part = [2, 5]
  5 > 4  shift  -> [2, 5, 5, 1]
  2 < 4  stop
  place 4 at index 1  -> [2, 4, 5, 1]

i = 3  key = 1   sorted part = [2, 4, 5]
  5 > 1  shift  -> [2, 4, 5, 5]
  4 > 1  shift  -> [2, 4, 4, 5]
  2 > 1  shift  -> [2, 2, 4, 5]
  place 1 at index 0  -> [1, 2, 4, 5]

Final Answer: [1, 2, 4, 5]
```

<br><br>

## Complexity

- **Best Case:** `O(n)`, when the array is already sorted (the inner loop never runs).
- **Average / Worst Case:** `O(n^2)`, worst when the array is in reverse order.
- **Space Complexity:** `O(1)`, sorts in place.
- **Stable:** Yes. It only shifts elements that are strictly bigger.

<br><br>

## When to Use It

- **Small arrays:** low overhead makes it faster than merge or quick sort for a few elements.
- **Nearly sorted data:** runs close to `O(n)`.
- Python's built-in sort (Timsort) uses insertion sort on small chunks for this reason.

<br><br>

## Related Problems

- [Insertion Sort List (147)](https://leetcode.com/problems/insertion-sort-list/)
- [Sort an Array (912)](https://leetcode.com/problems/sort-an-array/)
- [Merge Sorted Array (88)](https://leetcode.com/problems/merge-sorted-array/)
