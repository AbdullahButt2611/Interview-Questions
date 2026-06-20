# Spiral Matrix

`Google` • `Amazon` • `Meta` • `Microsoft` • `Bloomberg` • `Goldman Sachs` • `Apple` • `Adobe`

## Problem Statement

Given an `m x n` matrix, return all elements of the matrix in spiral order (clockwise, starting from the top left corner).

## Examples

**Example 1:**
```
Input:  matrix = [[1,2,3],[4,5,6],[7,8,9]]
Output: [1,2,3,6,9,8,7,4,5]
```

**Example 2:**
```
Input:  matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
Output: [1,2,3,4,8,12,11,10,9,5,6,7]
```

## Constraints

- `m == matrix.length`
- `n == matrix[i].length`
- `1 <= m, n <= 10`
- `-100 <= matrix[i][j] <= 100`

<br><br>

## Approach: Boundary Shrinking

Track four boundaries: `top`, `bottom`, `left`, `right`. These mark the current unvisited rectangle of the matrix. On each pass:

1. Traverse the top row, left to right. Move `top` down by one.
2. Traverse the right column, top to bottom. Move `right` left by one.
3. If `top <= bottom`, traverse the bottom row, right to left. Move `bottom` up by one.
4. If `left <= right`, traverse the left column, bottom to top. Move `left` right by one.

Repeat until `left > right` or `top > bottom`. The checks in steps 3 and 4 stop a row or column from being counted twice once the unvisited region collapses into a single row or column.

```python3
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        rows, cols = len(matrix), len(matrix[0])
        result = []

        top, bottom = 0, rows - 1
        left, right = 0, cols - 1

        while top <= bottom and left <= right:
            for col in range(left, right + 1):
                result.append(matrix[top][col])
            top += 1

            for row in range(top, bottom + 1):
                result.append(matrix[row][right])
            right -= 1

            if top <= bottom:
                for col in range(right, left - 1, -1):
                    result.append(matrix[bottom][col])
                bottom -= 1

            if left <= right:
                for row in range(bottom, top - 1, -1):
                    result.append(matrix[row][left])
                left += 1

        return result
```

**Explanation:**
Each pass peels off the outermost layer of the remaining matrix and shrinks the boundaries inward. The two guard conditions handle the edge case of a single remaining row or column, so cells are never appended twice. Every cell is appended exactly once, and the boundaries only move inward, so the loop terminates naturally after the last layer.

**Complexity:**
Time: O(m x n), every cell is visited exactly once.
Space: O(1) extra space, not counting the output array.

<br><br>

## Why the Conditions Are Written This Way

**1. Why `and`, not `or`, in the while loop?**

Picture a matrix with just one row:

```
[1, 2, 3, 4, 5]
```

`top = 0`, `bottom = 0`, `left = 0`, `right = 4`

After the first lap around the loop, the top row pass reads all 5 numbers and `top` becomes `1`. Now `top (1)` is greater than `bottom (0)`, meaning there are zero rows left. But `left (0)` is still less than `right (3)`, meaning columns still look "available".

- With **`and`**: `top <= bottom` is False, so the whole condition is False. The loop stops right away. Correct, since with no rows left there is nothing left to read.
- With **`or`**: `left <= right` is still True, so the loop runs again, even though there are no rows left. The code then tries to read `matrix[top][...]`, which is `matrix[1][...]`, a row that doesn't exist. That's a crash.

A spiral needs both a row and a column to draw its next lap. `and` checks for both at once, which is why it's correct here.

**2. Why check `top <= bottom` and `left <= right` again before the last two passes?**

Picture a matrix with just one column:

```
[1]
[2]
[3]
```

`top = 0`, `bottom = 2`, `left = 0`, `right = 0`

1. Top row pass reads `1`. `top` becomes `1`.
2. Right column pass reads `2` and `3`. `right` becomes `-1`.

At this point every number has already been read. But the loop still has two more passes lined up: the bottom row pass and the left column pass.

- The guard `if left <= right` checks `0 <= -1`, which is False, so the left column pass is skipped.
- If that guard wasn't there, the code would read `matrix[1][0]`, which is `2`, a number we already added. That's a duplicate in the output.

The guard is simply the code asking "is there still a fresh row (or column) waiting, or did I already grab it in an earlier pass?" before reading anything else.

<br><br>

## Importance of This Question

This problem only has one accepted, optimal solution, the boundary shrinking simulation above. There is no faster algorithm or smarter trick to fall back on, which is exactly why interviewers like asking it. It tests two specific things.

1. **Implementation skill.** \
The logic is simple to describe but easy to get wrong in code. Off by one errors in the boundary updates, or forgetting the two guard conditions, are common mistakes. Getting it right shows you can translate a clear idea into correct, bug free code.
2. **Code cleanliness.** \
Since there is no algorithmic complexity to hide behind, the interviewer is really watching how you structure the loop, name your variables, and handle edge cases (single row, single column, non square matrices). Clean, readable code matters more here than in problems with a "clever" optimization.