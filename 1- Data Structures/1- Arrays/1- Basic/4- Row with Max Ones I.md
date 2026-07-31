# Row With Maximum Ones I

`Google` • `Amazon` • `Microsoft` • `Arcesium` • `Disney+ Hotstar`

## Problem Statement

You are given an `m x n` binary matrix `mat` (every cell is either `0` or `1`).

Your job is to find the **0-indexed** position of the row that has the **maximum number of ones**, along with how many ones that row contains.

- If more than one row is tied for the most ones, pick the row with the **smallest index**.
- Return an array in the form `[row_index, count_of_ones]`.

## Examples

**Example 1**

```ini
Input:  mat = [[0,1],[1,0]]
Output: [0,1]
```

Both rows have one `1` each, so they are tied. We pick the smaller index (`0`) and its count of ones (`1`).

**Example 2**

```ini
Input:  mat = [[0,0,0],[0,1,1]]
Output: [1,2]
```

Row `1` has two ones, which is the most, so we return `[1, 2]`.

**Example 3**

```ini
Input:  mat = [[0,0],[1,1],[0,0]]
Output: [1,2]
```

Row `1` has two ones, which is the most, so we return `[1, 2]`.

## Constraints

- `m == mat.length`
- `n == mat[i].length`
- `1 <= m, n <= 100`
- `mat[i][j]` is either `0` or `1`.

<br><br>

## Approach

Go through the rows one by one and count how many ones each row has. Keep track of the highest count seen so far along with the index of the row it came from, and update both only when a row has a **bigger** count than the current best. 

<mark>Because we update only on a bigger count and never on a tie, the earlier (smaller) index automatically wins any tie.</mark> After one pass through the matrix, return that row index together with its count of ones.

<br><br>

## Code

```python
class Solution:
    def rowAndMaximumOnes(self, mat: List[List[int]]) -> List[int]:
        best_row = 0
        max_ones = -1
        
        for i, row in enumerate(mat):
            ones_count = sum(row)
            if ones_count > max_ones:
                max_ones = ones_count
                best_row = i
                
        return [best_row, max_ones]
```

<br><br>

## Dry Run

Let us trace the code with `mat = [[1,0,1],[0,1,0],[1,1,0]]`.

```ini
Initial state:
    best_row = 0
    max_ones = -1

Iteration 1  ->  i = 0, row = [1,0,1]
    ones_count = sum([1,0,1]) = 2
    Check: is ones_count (2) > max_ones (-1)?  YES
    Update: max_ones = 2
            best_row = 0
    State now: best_row = 0, max_ones = 2

Iteration 2  ->  i = 1, row = [0,1,0]
    ones_count = sum([0,1,0]) = 1
    Check: is ones_count (1) > max_ones (2)?  NO
    No update (this row has fewer ones).
    State now: best_row = 0, max_ones = 2

Iteration 3  ->  i = 2, row = [1,1,0]
    ones_count = sum([1,1,0]) = 2
    Check: is ones_count (2) > max_ones (2)?  NO
    No update (it only ties, so the earlier row 0 keeps the win).
    State now: best_row = 0, max_ones = 2

Loop finished.
Return [best_row, max_ones] = [0, 2]
```

<br><br>

## Complexity

- **Time:** `O(m * n)`. We visit every cell of the matrix exactly once while summing each row, where `m` is the number of rows and `n` is the number of columns.
- **Space:** `O(1)`. We only use two extra variables (`best_row` and `max_ones`), no matter how large the matrix is.

<br><br>

## Related Problems

- [Count Negative Numbers in a Sorted Matrix (1351)](https://leetcode.com/problems/count-negative-numbers-in-a-sorted-matrix/)
- [Special Positions in a Binary Matrix (1582)](https://leetcode.com/problems/special-positions-in-a-binary-matrix/)
- [Difference Between Ones and Zeros in Row and Column (2482)](https://leetcode.com/problems/difference-between-ones-and-zeros-in-row-and-column/)
- [Number of Laser Beams in a Bank (2125)](https://leetcode.com/problems/number-of-laser-beams-in-a-bank/)
- [Count Servers that Communicate (1267)](https://leetcode.com/problems/count-servers-that-communicate/)