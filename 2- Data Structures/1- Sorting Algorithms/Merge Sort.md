# Merge Sort

`Amazon` • `Microsoft`

## Problem Statement

Given an array of integers `arr`, sort it in **ascending order** using **Merge Sort**.

## Examples

**Example 1:**  
Input: `arr = [38, 27, 43, 3]`  
Output: `[3, 27, 38, 43]`

**Example 2:**  
Input: `arr = [5, 1, 1, 2, 0, 0]`  
Output: `[0, 0, 1, 1, 2, 5]`

**Example 3:**  
Input: `arr = [7]`  
Output: `[7]`

## Constraints

- `1 <= arr.length <= 5 * 10^4`
- `-5 * 10^4 <= arr[i] <= 5 * 10^4`

<br><br>

## Approach

<mark>Split the array in half, sort each half recursively, then merge the two sorted halves.</mark>

This is **Divide and Conquer**:

- **Divide:** cut the array in the middle.
- **Conquer:** keep cutting until each piece has 1 element. A single element is already sorted.
- **Combine:** merge two sorted pieces into one sorted piece.

**How merge works:**

- Keep one pointer at the start of each half.
- Compare the two elements, take the smaller one, move that pointer forward.
- When one half runs out, copy the rest of the other half as is.

<br><br>

## Code

```python
class Solution:
    def mergeSort(self, arr):
        # Base case: 0 or 1 element is already sorted
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = self.mergeSort(arr[:mid])
        right = self.mergeSort(arr[mid:])

        return self.merge(left, right)

    def merge(self, a, b):
        result = []
        i = j = 0

        while i < len(a) and j < len(b):
            # <= keeps equal elements in order (stable)
            if a[i] <= b[j]:
                result.append(a[i])
                i += 1
            else:
                result.append(b[j])
                j += 1

        # One side is empty now, copy what's left of the other
        result.extend(a[i:])
        result.extend(b[j:])

        return result
```

<br><br>

## Dry Run

```ini
Input: arr = [38, 27, 43, 3]

Divide
  [38, 27, 43, 3]
  -> [38, 27]        [43, 3]
  -> [38]  [27]      [43]  [3]

Merge [38] and [27]
  27 < 38  take 27
  copy 38            -> [27, 38]

Merge [43] and [3]
  3 < 43   take 3
  copy 43            -> [3, 43]

Merge [27, 38] and [3, 43]
  3 < 27   take 3    -> [3]
  27 < 43  take 27   -> [3, 27]
  38 < 43  take 38   -> [3, 27, 38]
  copy 43            -> [3, 27, 38, 43]

Final Answer: [3, 27, 38, 43]
```

<br><br>

## Complexity

- **Time Complexity:** `O(n log n)` in **every** case. The array is halved `log n` times and each level does `O(n)` merging work.
- **Space Complexity:** `O(n)` for the merged arrays, plus `O(log n)` for the recursion stack.
- **Stable:** Yes, because merge takes from the left half on ties.

<br><br>

## Merge Sort vs Quick Sort

| Aspect      | Merge Sort                 | Quick Sort                        |
| :---------- | :------------------------- | :-------------------------------- |
| Worst case  | `O(n log n)`               | `O(n^2)`                          |
| Extra space | `O(n)`                     | `O(log n)`, in place              |
| Stable      | Yes                        | No                                |
| Best for    | Linked lists, external sort| Arrays in memory                  |

<br><br>

## Related Problems

- [Sort an Array (912)](https://leetcode.com/problems/sort-an-array/)
- [Merge Sorted Array (88)](https://leetcode.com/problems/merge-sorted-array/)
- [Sort List (148)](https://leetcode.com/problems/sort-list/)
- [Merge k Sorted Lists (23)](https://leetcode.com/problems/merge-k-sorted-lists/)
- [Count of Smaller Numbers After Self (315)](https://leetcode.com/problems/count-of-smaller-numbers-after-self/)
- [Reverse Pairs (493)](https://leetcode.com/problems/reverse-pairs/)
