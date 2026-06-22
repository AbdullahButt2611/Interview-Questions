# Pascal's Triangle I

`Accenture` • `Cisco` • `Deloitte` • `Goldman Sachs` • `Google` • `Amazon` • `Nagarro`
<br>

## Problem Statement

Given an integer `numRows`, return the first `numRows` of **Pascal's triangle**.

In Pascal's triangle, each number is the sum of the two numbers directly above it.

**Example 1:**
```
Input: numRows = 5
Output: [[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]
```

**Example 2:**
```
Input: numRows = 1
Output: [[1]]
```

**Constraints:**
- `1 <= numRows <= 30`

<br><br>

## Approach 1: Brute Force (Using nCr for Each Element)

**Intuition:**

Every element in Pascal's triangle at row `r` and column `c` (0-indexed) is mathematically equivalent to the binomial coefficient `C(r, c)` = `r! / (c! * (r-c)!)`. We can compute each element independently using this formula.

**Steps:**
1. For each row `r` from `0` to `numRows - 1`, iterate over each column `c` from `0` to `r`.
2. Compute `C(r, c)` using the factorial formula.
3. Append each computed value to the current row, then append the row to the result.

**Solution:**

```python
from math import factorial
from typing import List

class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        result = []
        for r in range(numRows):
            row = []
            for c in range(r + 1):
                val = factorial(r) // (factorial(c) * factorial(r - c))
                row.append(val)
            result.append(row)
        return result
```

**Explanation:**

For row `r = 4` (the 5th row), elements are:
- `C(4,0)` = 1, `C(4,1)` = 4, `C(4,2)` = 6, `C(4,3)` = 4, `C(4,4)` = 1

This directly gives `[1, 4, 6, 4, 1]`.

**Complexity:**
- Time: `O(n^2 * r)` where factorial computation costs `O(r)` per element
- Space: `O(1)` auxiliary (ignoring the output)

**Problem with this approach:**

Computing `factorial(r)` for every single element is expensive and repetitive. For large rows, these multiplications pile up unnecessarily. We can avoid full factorial computation by observing that each element in a row can be derived from the previous element using a running product.

<br><br>

## Approach 2: Optimised nCr (Row-wise Iterative Binomial)

**Intuition:**

Instead of computing `C(r, c)` from scratch using factorials, we use the recurrence:

```
C(r, c) = C(r, c-1) * (r - c + 1) / c
```

This lets us compute each subsequent element from the previous one in `O(1)` time, making the full row generation `O(r)`.

**Steps:**
1. For each row `r` (1-indexed), start with `ans = 1` (the first element).
2. For each column `col` from `1` to `r - 1`, apply the recurrence to get the next element.
3. Collect all elements into the row.

**Solution:**

```python
from typing import List

class Solution:
    def generateRow(self, row: int) -> List[int]:
        ansRow = []
        ans = 1
        ansRow.append(ans)
        for col in range(1, row):
            ans = ans * (row - col)
            ans = ans // col
            ansRow.append(ans)
        return ansRow

    def generate(self, numRows: int) -> List[List[int]]:
        pascalTree = []
        for row in range(1, numRows + 1):
            pascalTree.append(self.generateRow(row))
        return pascalTree
```

**Explanation:**

For row `5` (1-indexed), `generateRow(5)` computes:
- Start: `ans = 1` → `[1]`
- `col=1`: `ans = 1 * (5-1) / 1` = `4` → `[1, 4]`
- `col=2`: `ans = 4 * (5-2) / 2` = `6` → `[1, 4, 6]`
- `col=3`: `ans = 6 * (5-3) / 3` = `4` → `[1, 4, 6, 4]`
- `col=4`: `ans = 4 * (5-4) / 4` = `1` → `[1, 4, 6, 4, 1]`

Each element is built from the previous one without recomputing factorials.

**Complexity:**
- Time: `O(n^2)` — each of the `n` rows takes `O(row)` to generate
- Space: `O(1)` auxiliary (ignoring the output)

**Problem with this approach:**

Each row is computed independently from scratch. For row `r`, we only need row `r-1` to derive all inner elements directly. We can exploit this to simplify the logic further using a straightforward DP build.

<br><br>

## Approach 3: Dynamic Programming (Build Each Row from the Previous)

**Intuition:**

Every inner element of a row is the sum of the two elements directly above it from the previous row. The first and last elements of every row are always `1`. We can build each row directly from the last appended row.

**Steps:**
1. Initialise the result with `[[1]]`.
2. For each subsequent row, start and end with `1`, and fill inner elements by summing adjacent pairs from the previous row.
3. Append each row to the result.

**Solution:**

```python
from typing import List

class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        result = [[1]]
        for i in range(1, numRows):
            prev = result[i - 1]
            row = [1]
            for j in range(1, len(prev)):
                row.append(prev[j - 1] + prev[j])
            row.append(1)
            result.append(row)
        return result
```

**Explanation:**

For `numRows = 4`:
- Row 0: `[1]`
- Row 1: `[1, 1]` (no inner elements)
- Row 2: `[1, 1+1, 1]` = `[1, 2, 1]`
- Row 3: `[1, 1+2, 2+1, 1]` = `[1, 3, 3, 1]`

This is clean, readable, and avoids any arithmetic beyond simple addition.

**Complexity:**
- Time: `O(n^2)` — total elements across all rows
- Space: `O(1)` auxiliary (ignoring the output)

<br><br>

## Summary

| Approach | Time | Space (Auxiliary) | Notes |
|---|---|---|---|
| Brute Force nCr (Factorial) | `O(n^2 * r)` | `O(1)` | Redundant factorial computation per element |
| Optimised nCr (Iterative) | `O(n^2)` | `O(1)` | Builds each row independently using running product |
| Dynamic Programming | `O(n^2)` | `O(1)` | Builds each row from the previous using addition only |

The **Optimised nCr** approach is best when you need to generate a single arbitrary row efficiently. The **DP approach** is the most intuitive for generating the full triangle and is preferred in most interview settings.