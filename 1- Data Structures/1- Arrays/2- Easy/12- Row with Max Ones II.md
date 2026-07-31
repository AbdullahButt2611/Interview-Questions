# Row With Maximum Ones II

`Amazon` • `Microsoft` • `Paytm` • `Google` • `takeUforward`

## Problem Statement
- You are given a non-empty grid `mat` that contains only `0`s and `1`s.
- Every row is sorted in ascending order, so all the `0`s come first and all the `1`s sit at the end of the row.
- Find and return the index of the row that has the maximum number of `1`s.
- If two rows have the same number of `1`s, return the one with the smaller index.
- If there is no `1` anywhere in the grid, return `-1`.

## Examples
**Example 1**
- Input: `mat = [ [1, 1, 1], [0, 0, 1], [0, 0, 0] ]`
- Output: `0`
- Explanation: Row `0` has three `1`s, which is the highest count. So the answer is `0`.

**Example 2**
- Input: `mat = [ [0, 0], [0, 0] ]`
- Output: `-1`
- Explanation: There is no `1` anywhere in the grid, so we return `-1`.

## Constraints
- `n == mat.length`
- `m == mat[i].length`
- `1 <= n, m <= 100`
- `mat[i][j]` is either `0` or `1`

<br><br>

## Approach

**The whole solution rests on one fact: each row is sorted.**

<mark>Because every row is sorted in ascending order, all the `0`s sit on the left and all the `1`s sit on the right. A row is simply `0`s followed by `1`s, like `0 0 0 1 1`.</mark>

Keep that picture in your head, because everything else falls out of it:

- The `1`s always live at the end of the row.
- So the sooner the first `1` starts, the more `1`s that row has.
- That turns the whole question into one tiny question: **where does the first `1` begin?**

**Count of `1`s in a single row:**

- `count of 1s = total columns - index of the first 1`

**Finding that first `1` fast.** We do not scan the row. Because it is sorted, we use binary search to jump to the first `1` in `log m` time. Sorting is the gift that makes binary search possible here, without it, this trick would not work.

**Now do this in one pass over the rows:**

- Keep `cnt_max = 0` (best count so far) and `index = -1` (the answer).
- For each row, binary search for the first spot where the value is `>= 1`. That spot is the first `1`.
  - Start with `low = 0`, `high = m - 1`, `ans = m` (`ans = m` means "no `1` in this row").
  - Look at the middle. If it is `>= 1`, this might be the first `1`, so save it (`ans = mid`) and search the left half for an even earlier one.
  - If it is `0`, the first `1` is further right, so search the right half.
- Count of `1`s in this row is `m - (index of first 1)`.
- If this count beats `cnt_max`, update `cnt_max` and set `index = i`.
- After all rows are checked, return `index`. If a `1` was never found, it stays `-1`.

<mark>Update only when the new count is strictly greater. That way, if two rows tie, the earlier (smaller index) row keeps the answer on its own.</mark>

<br><br>

## Code
```python
class Solution:
    # Binary search to find the lower bound (first index where element >= x)
    def lower_bound(self, arr, n, x):
        low, high = 0, n - 1
        ans = n  # Default if x not found

        while low <= high:
            mid = (low + high) // 2
            if arr[mid] >= x:
                ans = mid       # Potential answer found
                high = mid - 1  # Look on the left half
            else:
                low = mid + 1   # Move right
        return ans  # Return index of first element >= x

    def rowWithMax1s(self, matrix):
        n = len(matrix)      # Number of rows
        m = len(matrix[0])   # Number of columns
        cnt_max = 0          # Maximum number of 1s found so far
        index = -1           # Row index with the max 1s

        for i in range(n):
            # Calculate count of 1s using lower bound
            cnt_ones = m - self.lower_bound(matrix[i], m, 1)
            if cnt_ones > cnt_max:
                cnt_max = cnt_ones
                index = i
        return index  # Return row index with most 1s
```

<br><br>

## Dry Run
```ini
Input : mat = [ [1, 1, 1],
                [0, 0, 1],
                [0, 0, 0] ]

Initial state  ->  n = 3, m = 3, cnt_max = 0, index = -1


=====================  Row i = 0  =====================
Current row  ->  [1, 1, 1]
Task         ->  find index of first 1 using lower_bound(arr, 3, 1)

  Start  ->  low = 0, high = 2, ans = 3   (ans = 3 means "no 1 found yet")

  Iteration 1  ->  mid = (0 + 2) // 2 = 1
                   arr[1] = 1   ->   1 >= 1 is True
                   So ans = 1, then move left  ->  high = mid - 1 = 0

  Iteration 2  ->  low = 0, high = 0
                   mid = (0 + 0) // 2 = 0
                   arr[0] = 1   ->   1 >= 1 is True
                   So ans = 0, then move left  ->  high = mid - 1 = -1

  Loop stops (low = 0 > high = -1)  ->  first 1 is at index 0

  cnt_ones = m - first_one = 3 - 0 = 3
  Is 3 > cnt_max(0) ?  Yes
  Update  ->  cnt_max = 3, index = 0


=====================  Row i = 1  =====================
Current row  ->  [0, 0, 1]
Task         ->  find index of first 1 using lower_bound(arr, 3, 1)

  Start  ->  low = 0, high = 2, ans = 3

  Iteration 1  ->  mid = (0 + 2) // 2 = 1
                   arr[1] = 0   ->   0 >= 1 is False
                   Move right  ->  low = mid + 1 = 2

  Iteration 2  ->  low = 2, high = 2
                   mid = (2 + 2) // 2 = 2
                   arr[2] = 1   ->   1 >= 1 is True
                   So ans = 2, then move left  ->  high = mid - 1 = 1

  Loop stops (low = 2 > high = 1)  ->  first 1 is at index 2

  cnt_ones = m - first_one = 3 - 2 = 1
  Is 1 > cnt_max(3) ?  No
  No update  ->  cnt_max = 3, index = 0


=====================  Row i = 2  =====================
Current row  ->  [0, 0, 0]
Task         ->  find index of first 1 using lower_bound(arr, 3, 1)

  Start  ->  low = 0, high = 2, ans = 3

  Iteration 1  ->  mid = (0 + 2) // 2 = 1
                   arr[1] = 0   ->   0 >= 1 is False
                   Move right  ->  low = mid + 1 = 2

  Iteration 2  ->  low = 2, high = 2
                   mid = (2 + 2) // 2 = 2
                   arr[2] = 0   ->   0 >= 1 is False
                   Move right  ->  low = mid + 1 = 3

  Loop stops (low = 3 > high = 2)  ->  ans stays 3 (no 1 in this row)

  cnt_ones = m - first_one = 3 - 3 = 0
  Is 0 > cnt_max(3) ?  No
  No update  ->  cnt_max = 3, index = 0


=====================  Final Answer  =====================
All rows checked  ->  return index = 0
```

<br><br>

## Complexity Analysis
- Time Complexity: `O(n * log m)`. For each of the `n` rows we run a binary search that costs `log m`.
- Space Complexity: `O(1)`. We only use a few variables and no extra data structures.

<br><br>

## Related Problems
- [Row With Maximum Ones (2643)](https://leetcode.com/problems/row-with-maximum-ones/)
- [Count Negative Numbers in a Sorted Matrix (1351)](https://leetcode.com/problems/count-negative-numbers-in-a-sorted-matrix/)
- [Search a 2D Matrix (74)](https://leetcode.com/problems/search-a-2d-matrix/)
- [Search a 2D Matrix II (240)](https://leetcode.com/problems/search-a-2d-matrix-ii/)
- [Find First and Last Position of Element in Sorted Array (34)](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/)