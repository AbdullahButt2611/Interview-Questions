# Find a Peak Element II

`Google` • `Amazon` • `Meta`

## Problem Statement

A peak element in a 2D grid is an element that is strictly greater than all of its adjacent neighbors to the left, right, top, and bottom.

Given a 0-indexed `m x n` matrix `mat` where no two adjacent cells are equal, find any peak element `mat[i][j]` and return the length 2 array `[i,j]`.

You may assume that the entire matrix is surrounded by an outer perimeter with the value `-1` in each cell.

You must write an algorithm that runs in `O(m log(n))` or `O(n log(m))` time.

## Examples

```ini
Input: mat = [[1,4],[3,2]]
Output: [0,1]
Explanation: Both 3 and 4 are peak elements so [1,0] and [0,1] are both acceptable answers.
```

```ini
Input: mat = [[10,20,15],[21,30,14],[7,16,32]]
Output: [1,1]
Explanation: Both 30 and 32 are peak elements so [1,1] and [2,2] are both acceptable answers.
```

## Constraints

* `m == mat.length`
* `n == mat[i].length`
* `1 <= m, n <= 500`
* `1 <= mat[i][j] <= 10^5`
* No two adjacent cells are equal.

<br><br>

## Approach

### Step 1: What are we actually looking for?

A **peak** is just a cell that is bigger than all four of its touching neighbors (up, down, left, right). Imagine looking down at a mountain range from a helicopter. A peak is any little bump that is taller than everything right next to it.

```ini
              top = 3
                |
   left = 2 -- [ 9 ] -- right = 5      9 beats 3, 2, 5, and 4,
                |                       so 9 is a PEAK.
            bottom = 4
```

Two things make our life easier:

* We only need to find **any one** peak, not the tallest one. Any bump will do.

* The grid is wrapped in an invisible border of `-1` (the smallest value possible). So a cell sitting on the edge can still be a peak, because its "missing" neighbor counts as `-1`, which every real cell beats. This means **we never need special code for the edges**.

### Step 2: Why not just check every cell?

We could walk through all cells and test each one. That works, but it looks at every single box, which is `O(m * n)` (slow). The problem asks for `O(m log n)` time. That `log` is a big hint: **something must be getting cut in half every round.** Cutting things in half is the fingerprint of binary search.

### Step 3: The one idea that makes everything work

Here is the trick to remember for life:

<mark>If you always step toward a bigger neighbor, you can never fall off the grid, and you must eventually get stuck on a peak.</mark>

Why? The numbers cannot keep growing forever inside a finite grid, so your uphill walk has to stop somewhere. The place where it stops has no bigger neighbor around it, which is exactly the definition of a peak.

```ini
Start anywhere and keep stepping to a BIGGER neighbor:

   1    2    3
   4    6 -> 9      6 sees 9 next door (bigger), so it walks to 9.
   5    7    8

9 has no bigger neighbor, so you STOP.
Wherever you get stuck = a peak. Simple.
```

### Step 4: Turning "walk uphill" into binary search

Walking one step at a time is still slow. To make it fast, we jump using columns instead of single steps.

* Look at the **middle column** of the grid (the whole column, not one cell).

* Find the **biggest value in that middle column**. Say it sits at `(row, mid)`. Call it `BIG`.

* Because `BIG` is the biggest in its own column, it already beats the cell **above** it and the cell **below** it. So the only two neighbors left to worry about are the ones to its **left** and **right**.

* Now just compare `BIG` with those two:

```ini
Columns:   0     1     2     3     4
                      (mid)

              col mid
                |
   ...  [L]   [BIG]   [R]  ...
                |

If BIG > L and BIG > R  ->  BIG is a PEAK. Return it.
If L > BIG              ->  a peak hides on the LEFT.  Search columns [low .. mid-1].
If R > BIG              ->  a peak hides on the RIGHT. Search columns [mid+1 .. high].
```

Each round we throw away half of the columns, which is the binary search we wanted.

