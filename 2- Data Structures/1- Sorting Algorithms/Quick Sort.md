# Quick Sort

`Google` • `Amazon`

## Problem Statement

Given an array of integers `arr`, sort it in **ascending order** using **Quick Sort**.

## Examples

**Example 1:**  
Input: `arr = [5, 3, 8, 1, 9, 2]`  
Output: `[1, 2, 3, 5, 8, 9]`

**Example 2:**  
Input: `arr = [4, 1, 3, 9, 7]`  
Output: `[1, 3, 4, 7, 9]`

**Example 3:**  
Input: `arr = [7]`  
Output: `[7]`

## Constraints

- `1 <= arr.length <= 5 * 10^4`
- `-5 * 10^4 <= arr[i] <= 5 * 10^4`

<br><br>

## Approach

<mark>Pick a pivot, put it in its final sorted position with smaller elements on its left and bigger ones on its right, then repeat on both sides.</mark>

1. **Pick a pivot.** Here, the first element of the range.
2. **Partition** the range:
   - `i` moves right, skipping elements `<= pivot` (already on the correct side).
   - `j` moves left, skipping elements `> pivot` (already on the correct side).
   - When both stop and haven't crossed, swap `arr[i]` and `arr[j]`.
   - When they cross, swap the pivot with `arr[j]`. The pivot is now in its final spot.
3. **Recurse** on the left part and the right part.
4. **Stop** when `low >= high`. A range with 0 or 1 element is already sorted.

<br><br>

## Code

```python
class Solution:
    def quickSort(self, arr, low, high):
        # Only sort if there are at least 2 elements
        if low < high:
            p_index = self.partition(arr, low, high)

            self.quickSort(arr, low, p_index - 1)
            self.quickSort(arr, p_index + 1, high)

    def partition(self, arr, low, high):
        pivot = arr[low]
        i = low
        j = high

        while i < j:
            # Skip elements already on the left side
            while i <= high and arr[i] <= pivot:
                i += 1

            # Skip elements already on the right side
            while j >= low and arr[j] > pivot:
                j -= 1

            # Both are on the wrong side, swap them
            if i < j:
                arr[i], arr[j] = arr[j], arr[i]

        # j is the last element <= pivot, so the pivot belongs here
        arr[low], arr[j] = arr[j], arr[low]

        return j
```

<br><br>

## Dry Run

```ini
Input: arr = [5, 3, 8, 1, 9, 2], low = 0, high = 5

Partition (pivot = 5)
  i moves right, stops at 8 (index 2)
  j moves left,  stops at 2 (index 5)
  i < j  swap  -> [5, 3, 2, 1, 9, 8]

  i moves right, stops at 9 (index 4)
  j moves left,  stops at 1 (index 3)
  i > j  crossed, stop

  swap pivot with arr[3]  -> [1, 3, 2, 5, 9, 8]
  5 is now at index 3, its final position

Recurse
  Left:  [1, 3, 2]  (indices 0 to 2)  -> [1, 2, 3]
  Right: [9, 8]     (indices 4 to 5)  -> [8, 9]

Final Answer: [1, 2, 3, 5, 8, 9]
```

<br><br>

## Complexity

| Case    | Time         | When                                                        |
| :------ | :----------- | :---------------------------------------------------------- |
| Best    | `O(n log n)` | Pivot splits the range into two equal halves                |
| Average | `O(n log n)` | Random data                                                 |
| Worst   | `O(n^2)`     | Already sorted data or all equal elements (pivot is always the smallest or largest) |

- **Space Complexity:** `O(log n)` on average for the recursion stack, `O(n)` in the worst case.
- **Stable:** No. Partition swaps can reorder equal elements.

<br><br>

## Why It's Fast in Practice

Even with an `O(n^2)` worst case, Quick Sort usually beats Merge Sort on random data:

- It sorts **in place**, so there are no extra arrays to allocate.
- It scans memory in order, which is **cache friendly**.

<br><br>

## Tips

- To avoid the worst case on sorted input, pick a **random pivot** or the **median of three**.
- Don't forget the base case `low < high`. Without it, the recursion never ends.
- Partition is the whole algorithm. The rest is two recursive calls.

<br><br>

## Related Problems

- [Sort an Array (912)](https://leetcode.com/problems/sort-an-array/)
- [Kth Largest Element in an Array (215)](https://leetcode.com/problems/kth-largest-element-in-an-array/)
- [K Closest Points to Origin (973)](https://leetcode.com/problems/k-closest-points-to-origin/)
- [Sort Colors (75)](https://leetcode.com/problems/sort-colors/)
