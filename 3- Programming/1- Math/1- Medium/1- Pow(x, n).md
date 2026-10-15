# Pow(x, n)

`Meta` • `LinkedIn` • `Bloomberg` • `Amazon` • `Educative`

## Problem Statement

Implement `pow(x, n)`, which calculates `x` raised to the power `n` (i.e., `x^n`).

## Examples

**Example 1:**

```ini
Input: x = 2.00000, n = 10
Output: 1024.00000
```

**Example 2:**

```ini
Input: x = 2.10000, n = 3
Output: 9.26100
```

**Example 3:**

```ini
Input: x = 2.00000, n = -2
Output: 0.25000
Explanation: 2^-2 = 1/2^2 = 1/4 = 0.25
```

## Constraints

- `-100.0 < x < 100.0`
- `-2^31 <= n <= 2^31 - 1`
- `n` is an integer.
- Either `x` is not zero or `n > 0`.
- `-10^4 <= x^n <= 10^4`

<br><br>

## Approach

### The One Rule to Remember

<mark>Every number can be broken into powers of 2</mark>, and that is exactly what its binary form shows.

- `10` in binary is `1010`, which means `10 = 8 + 2`.
- So `x^10 = x^8 * x^2`.
- We only need `x^8` and `x^2`. Nothing else.

### Why Not the Simple Way?

The simple idea is: "multiply `x` by itself `n` times."

```python
ans = 1
for _ in range(abs(n)):
    ans *= x
```

- This is correct, but it is **too slow**.
- `n` can be as big as `2^31 - 1`, which is about **2.1 billion**.
- That means about **2.1 billion multiplications** in a loop.
- Python does roughly **10 to 50 million** simple loop steps per second.
- So this would take **minutes**, but LeetCode only allows a **couple of seconds**.
- Result: <mark>Time Limit Exceeded (TLE)</mark>.

> The simple way does `n` steps. Our way does only about `log2(n)` steps. For `n = 2.1 billion`, that is about **31 steps** instead of 2.1 billion.

### The Two Tricks That Make It Fast

**Trick 1: Squaring climbs very fast.**

- Start with `x`.
- Square it: `x^2`. Square again: `x^4`. Again: `x^8`. Again: `x^16`.
- Each square **doubles** the power with just **one** multiplication.
- After only 31 squares, you reach `x^(2^31)`.

**Trick 2: The binary digits tell you which squares to keep.**

- Read `n` in binary from **right to left** (smallest digit first).
- Each digit matches one square: `x^1`, `x^2`, `x^4`, `x^8`, ...
- Digit is `1` → **keep** that square (multiply it into the answer).
- Digit is `0` → **skip** it.

### How the Code Reads Binary Without Converting It

We never build a binary string. Two simple operations do the job:

- `binForm % 2 == 1` → "Is the **last** binary digit a `1`?" (Is the number odd?)
- `binForm //= 2` → "**Chop off** the last binary digit." (Halve the number.)

### What About Negative `n`?

- A negative power just means **flip** the answer: `x^-n = 1 / x^n`.
- So we work with `abs(n)` the whole time.
- At the very end, if `n` was negative, return `1 / ans`.

> In Python, `abs(-2^31)` is safe because Python integers never overflow. (In Java or C++, you would need a `long` here.)

### Step by Step

1. **Get ready.**
   - `binForm = abs(n)`, the power we still need to cover.
   - `ans = 1`, the running answer.
2. **Loop while `binForm > 0`.**
   - **Odd?** If `binForm % 2 == 1`, the current square is needed. Do `ans = ans * x`.
   - **Square.** Do `x *= x`, so `x` moves to the next square (`x^1 → x^2 → x^4 → ...`).
   - **Halve.** Do `binForm //= 2`, which removes the binary digit we just used.
3. **Finish.**
   - If `n` was negative, return `1 / ans`.
   - Otherwise, return `ans`.