### Step 5: Why is it safe to move toward the bigger side?

This is the part most people skip, so let us nail it down. Suppose the **left** neighbor `L` is bigger than `BIG`. Why must a peak really live on the left side?

Picture the **tallest cell in the entire left block** (all columns before `mid`). Call it `T`.

* `T` is the tallest in that block, so it beats its up, down, and left neighbors (they all live in the same block and are smaller).

* Its right neighbor sticks into the middle column. But `BIG` was already the tallest cell in the middle column, and `T` is even bigger than `BIG` (since `T >= L > BIG`). So `T` beats that neighbor too.

That means `T` beats all four of its neighbors, so `T` is a peak, and it sits on the left. So moving left is guaranteed to be safe. The same reasoning works for moving right. **We are never chasing a dead end.**

### Step 6: How fast is it?

* There are a limited number of columns. Each round we drop half of them, so we only ever look at about `log(columns)` of them.

* For each column we visit, we scan every row once to find its biggest value, which costs `rows` work.

* Multiply them: `O(rows * log(columns))`, which matches the required `O(m log n)` (or `O(n log m)`) target.

That is the whole magic in one line: **always move toward the taller side, and half your work disappears each time.**

## Code

```python
class Solution:
    def maxElementRow(self, arr, mid, n):
        maxVal = -1
        maxRow = -1
        
        for i in range(n):
            if arr[i][mid] > maxVal:
                maxVal = arr[i][mid]
                maxRow = i
        
        return maxRow

    def findPeakGrid(self, mat: List[List[int]]) -> List[int]:
        n = len(mat)
        m = len(mat[0])

        low = 0
        high = m - 1

        while low <= high:
            mid = (low + high) // 2
            row = self.maxElementRow(mat, mid, n)
            left = mat[row][mid - 1] if mid - 1 >= 0 else -1
            right = mat[row][mid + 1] if mid + 1 < m else -1

            if mat[row][mid] > left and mat[row][mid] > right:
                return [row, mid]
            elif mat[row][mid] < left:
                high = mid - 1
            else:
                low = mid + 1
```

## Dry Run

We will use Example 2 to see exactly what happens in each step.

```ini
mat = [[10, 20, 15],
       [21, 30, 14],
       [ 7, 16, 32]]

n = 3 (number of rows)
m = 3 (number of columns)

Start: low = 0, high = 2

======================= Iteration 1 =======================
low = 0, high = 2
mid = (0 + 2) // 2 = 1        --> we look at column 1

Column 1 values (top to bottom): 20, 30, 16
Find the biggest in column 1:
    row 0 -> 20  (maxVal = 20, maxRow = 0)
    row 1 -> 30  (30 > 20, so maxVal = 30, maxRow = 1)
    row 2 -> 16  (16 < 30, no change)
So row = 1, the biggest cell is mat[1][1] = 30

Now find left and right neighbors of mat[1][1]:
    left  = mat[1][0] = 21   (mid - 1 = 0, which is valid)
    right = mat[1][2] = 14   (mid + 1 = 2, which is valid)

Compare: is 30 > 21 (left) AND 30 > 14 (right)?
    30 > 21 --> True
    30 > 14 --> True
    Both are True, so mat[1][1] = 30 is a PEAK.

Return [1, 1]
===========================================================

Final Answer: [1, 1]
```

Notice how we found the answer in just one step here, because the very first middle column already contained a peak. In bigger grids, we would keep cutting the columns in half and sliding left or right until we land on one.

<br><br>

## Related Problems

* [Find Peak Element (162)](https://leetcode.com/problems/find-peak-element/)
* [Peak Index in a Mountain Array (852)](https://leetcode.com/problems/peak-index-in-a-mountain-array/)
* [Binary Search (704)](https://leetcode.com/problems/binary-search/)
* [Search a 2D Matrix (74)](https://leetcode.com/problems/search-a-2d-matrix/)
* [Search a 2D Matrix II (240)](https://leetcode.com/problems/search-a-2d-matrix-ii/)