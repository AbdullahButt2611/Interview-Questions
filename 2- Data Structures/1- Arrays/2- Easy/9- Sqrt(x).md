# Sqrt(x)

`Amazon` • `Google` • `Microsoft` • `Apple` • `Bloomberg` • `Adobe` • `Meta` • `Uber`

## Problem Statement

Given a non-negative integer `x`, return the square root of `x` rounded **down** to the nearest integer.

- The returned integer should be non-negative as well.
- You must not use any built-in exponent function or operator.
- <mark>For example, do not use `pow(x, 0.5)` in C++ or `x ** 0.5` in Python.</mark>

## Examples

**Example 1**

```ini
Input: x = 4
Output: 2
Explanation: The square root of 4 is 2, so we return 2.
```

**Example 2**

```ini
Input: x = 8
Output: 2
Explanation: The square root of 8 is 2.82842..., and since we round it down to the nearest integer, 2 is returned.
```

## Constraints

- `0 <= x <= 2^31 - 1`

<br><br>

## Approach 1: Built-in Square Root

The simplest idea is to directly ask the language for the square root and truncate the decimal part.

- Call `math.sqrt(x)` to get the floating point root.
- Convert it to an `int`, which drops everything after the decimal point.

**Code**

```python
import math

class Solution:
    def mySqrt(self, x: int) -> int:
        return int(math.sqrt(x))
```

**Important note**

- This is shown only for completeness. <mark>It does not satisfy the problem, because `math.sqrt` is a built-in square root helper and the question forbids using built-in exponent style functions.</mark>

**Complexity**

- Time: `O(1)` (single library call)
- Space: `O(1)`

<br><br>

## Approach 2: Linear Loop

Since the answer grows as the number grows, we can simply count upward until the square of our candidate crosses `x`.

- Start with a candidate `i = 0`.
- Keep increasing `i` while `i * i` is still less than or equal to `x`.
- The moment `i * i` becomes larger than `x`, the previous value (`i - 1`) is our floored square root.

**Code**

```python
class Solution:
    def mySqrt(self, x: int) -> int:
        i = 0
        while i * i <= x:
            i += 1
        return i - 1
```

**Dry Run (x = 8)**

```ini
i = 0 -> 0 * 0 = 0  <= 8  -> i becomes 1
i = 1 -> 1 * 1 = 1  <= 8  -> i becomes 2
i = 2 -> 2 * 2 = 4  <= 8  -> i becomes 3
i = 3 -> 3 * 3 = 9  >  8  -> stop the loop
return i - 1 = 3 - 1 = 2
Answer = 2
```

**Complexity**

- Time: `O(sqrt(x))` (we iterate up to the square root of `x`)
- Space: `O(1)`

<br><br>

## Approach 3: Binary Search (Optimal)

The candidate answers `0, 1, 2, ... x` form a sorted range, and `mid * mid` increases as `mid` increases. That monotonic behaviour is exactly what binary search needs.

- Set `low = 0` and `high = x`, and keep a variable `ans` for the best valid candidate.
- Take the middle value `mid`.
  - If `mid * mid <= x`, then `mid` could be the answer, so store it in `ans` and search the right half (`low = mid + 1`) for something bigger.
  - Otherwise `mid` is too large, so search the left half (`high = mid - 1`).
- When the range closes, `ans` holds the largest integer whose square stays within `x`.

**Code**

```python
class Solution:
    def mySqrt(self, x: int) -> int:
        low = 0
        high = x
        ans = 0

        while low <= high:
            mid = (low + high) // 2

            if mid * mid <= x:
                ans = mid
                low = mid + 1
            else:
                high = mid - 1

        return ans
```

**Dry Run (x = 8)**

```ini
Start: low = 0, high = 8, ans = 0

Step 1: mid = (0 + 8) // 2 = 4
        4 * 4 = 16 > 8  -> too big -> high = 3

Step 2: low = 0, high = 3
        mid = (0 + 3) // 2 = 1
        1 * 1 = 1 <= 8  -> ans = 1, low = 2

Step 3: low = 2, high = 3
        mid = (2 + 3) // 2 = 2
        2 * 2 = 4 <= 8  -> ans = 2, low = 3

Step 4: low = 3, high = 3
        mid = (3 + 3) // 2 = 3
        3 * 3 = 9 > 8   -> too big -> high = 2

Now low = 3 > high = 2 -> loop ends
return ans = 2
Answer = 2
```

**Complexity**

- Time: `O(log x)` (search space is halved every step)
- Space: `O(1)`

<br><br>

## Related Problems

- [Pow(x, n)](https://leetcode.com/problems/powx-n/)
- [Valid Perfect Square](https://leetcode.com/problems/valid-perfect-square/)
- [Search Insert Position](https://leetcode.com/problems/search-insert-position/)
- [Find First and Last Position of Element in Sorted Array](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/)