> Memory hook: <mark>"Odd? Grab it. Then square x, halve n. Repeat."</mark>

<br><br>

## Solution

```python
class Solution:
    def myPow(self, x: float, n: int) -> float:
        binForm = abs(n)
        ans = 1

        while binForm > 0:
            if binForm % 2 == 1:
                ans = ans * x
            x *= x
            binForm //= 2

        return 1 / ans if n < 0 else ans
```

<br><br>

## Dry Run

```ini
=====================================================
SCENARIO A: x = 2.0, n = 10
=====================================================

Binary view first:
  10 in binary = 1010
  Reading right to left: 0, 1, 0, 1
  Matching squares:      x^1, x^2, x^4, x^8
  Keep the ones with 1:  x^2 and x^8
  So 2^10 = 2^2 * 2^8 = 4 * 256 = 1024

Setup:
  binForm = abs(10) = 10
  ans     = 1
  x       = 2.0   (this is x^1)

Iteration 1:
  Loop check: binForm = 10 > 0. Enter loop.
  Is binForm odd? 10 % 2 = 0. NO.
    Last binary digit is 0, so skip x^1 = 2.
    ans = 1 (unchanged)
  Square x: x = 2 * 2 = 4          (x now holds x^2)
  Halve binForm: 10 // 2 = 5       (binary 1010 → 101)

Iteration 2:
  Loop check: binForm = 5 > 0. Enter loop.
  Is binForm odd? 5 % 2 = 1. YES.
    Last binary digit is 1, so keep x^2 = 4.
    ans = 1 * 4 = 4
  Square x: x = 4 * 4 = 16         (x now holds x^4)
  Halve binForm: 5 // 2 = 2        (binary 101 → 10)

Iteration 3:
  Loop check: binForm = 2 > 0. Enter loop.
  Is binForm odd? 2 % 2 = 0. NO.
    Last binary digit is 0, so skip x^4 = 16.
    ans = 4 (unchanged)
  Square x: x = 16 * 16 = 256      (x now holds x^8)
  Halve binForm: 2 // 2 = 1        (binary 10 → 1)

Iteration 4:
  Loop check: binForm = 1 > 0. Enter loop.
  Is binForm odd? 1 % 2 = 1. YES.
    Last binary digit is 1, so keep x^8 = 256.
    ans = 4 * 256 = 1024
  Square x: x = 256 * 256 = 65536  (x now holds x^16, not needed anymore)
  Halve binForm: 1 // 2 = 0        (binary 1 → nothing left)

Iteration 5:
  Loop check: binForm = 0. Exit loop.

Finish:
  Is n (10) < 0? NO. Return ans as it is.

Total loop runs: 4 (the simple way would need 10 multiplications)
Return 1024.0
Output: 1024.00000  ✓


=====================================================
SCENARIO B: x = 2.1, n = 3
=====================================================

Binary view first:
  3 in binary = 11
  Reading right to left: 1, 1
  Matching squares:      x^1, x^2
  Keep both: 2.1^3 = 2.1^1 * 2.1^2

Setup:
  binForm = abs(3) = 3
  ans     = 1
  x       = 2.1   (this is x^1)

Iteration 1:
  Loop check: binForm = 3 > 0. Enter loop.
  Is binForm odd? 3 % 2 = 1. YES.
    Keep x^1 = 2.1.
    ans = 1 * 2.1 = 2.1
  Square x: x = 2.1 * 2.1 = 4.41   (x now holds x^2)
  Halve binForm: 3 // 2 = 1        (binary 11 → 1)

Iteration 2:
  Loop check: binForm = 1 > 0. Enter loop.
  Is binForm odd? 1 % 2 = 1. YES.
    Keep x^2 = 4.41.
    ans = 2.1 * 4.41 = 9.261
  Square x: x = 4.41 * 4.41 = 19.4481   (x^4, not needed anymore)
  Halve binForm: 1 // 2 = 0

Iteration 3:
  Loop check: binForm = 0. Exit loop.

Finish:
  Is n (3) < 0? NO. Return ans as it is.

Return 9.261
Output: 9.26100  ✓


=====================================================
SCENARIO C: x = 2.0, n = -2  (negative power)
=====================================================

Binary view first:
  abs(-2) = 2, and 2 in binary = 10
  Reading right to left: 0, 1
  Matching squares:      x^1, x^2
  Keep only x^2. Then flip it at the end because n is negative.

Setup:
  binForm = abs(-2) = 2   (we work with the positive version)
  ans     = 1
  x       = 2.0

Iteration 1:
  Loop check: binForm = 2 > 0. Enter loop.
  Is binForm odd? 2 % 2 = 0. NO.
    Skip x^1 = 2.
    ans = 1 (unchanged)
  Square x: x = 2 * 2 = 4          (x now holds x^2)
  Halve binForm: 2 // 2 = 1

Iteration 2:
  Loop check: binForm = 1 > 0. Enter loop.
  Is binForm odd? 1 % 2 = 1. YES.
    Keep x^2 = 4.
    ans = 1 * 4 = 4
  Square x: x = 4 * 4 = 16
  Halve binForm: 1 // 2 = 0

Iteration 3:
  Loop check: binForm = 0. Exit loop.

Finish:
  ans = 4, which is 2^2.
  Is n (-2) < 0? YES. Flip it.
  Return 1 / 4 = 0.25

Output: 0.25000  ✓


=====================================================
SCENARIO D: x = 5.0, n = 0  (power of zero)
=====================================================

Setup:
  binForm = abs(0) = 0
  ans     = 1
  x       = 5.0

Iteration 1:
  Loop check: binForm = 0. Condition 0 > 0 is False.
  The loop never runs.

Finish:
  Is n (0) < 0? NO. Return ans as it is.

Note: Anything raised to the power 0 is 1, and ans already starts at 1.
So no special check is needed for n = 0.

Return 1
Output: 1.00000  ✓


=====================================================
SCENARIO E: n = 2^31 - 1 = 2,147,483,647  (why the simple way gives TLE)
=====================================================

Simple way (multiply n times):
  Loop runs 2,147,483,647 times.
  At ~20 million steps per second in Python, that is ~107 seconds.
  LeetCode limit is about 1 to 2 seconds.  →  TLE  ✗

Our way (square and halve):
  binForm values: 2147483647 → 1073741823 → 536870911 → ... → 3 → 1 → 0
  Each loop halves binForm, so the loop runs only 31 times.
  At most 2 multiplications per loop = about 62 multiplications total.  →  Instant  ✓
```

<br><br>

## Complexity Analysis

- **Time Complexity:** `O(log N)`, where `N` is `abs(n)`.
  - Every loop run cuts `binForm` in half.
  - So the loop runs once per binary digit of `n`, which is about `log2(N)` times.
  - Even for the largest `n` (about 2.1 billion), that is only **31** loop runs.
- **Space Complexity:** `O(1)`.
  - Only a few variables (`binForm`, `ans`, `x`) are used.
  - No recursion and no extra data structures.

<br><br>

## Related Problems

- [Divide Two Integers (29)](https://leetcode.com/problems/divide-two-integers/)
- [Sqrt(x) (69)](https://leetcode.com/problems/sqrtx/)
- [Number of 1 Bits (191)](https://leetcode.com/problems/number-of-1-bits/)
- [Power of Two (231)](https://leetcode.com/problems/power-of-two/)
- [Power of Three (326)](https://leetcode.com/problems/power-of-three/)
- [Power of Four (342)](https://leetcode.com/problems/power-of-four/)
- [Super Pow (372)](https://leetcode.com/problems/super-pow/)
- [Count Good Numbers (1922)](https://leetcode.com/problems/count-good-numbers/)
