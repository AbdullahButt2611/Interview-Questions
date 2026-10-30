# Set Matrix Zeroes

`Google` • `Meta` • `Amazon` • `Microsoft` • `Bloomberg` • `Apple` • `Adobe` • `Goldman Sachs` • `Uber` • `Oracle` • `TakeuForward`
<br>

## Problem Statement

Given an `m x n` integer matrix `matrix`, if an element is `0`, set its entire row and column to `0`'s.

You must do it **in place**.

**Example 1:**

```
Input:  matrix = [[1,1,1],[1,0,1],[1,1,1]]
Output: [[1,0,1],[0,0,0],[1,0,1]]
```

**Example 2:**

```
Input:  matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]
Output: [[0,0,0,0],[0,4,5,0],[0,3,1,0]]
```

**Constraints:**
- `m == matrix.length`
- `n == matrix[0].length`
- `1 <= m, n <= 200`
- `-2^31 <= matrix[i][j] <= 2^31 - 1`

**Follow-up:**
- A straightforward solution using `O(m * n)` space is probably a bad idea.
- A simple improvement uses `O(m + n)` space, but still not the best solution.
- Could you devise a constant space solution?

<br><br>

## Approach 1: Brute Force (In-place Marking with -1)

### Approach

Since the problem requires an in-place solution, we avoid creating a copy of the matrix entirely. The core challenge is: if we start writing `0`s immediately when we find a zero, those freshly written `0`s will be mistaken for original zeros during subsequent iterations, corrupting the result.

The trick is to use `-1` as a temporary marker. Whenever we find an original `0` at `[i][j]`, we traverse its entire row and column and mark every non-zero cell with `-1`. After scanning the entire matrix, we do a final pass and convert all `-1`s to `0`.

**Steps:**
1. Scan every cell. When `matrix[i][j] == 0` is found, traverse row `i` and column `j` and set every non-zero cell to `-1`.
2. After the full scan, traverse the matrix again and convert every `-1` to `0`.

### Solution

```python
class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        rows = len(matrix)
        cols = len(matrix[0])

        def markRow(r):
            for c in range(cols):
                if matrix[r][c] != 0:
                    matrix[r][c] = -1

        def markCol(c):
            for r in range(rows):
                if matrix[r][c] != 0:
                    matrix[r][c] = -1

        # Step 1: Mark rows and columns with -1 wherever original zero is found
        for r in range(rows):
            for c in range(cols):
                if matrix[r][c] == 0:
                    markRow(r)
                    markCol(c)

        # Step 2: Convert all -1s to 0
        for r in range(rows):
            for c in range(cols):
                if matrix[r][c] == -1:
                    matrix[r][c] = 0
```

### Complexity Analysis

| | |
|---|---|
| **Time** | `O(m * n * (m + n))` - for each zero found, we traverse its full row and column |
| **Space** | `O(1)` - no extra space used, all modifications are done in place |

### Problem with this approach

The space is already `O(1)`, which is good. However, the time complexity is expensive at `O(m * n * (m + n))` because for every zero found, we re-traverse its entire row and column. Additionally, this approach relies on `-1` being a safe sentinel value, but the constraints allow negative numbers down to `-2^31`, so `-1` could be a legitimate value in the matrix, which would cause incorrect results. We need a cleaner approach that does not depend on a sentinel value.

<br><br>

## Approach 2: Row and Column Hash Arrays

### Approach

Instead of copying the entire matrix, we use two boolean arrays: `row_zero[i]` to track whether row `i` contains a zero, and `col_zero[j]` to track whether column `j` contains a zero.

We do two passes:
- **First pass:** Scan every cell. If `matrix[i][j] == 0`, mark `row_zero[i] = True` and `col_zero[j] = True`.
- **Second pass:** For each cell `[i][j]`, if either `row_zero[i]` or `col_zero[j]` is `True`, set `matrix[i][j] = 0`.

This separation is critical. If we started zeroing cells immediately during the first pass, we would introduce new zeros that could corrupt the markers for subsequent cells.

### Solution

```python
class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        rows = len(matrix)
        cols = len(matrix[0])

        row_zero = [False] * rows
        col_zero = [False] * cols

        # First pass: record which rows and columns contain a zero
        for r in range(rows):
            for c in range(cols):
                if matrix[r][c] == 0:
                    row_zero[r] = True
                    col_zero[c] = True

        # Second pass: zero out cells whose row or column is marked
        for r in range(rows):
            for c in range(cols):
                if row_zero[r] or col_zero[c]:
                    matrix[r][c] = 0
```

### Complexity Analysis

| | |
|---|---|
| **Time** | `O(m * n)` - two full passes over the matrix |
| **Space** | `O(m + n)` - two auxiliary arrays for row and column flags |

