# Selection Sort

`Capgemini`

## Problem Statement

Given an array of integers `arr`, sort it in **ascending order** using **Selection Sort**.

## Examples

**Example 1:**  
Input: `arr = [64, 25, 12, 22, 11]`  
Output: `[11, 12, 22, 25, 64]`

**Example 2:**  
Input: `arr = [3, 1, 2]`  
Output: `[1, 2, 3]`

**Example 3:**  
Input: `arr = [7]`  
Output: `[7]`

## Constraints

- `1 <= arr.length <= 10^4`
- `-10^5 <= arr[i] <= 10^5`

<br><br>

## Approach

<mark>Find the smallest element in the unsorted part and swap it to the front of that part.</mark>

- Split the array into two parts: **sorted** (left) and **unsorted** (right).
- At the start, the sorted part is empty.
- On each pass:
  - Scan the unsorted part and find the index of the **minimum**.
  - Swap it with the first element of the unsorted part.
  - The sorted part grows by one.
- Stop when only one element is left. It's already in place.

<br><br>

## Code

```python
class Solution:
    def selectionSort(self, arr):
        n = len(arr)

        for i in range(n - 1):
            min_index = i

            # Find the smallest element in arr[i..n-1]
            for j in range(i + 1, n):
                if arr[j] < arr[min_index]:
                    min_index = j

            # Move it to the front of the unsorted part
            if min_index != i:
                arr[i], arr[min_index] = arr[min_index], arr[i]

        return arr
```

<br><br>

## Dry Run

```ini
Input: arr = [64, 25, 12, 22, 11]

i = 0  unsorted = [64, 25, 12, 22, 11]
  min = 11 at index 4
  swap arr[0] and arr[4]  -> [11, 25, 12, 22, 64]

i = 1  unsorted = [25, 12, 22, 64]
  min = 12 at index 2
  swap arr[1] and arr[2]  -> [11, 12, 25, 22, 64]

i = 2  unsorted = [25, 22, 64]
  min = 22 at index 3
  swap arr[2] and arr[3]  -> [11, 12, 22, 25, 64]

i = 3  unsorted = [25, 64]
  min = 25 at index 3
  already in place, no swap

Final Answer: [11, 12, 22, 25, 64]
```

<br><br>

## Complexity

- **Time Complexity:** `O(n^2)` in **every** case. It always scans the whole unsorted part, even if the array is already sorted.
- **Space Complexity:** `O(1)`, sorts in place.
- **Stable:** No. A long-distance swap can jump an element over an equal one.
- **Swaps:** At most `n - 1`. This is useful when writing to memory is expensive.

<br><br>

## Related Problems

- [Sort an Array (912)](https://leetcode.com/problems/sort-an-array/)
- [Kth Largest Element in an Array (215)](https://leetcode.com/problems/kth-largest-element-in-an-array/)
- [Sort Colors (75)](https://leetcode.com/problems/sort-colors/)
