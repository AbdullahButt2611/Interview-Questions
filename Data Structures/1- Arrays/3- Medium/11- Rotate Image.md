# Rotate Image

`Google` • `Amazon` • `Meta` • `Microsoft` • `Goldman Sachs` • `Bloomberg` • `J.P. Morgan` • `Capital One`
<br>
## Problem Statement

You are given an `n x n` 2D matrix representing an image, rotate the image by 90 degrees (clockwise).

You have to rotate the image in-place, which means you have to modify the input 2D matrix directly. **DO NOT** allocate another 2D matrix and do the rotation.

### Example 1

```
Input: matrix = [[1,2,3],[4,5,6],[7,8,9]]
Output: [[7,4,1],[8,5,2],[9,6,3]]
```

### Example 2

```
Input: matrix = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]
Output: [[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]
```

### Constraints

- `n == matrix.length == matrix[i].length`
- `1 <= n <= 20`
- `-1000 <= matrix[i][j] <= 1000`

<br><br>

## Approach 1: Brute Force (Auxiliary Matrix)

**Idea:** `(i, j)` moves to `(j, n - 1 - i)` after a 90 degree clockwise rotation. Build a new matrix using this mapping, then copy it back over the original.

```python
class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        n = len(matrix)
        rotated = [[0] * n for _ in range(n)]

        for i in range(n):
            for j in range(n):
                rotated[j][n - 1 - i] = matrix[i][j]

        for i in range(n):
            for j in range(n):
                matrix[i][j] = rotated[i][j]
```

- **Time:** O(n²)
- **Space:** O(n²), uses a second matrix

**Limitation:** Breaks the "no extra 2D matrix" constraint, so it won't satisfy the in-place requirement in an interview.

<br><br>

## Approach 2: Transpose + Reverse (Optimal)

**Idea:** Rotation = transpose + row reversal.
1. Transpose: swap `matrix[i][j]` with `matrix[j][i]` across the diagonal.
2. Reverse each row left to right.

```python
class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        # Transpose Matrix
        for i in range(len(matrix) - 1):
            for j in range(i + 1, len(matrix)):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

        # Reverse Each row
        for row in matrix:
            row.reverse()
```

- **Time:** O(n²)
- **Space:** O(1), in-place

**Why it works:** Transposing only touches the upper triangle (`j > i`), so each pair swaps exactly once. Reversing each row then completes the clockwise turn, all within the original matrix. This is the standard expected solution.

<br><br>

## Summary

| Approach | Time | Space | Notes |
|---|---|---|---|
| Brute Force (Auxiliary Matrix) | O(n²) | O(n²) | Violates in-place constraint |
| Transpose + Reverse | O(n²) | O(1) | Standard interview answer |