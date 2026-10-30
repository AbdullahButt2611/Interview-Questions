# Search a 2D Matrix II

`Amazon` • `Google` • `Microsoft` • `Apple` • `Bloomberg` • `Facebook` • `Oracle` • `LinkedIn` • `Salesforce` • `Goldman Sachs`

## Problem Statement

Write an efficient algorithm that searches for a value `target` in an `m x n` integer matrix. This matrix has the following properties:

- Integers in each **row** are sorted in ascending order from left to right.
- Integers in each **column** are sorted in ascending order from top to bottom.

## Examples

**Example 1:**

```ini
Input: matrix = [[1,4,7,11,15],
                 [2,5,8,12,19],
                 [3,6,9,16,22],
                 [10,13,14,17,24],
                 [18,21,23,26,30]], target = 5
Output: true
```

**Example 2:**

```ini
Input: matrix = [[1,4,7,11,15],
                 [2,5,8,12,19],
                 [3,6,9,16,22],
                 [10,13,14,17,24],
                 [18,21,23,26,30]], target = 20
Output: false
```

## Constraints

- `m == matrix.length`
- `n == matrix[i].length`
- `1 <= n, m <= 300`
- `-10^9 <= matrix[i][j] <= 10^9`
- `-10^9 <= target <= 10^9`

<br><br>

## Approach

### Brute Force (check everything)

The simplest idea is to just look at every number in the matrix one by one.

- Go through each row, and inside each row go through each column.
- Compare every value with the `target`.
- If any value matches, return `true`.
- If you reach the end and nothing matched, return `false`.

This works, but it is slow. In the worst case you touch all `m x n` numbers, and it completely ignores the fact that the matrix is already sorted.

- **Time:** `O(m * n)`
- **Space:** `O(1)`

<br><br>

### Optimal Approach (use the sorting)

The matrix is sorted in a special way, so we should use that instead of blindly checking every cell.

The trick is to <mark>start from the top-right corner</mark> of the matrix.

Why the top-right corner is special:

- Everything to its **left** is smaller (because the row is sorted).
- Everything **below** it is bigger (because the column is sorted).

So the top-right value works like a signpost. One comparison tells you exactly which way to move:

- If the current value **equals** the target, you found it, return `true`.
- If the current value is **bigger** than the target, the target cannot be in this column (everything below is even bigger), so move **left** (`col -= 1`).
- If the current value is **smaller** than the target, the target cannot be in this row (everything to the left is even smaller), so move **down** (`row += 1`).

Every single step throws away one full row or one full column that you never need to look at again. You keep walking until you either land on the target or step outside the matrix.

That is the whole idea: each move deletes a row or a column, so you reach the answer in a straight walk instead of scanning the whole grid.

- **Time:** `O(m + n)`
- **Space:** `O(1)`

<br><br>

## Dry Run

Let us walk through **Example 1** with `target = 5`. We start at the top-right corner, so `row = 0` and `col = 4`.

```ini
Matrix:
[ 1,  4,  7, 11, 15]
[ 2,  5,  8, 12, 19]
[ 3,  6,  9, 16, 22]
[10, 13, 14, 17, 24]
[18, 21, 23, 26, 30]

Start: row = 0, col = 4

Iteration 1:
  matrix[0][4] = 15
  15 > 5  -> value is too big, move left
  col becomes 3

Iteration 2:
  matrix[0][3] = 11
  11 > 5  -> value is too big, move left
  col becomes 2

Iteration 3:
  matrix[0][2] = 7
  7 > 5   -> value is too big, move left
  col becomes 1

Iteration 4:
  matrix[0][1] = 4
  4 < 5   -> value is too small, move down
  row becomes 1

Iteration 5:
  matrix[1][1] = 5
  5 == 5  -> match found!
  return True

Result: true
```

<br><br>

## Code

```python
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        row = 0
        col = len(matrix[0]) - 1

        while row < len(matrix) and col >= 0:
            if matrix[row][col] == target:
                return True
            elif matrix[row][col] < target:
                row += 1
            else:
                col -= 1

        return False
```

<br><br>

## Related Problems

- [Search a 2D Matrix (74)](https://leetcode.com/problems/search-a-2d-matrix/)
- [Kth Smallest Element in a Sorted Matrix (378)](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/)
- [Binary Search (704)](https://leetcode.com/problems/binary-search/)
- [Find K Pairs with Smallest Sums (373)](https://leetcode.com/problems/find-k-pairs-with-smallest-sums/)