### Problem with this approach

This is much better than the brute force. The time complexity is optimal, and the space has dropped from `O(m * n)` to `O(m + n)`. However, the follow-up challenge asks whether we can get to `O(1)` extra space. The key insight is that we are using two auxiliary arrays purely as flag storage. What if we could repurpose existing cells in the matrix itself to store those flags?

<br><br>

## Approach 3: Constant Space Using First Row and Column as Markers (Optimal)

### Approach

We use the first row and the first column of the matrix itself as our flag arrays, eliminating the need for any auxiliary storage.

The idea is: `matrix[i][0]` will serve as the zero-flag for row `i`, and `matrix[0][j]` will serve as the zero-flag for column `j`.

The tricky part is that `matrix[0][0]` sits at the intersection of the first row and the first column. It cannot represent both flags at once. So we handle the first column separately with a boolean variable `first_col_zero`.

**Steps:**

1. **Pre-check:** Scan column `0` to see if any cell is `0`. Record this in `first_col_zero`.
2. **Mark:** Scan the matrix from `[0][0]` to `[m-1][n-1]`. For any `matrix[i][j] == 0`, set `matrix[i][0] = 0` (mark the row) and `matrix[0][j] = 0` (mark the column). `matrix[0][0]` will serve as the flag for the first row.
3. **Zero out inner cells:** Traverse from `[1][1]` to `[m-1][n-1]`. For any cell where `matrix[i][0] == 0` or `matrix[0][j] == 0`, set `matrix[i][j] = 0`.
4. **Zero out the first row:** If `matrix[0][0] == 0`, zero the entire first row.
5. **Zero out the first column:** If `first_col_zero` is `True`, zero the entire first column.

The order in steps 4 and 5 matters: we handle the first row before the first column to avoid prematurely overwriting `matrix[0][0]`.

### Solution

```python
class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        rows = len(matrix)
        cols = len(matrix[0])

        # Step 1: Check if the first column originally has any zero
        first_col_zero = any(matrix[i][0] == 0 for i in range(rows))

        # Step 2: Use first row and first column as markers
        # matrix[0][0] is the marker for the first row
        for r in range(rows):
            for c in range(cols):
                if matrix[r][c] == 0:
                    matrix[r][0] = 0          # mark the row
                    if c != 0:
                        matrix[0][c] = 0      # mark the column

        # Step 3: Zero out inner cells [1..m-1][1..n-1] based on markers
        for r in range(1, rows):
            for c in range(1, cols):
                if matrix[r][0] == 0 or matrix[0][c] == 0:
                    matrix[r][c] = 0

        # Step 4: Zero out the first row if matrix[0][0] is marked
        if matrix[0][0] == 0:
            for c in range(cols):
                matrix[0][c] = 0

        # Step 5: Zero out the first column if it originally had a zero
        if first_col_zero:
            for r in range(rows):
                matrix[r][0] = 0
```

### Dry Run

```
Input: matrix = [[1,1,1],[1,0,1],[1,1,1]]

Step 1: first_col_zero = False  (no zero in column 0)

Step 2: Scan matrix
  At [1][1] -> matrix[1][1] = 0
    -> matrix[1][0] = 0  (mark row 1)
    -> matrix[0][1] = 0  (mark col 1)

  Matrix after marking:
  [[1, 0, 1],
   [0, 0, 1],
   [1, 1, 1]]

Step 3: Zero out inner cells
  [1][1]: matrix[1][0]=0 -> set to 0  (already 0)
  [1][2]: matrix[1][0]=0 -> set to 0
  [2][1]: matrix[0][1]=0 -> set to 0

  Matrix after inner pass:
  [[1, 0, 1],
   [0, 0, 0],
   [1, 0, 1]]

Step 4: matrix[0][0] = 1 -> skip first row

Step 5: first_col_zero = False -> skip first column

Output: [[1,0,1],[0,0,0],[1,0,1]]  ✓
```

### Complexity Analysis

| | |
|---|---|
| **Time** | `O(m * n)` - constant number of full passes |
| **Space** | `O(1)` - only one extra boolean variable used |

<br><br>

## Summary

| Approach | Time | Space | Notes |
|---|---|---|---|
| Brute Force (Matrix Copy) | `O(m * n * (m + n))` | `O(m * n)` | Simple but wasteful |
| Row/Column Hash Arrays | `O(m * n)` | `O(m + n)` | Clean, optimal time |
| First Row/Col as Markers | `O(m * n)` | `O(1)` | Optimal in both time and space |

The optimal solution reuses the matrix's own first row and column as flag storage, handling the overlap at `matrix[0][0]` by separating the first column flag into a single boolean variable. This achieves constant extra space while maintaining linear time across the full matrix.