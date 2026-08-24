# Equal Row and Column Pairs
`LeetCode 75`

## Problem Statement

You are given a **0-indexed `n x n` integer matrix** called `grid`.

Return the number of pairs `(ri, cj)` such that **row `ri` and column `cj` are exactly the same**.

A row and a column are considered equal if:

* They have the same length
* They contain the same values
* The values appear in the same order

## Example

```
Input:
[
  [3, 2, 1],
  [1, 7, 6],
  [2, 7, 7]
]

Output:
1
```

Only row `1` and column `1` match.

## Constraints

* `1 <= n <= 200`
* `grid.length == n`
* `grid[i].length == n`
* `1 <= grid[i][j] <= 10^5`

<br><br>

## Approach 1: Brute Force Comparison

### Idea

1. Loop through every row.
2. For each row, loop through every column.
3. Build the column array and compare it with the row.
4. Increase the count if they match.

### Code (Python)

```python
class Solution:
    def equalPairs(self, grid):
        n = len(grid)
        count = 0

        for r in range(n):
            for c in range(n):
                column = []
                for i in range(n):
                    column.append(grid[i][c])

                if grid[r] == column:
                    count += 1

        return count
```

### Problem With This Approach

* Building each column repeatedly is slow.
* Time complexity is `O(n^3)`.
* This will be too slow for large inputs.

We can do better by storing rows and columns in a smarter way.

<br><br>

## Approach 2: Hash Map With Tuples (Better Solution)

### Idea

1. Convert each row into a tuple and store its count in a map.
2. Convert each column into a tuple.
3. If the column tuple exists in the row map, add its count to the result.

This avoids repeated comparisons.

### Steps

1. Create a map to store row patterns.
2. Loop through rows and store each row as a tuple.
3. Loop through columns and build each column as a tuple.
4. Add matches from the map.

### Code (Python)

```python
class Solution:
    def equalPairs(self, grid):
        from collections import defaultdict

        n = len(grid)
        row_map = defaultdict(int)

        # Store rows
        for row in grid:
            row_map[tuple(row)] += 1

        count = 0

        # Compare columns
        for c in range(n):
            column = []
            for r in range(n):
                column.append(grid[r][c])

            column_tuple = tuple(column)
            count += row_map[column_tuple]

        return count
```

### Explanation

* Tuples can be used as keys in a map.
* Each row pattern is stored once.
* Each column is checked in `O(n)` time.
* This removes repeated work.

## Time and Space Complexity

* **Time Complexity**: `O(n^2)`
* **Space Complexity**: `O(n^2)` for storing row patterns

<br><br>

## Final Notes

This method is fast, clean, and works well for large matrices. It is a common interview pattern when rows and columns need to be compared.
