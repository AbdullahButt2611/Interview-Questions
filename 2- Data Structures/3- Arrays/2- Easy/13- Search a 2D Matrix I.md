# Search a 2D Matrix I

`Amazon` • `Google` • `Microsoft` • `Uber`

## Problem Statement

You are given an `m x n` integer matrix with two special properties:

- Every row is sorted in non-decreasing order (left to right).
- The first number of each row is greater than the last number of the row above it.

Given an integer `target`, return `true` if `target` is present in the matrix, otherwise return `false`.

<mark>You must solve it in O(log(m * n)) time.</mark>

## Examples

**Example 1**

```ini
Input:  matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
Output: true
```

**Example 2**

```ini
Input:  matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13
Output: false
```

## Constraints

- `m == matrix.length`
- `n == matrix[i].length`
- `1 <= m, n <= 100`
- `-10^4 <= matrix[i][j], target <= 10^4`

<br><br>

## Approach

The matrix looks two dimensional, but the two rules hide a simple secret.

- Each row is sorted.
- Each new row starts with a bigger number than the last number of the row above it.

Put those two facts together and you get one important idea: <mark>if you glued all the rows back into a single line, you would have one perfectly sorted list.</mark>

So the trick is to stop thinking of it as a grid, and start thinking of it as one long sorted array that just happens to be folded into rows.

Once we see it that way, the plan becomes plain binary search:

- We do NOT actually build the 1D array (that would waste memory). We only pretend it exists.
- Our imaginary array has positions from `0` to `(m * n) - 1`.
- We pick the middle position, jump to it, and compare its value with the target, exactly like normal binary search.

The only new piece is translating an imaginary 1D position back into a real (row, column) spot. Two small pieces of math do this, where `n` is the number of columns:

- `row = mid / n` tells you which row the position falls into. Dividing by the row width tells you how many full rows you have already passed.
- `column = mid % n` tells you how far inside that row you are. The remainder is your position within the row.

After that, it is regular binary search:

- If the value equals the target, we found it, return `true`.
- If the value is smaller than the target, the answer must be to the right, so move `low` up.
- If the value is bigger than the target, the answer must be to the left, so move `high` down.

Keep halving the search space until `low` crosses `high`. If we never land on the target, it simply is not there, so return `false`.

<br><br>

## Code

```python
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m = len(matrix)
        n = len(matrix[0])

        low = 0
        high = (m * n) - 1

        while low <= high:
            mid = (low + high) // 2

            row = int(mid / n)
            column = mid % n

            if matrix[row][column] == target:
                return True
            
            if matrix[row][column] < target:
                low = mid + 1
            else:
                high = mid - 1
        
        return False
```

<br><br>

## Dry Run

We will walk through **Example 1** step by step.

```ini
matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]]
target = 3

m = 3   (rows)
n = 4   (columns)

Imagine the matrix as one flat sorted array:
[1, 3, 5, 7, 10, 11, 16, 20, 23, 30, 34, 60]
 0  1  2  3   4   5   6   7   8   9  10  11   <- flat positions

Start:
low  = 0
high = (m * n) - 1 = (3 * 4) - 1 = 11

------------------------------------------------
Iteration 1:
low = 0, high = 11
mid    = (0 + 11) // 2 = 5
row    = 5 / 4 = 1
column = 5 % 4 = 1
matrix[1][1] = 11

Compare: 11 vs target 3  ->  11 > 3
Target is smaller, so search the LEFT half.
high = mid - 1 = 4

------------------------------------------------
Iteration 2:
low = 0, high = 4
mid    = (0 + 4) // 2 = 2
row    = 2 / 4 = 0
column = 2 % 4 = 2
matrix[0][2] = 5

Compare: 5 vs target 3  ->  5 > 3
Target is smaller, so search the LEFT half.
high = mid - 1 = 1

------------------------------------------------
Iteration 3:
low = 0, high = 1
mid    = (0 + 1) // 2 = 0
row    = 0 / 4 = 0
column = 0 % 4 = 0
matrix[0][0] = 1

Compare: 1 vs target 3  ->  1 < 3
Target is bigger, so search the RIGHT half.
low = mid + 1 = 1

------------------------------------------------
Iteration 4:
low = 1, high = 1
mid    = (1 + 1) // 2 = 1
row    = 1 / 4 = 0
column = 1 % 4 = 1
matrix[0][1] = 3

Compare: 3 vs target 3  ->  3 == 3
Match found!
return True
------------------------------------------------

Final Answer: true
```

<br><br>

## Complexity

- **Time:** O(log(m * n))
- **Space:** O(1)

<br><br>

## Related Problems

- [Search a 2D Matrix II (240)](https://leetcode.com/problems/search-a-2d-matrix-ii/)
- [Binary Search (704)](https://leetcode.com/problems/binary-search/)
- [Search Insert Position (35)](https://leetcode.com/problems/search-insert-position/)
- [Find First and Last Position of Element in Sorted Array (34)](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/)
- [Find Minimum in Rotated Sorted Array (153)](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)