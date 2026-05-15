# Quick Sort

- **Divide and Conquer** sorting algorithm
- Picks a **pivot** and places it at its correct sorted position
- All elements smaller than pivot go to its **left**, larger go to its **right**
- Then applies the same logic **recursively** on the left and right parts


## How It Works (The Big Picture)

1. **Pick a pivot** (here, the first element of the range).
2. **Partition** the array so that:
   - Pivot ends up at its final sorted position.
   - Smaller elements are on the left, larger on the right.
3. **Recursively** quick sort the left part and the right part.
4. When `low >= high`, the part is already sorted (0 or 1 element), so stop.


## Code

```python
class Solution:
    def quickSort(self, arr, low, high):
        # Base case: only sort if there are at least 2 elements
        if low < high:
            # Partition the array and get the pivot's final position
            p_index = self.partition(arr, low, high)

            # Recursively sort the left part (elements smaller than pivot)
            self.quickSort(arr, low, p_index - 1)

            # Recursively sort the right part (elements larger than pivot)
            self.quickSort(arr, p_index + 1, high)

    def partition(self, arr, low, high):
        # Choose the first element as the pivot
        pivot = arr[low]

        # i starts from the left, j starts from the right
        i = low
        j = high

        # Keep moving i and j toward each other until they cross
        while i < j:

            # Move i to the right while elements are <= pivot
            # (these are already on the correct side)
            while i <= high and arr[i] <= pivot:
                i += 1

            # Move j to the left while elements are > pivot
            # (these are already on the correct side)
            while j >= low and arr[j] > pivot:
                j -= 1

            # If i and j haven't crossed yet, swap the misplaced elements
            # arr[i] is > pivot (wrong side), arr[j] is <= pivot (wrong side)
            if i < j:
                arr[i], arr[j] = arr[j], arr[i]

        # Finally, place the pivot at its correct position by swapping it with arr[j]
        # j now points to the last element that is <= pivot
        arr[low], arr[j] = arr[j], arr[low]

        # Return the pivot's final index
        return j
```


## Dry Run Example

Array: `[5, 3, 8, 1, 9, 2]`, `low = 0`, `high = 5`

- **Pivot** = `arr[0] = 5`
- `i` moves right until it finds something **>** 5 → stops at `8` (index 2)
- `j` moves left until it finds something **<=** 5 → stops at `2` (index 5)
- Swap them → `[5, 3, 2, 1, 9, 8]`
- Continue: `i` stops at `9` (index 4), `j` stops at `1` (index 3)
- `i > j` now → stop the loop
- Swap pivot `arr[low]` with `arr[j]` → `[1, 3, 2, 5, 9, 8]`
- Pivot `5` is at index 3 → **its correct sorted position**

Now recursively sort:
- Left: `[1, 3, 2]` (indices 0 to 2)
- Right: `[9, 8]` (indices 4 to 5)


## Time & Space Complexity

| Case | Time |
|---|---|
| **Best** | `O(n log n)` when the pivot splits the array evenly |
| **Average** | `O(n log n)` |
| **Worst** | `O(n²)` when the array is already sorted or all elements are equal (pivot is always smallest/largest) |

- **Space**: `O(log n)` on average for recursion stack, `O(n)` in the worst case.


## Why It's Fast in Practice

- Even though the worst case is `O(n²)`, on **random data** Quick Sort is usually **faster than Merge Sort** because:
  - It sorts **in-place** (no extra memory allocations).
  - It has **low constant factors** and great cache performance.


## Quick Tips

- To avoid worst case on sorted arrays, pick a **random pivot** or the **median-of-three** instead of the first element.
- Always check the base case `low < high`, because forgetting it causes infinite recursion.
- The partition step is the **heart** of Quick Sort. Understand it once, and the rest is just recursion.
