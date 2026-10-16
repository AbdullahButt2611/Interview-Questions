# Print All Divisors of a Number

`Amazon` • `Google`

## Problem Statement

Given an integer `n`, return **all the divisors** of `n` in **ascending order**.

A divisor of `n` is a number that divides `n` with **no remainder** (`n % i == 0`).

## Examples

**Example 1:**

```ini
Input: n = 36
Output: [1, 2, 3, 4, 6, 9, 12, 18, 36]
Explanation: Each of these numbers divides 36 with no remainder.
```

**Example 2:**

```ini
Input: n = 10
Output: [1, 2, 5, 10]
Explanation: 1 x 10 = 10 and 2 x 5 = 10, so the divisors are 1, 2, 5, 10.
```

**Example 3:**

```ini
Input: n = 13
Output: [1, 13]
Explanation: 13 is a prime number, so it is divisible only by 1 and itself.
```

## Constraints

- `1 <= n <= 10^5`

<br><br>

## Approach

### The One Rule to Remember

<mark>Divisors always come in pairs. If i divides n, then n // i divides n too.</mark>

Look at the pairs of `36`:

```ini
1  x 36 = 36
2  x 18 = 36
3  x 12 = 36
4  x  9 = 36
6  x  6 = 36   ← the two sides meet here (6 is the square root of 36)
```

- In every pair, one number is **small** and the other is **big**.
- The small one is **never bigger than the square root** of `n`.
- So we only need to search up to `√n`. Every small divisor we find **hands us its big partner for free**.

### Why Not Check Every Number?

The simple idea is: "try every number from `1` to `n`."

- That works, but it does `n` checks.
- For `n = 100,000`, that is **100,000** checks.
- With the pair trick, we only go up to `√100,000 ≈ 316`. That is about **316** checks.

### The One Trap to Avoid

When `n` is a **perfect square** (like `36`), the middle pair is the **same number twice** (`6 x 6`).

- If we blindly add both sides, `6` shows up **two times**.
- So before adding the partner, we check: is the partner **different** from `i`?
- Same number → add it **once** only.

### Step by Step

1. **Get ready.**
   - Start with an empty list `divisors`.
2. **Loop `i` from `1` up to `√n`** (including `√n`).
3. **Does `i` divide `n`?** Check `n % i == 0`.
   - **No:** skip it and move on.
   - **Yes:** add `i` to the list (this is the **small** partner).
4. **Grab the big partner.**
   - The partner is `n // i`.
   - If `n // i` is **different** from `i`, add it too.
   - If it is the **same**, skip it (this is the perfect square case).
5. **Sort the list.**
   - Pairs are added as small, big, small, big, so the list is jumbled.
   - Sorting puts them in ascending order.
6. **Return** the sorted list.

> Memory hook: <mark>"Search till the square root. Every find brings a partner. Twins count once."</mark>

<br><br>

## Solution

```python
import math

def print_divisors(n):
    divisors = []
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divisors.append(i)  # Add the divisor
            if n // i != i:  # Add the paired divisor only if it's different
                divisors.append(n // i)

    divisors.sort()  # Sort the list of divisors
    return divisors

# Example usage:
n = 36
print(print_divisors(n))
```

<br><br>

## Dry Run

```ini
=====================================================
SCENARIO A: n = 36  (perfect square)
=====================================================

Setup:
  divisors = []
  math.sqrt(36) = 6.0  →  int(6.0) = 6
  Loop range: range(1, 6 + 1) = range(1, 7)
  So i will take the values 1, 2, 3, 4, 5, 6

Iteration 1: i = 1
  Does 1 divide 36? 36 % 1 = 0. YES.
  Add the small partner: divisors.append(1)
    divisors = [1]
  Find the big partner: n // i = 36 // 1 = 36
  Is 36 != 1? YES, they are different.
  Add the big partner: divisors.append(36)
    divisors = [1, 36]

Iteration 2: i = 2
  Does 2 divide 36? 36 % 2 = 0. YES.
  Add the small partner: divisors.append(2)
    divisors = [1, 36, 2]
  Find the big partner: n // i = 36 // 2 = 18
  Is 18 != 2? YES, they are different.
  Add the big partner: divisors.append(18)
    divisors = [1, 36, 2, 18]

Iteration 3: i = 3
  Does 3 divide 36? 36 % 3 = 0. YES.
  Add the small partner: divisors.append(3)
    divisors = [1, 36, 2, 18, 3]
  Find the big partner: n // i = 36 // 3 = 12
  Is 12 != 3? YES, they are different.
  Add the big partner: divisors.append(12)
    divisors = [1, 36, 2, 18, 3, 12]

Iteration 4: i = 4
  Does 4 divide 36? 36 % 4 = 0. YES.
  Add the small partner: divisors.append(4)
    divisors = [1, 36, 2, 18, 3, 12, 4]
  Find the big partner: n // i = 36 // 4 = 9
  Is 9 != 4? YES, they are different.
  Add the big partner: divisors.append(9)
    divisors = [1, 36, 2, 18, 3, 12, 4, 9]

Iteration 5: i = 5
  Does 5 divide 36? 36 % 5 = 1. NO, remainder is 1.
  Skip. Nothing is added.
    divisors = [1, 36, 2, 18, 3, 12, 4, 9]   (unchanged)

Iteration 6: i = 6
  Does 6 divide 36? 36 % 6 = 0. YES.
  Add the small partner: divisors.append(6)
    divisors = [1, 36, 2, 18, 3, 12, 4, 9, 6]
  Find the big partner: n // i = 36 // 6 = 6
  Is 6 != 6? NO, they are the SAME number (the twin case).
  Skip the big partner, so 6 is not added twice.
    divisors = [1, 36, 2, 18, 3, 12, 4, 9, 6]

Loop finished. i = 7 is outside range(1, 7), so we stop.

Sort the list:
  Before: [1, 36, 2, 18, 3, 12, 4, 9, 6]
  After:  [1, 2, 3, 4, 6, 9, 12, 18, 36]

Pairs found:
  (1, 36), (2, 18), (3, 12), (4, 9), (6, 6 counted once)

Total checks: 6 (checking every number up to 36 would need 36)
Return [1, 2, 3, 4, 6, 9, 12, 18, 36]
Output: [1, 2, 3, 4, 6, 9, 12, 18, 36]  ✓


=====================================================
SCENARIO B: n = 10  (square root is not a whole number)
=====================================================

Setup:
  divisors = []
  math.sqrt(10) = 3.162...  →  int(3.162...) = 3   (the decimal is dropped)
  Loop range: range(1, 3 + 1) = range(1, 4)
  So i will take the values 1, 2, 3

Iteration 1: i = 1
  Does 1 divide 10? 10 % 1 = 0. YES.
  Add the small partner: divisors.append(1)
    divisors = [1]
  Find the big partner: n // i = 10 // 1 = 10
  Is 10 != 1? YES, they are different.
  Add the big partner: divisors.append(10)
    divisors = [1, 10]

Iteration 2: i = 2
  Does 2 divide 10? 10 % 2 = 0. YES.
  Add the small partner: divisors.append(2)
    divisors = [1, 10, 2]
  Find the big partner: n // i = 10 // 2 = 5
  Is 5 != 2? YES, they are different.
  Add the big partner: divisors.append(5)
    divisors = [1, 10, 2, 5]

Iteration 3: i = 3
  Does 3 divide 10? 10 % 3 = 1. NO, remainder is 1.
  Skip. Nothing is added.
    divisors = [1, 10, 2, 5]   (unchanged)

Loop finished. i = 4 is outside range(1, 4), so we stop.

Note: 5 is bigger than the square root (3.16), but we still found it.
It came for free as the partner of 2.

Sort the list:
  Before: [1, 10, 2, 5]
  After:  [1, 2, 5, 10]

Return [1, 2, 5, 10]
Output: [1, 2, 5, 10]  ✓


=====================================================
SCENARIO C: n = 13  (prime number)
=====================================================

Setup:
  divisors = []
  math.sqrt(13) = 3.605...  →  int(3.605...) = 3
  Loop range: range(1, 4)
  So i will take the values 1, 2, 3

Iteration 1: i = 1
  Does 1 divide 13? 13 % 1 = 0. YES.
  Add the small partner: divisors.append(1)
    divisors = [1]
  Find the big partner: n // i = 13 // 1 = 13
  Is 13 != 1? YES, they are different.
  Add the big partner: divisors.append(13)
    divisors = [1, 13]

Iteration 2: i = 2
  Does 2 divide 13? 13 % 2 = 1. NO, remainder is 1.
  Skip. Nothing is added.
    divisors = [1, 13]   (unchanged)

Iteration 3: i = 3
  Does 3 divide 13? 13 % 3 = 1. NO, remainder is 1.
  Skip. Nothing is added.
    divisors = [1, 13]   (unchanged)

Loop finished. i = 4 is outside range(1, 4), so we stop.

Sort the list:
  Before: [1, 13]
  After:  [1, 13]   (already sorted)

Note: Only the pair (1, 13) was found. A number with exactly
two divisors (1 and itself) is a prime number.

Return [1, 13]
Output: [1, 13]  ✓


=====================================================
SCENARIO D: n = 1  (smallest input)
=====================================================

Setup:
  divisors = []
  math.sqrt(1) = 1.0  →  int(1.0) = 1
  Loop range: range(1, 2)
  So i will take only the value 1

Iteration 1: i = 1
  Does 1 divide 1? 1 % 1 = 0. YES.
  Add the small partner: divisors.append(1)
    divisors = [1]
  Find the big partner: n // i = 1 // 1 = 1
  Is 1 != 1? NO, they are the SAME number (the twin case).
  Skip the big partner, so 1 is not added twice.
    divisors = [1]

Loop finished. i = 2 is outside range(1, 2), so we stop.

Sort the list:
  [1] stays [1].

Return [1]
Output: [1]  ✓
```

<br><br>

## Complexity Analysis

- **Time Complexity:** `O(√N + D log D)`, where `D` is the number of divisors.
  - The loop runs only up to `√N`, so it does about `√N` checks.
  - Sorting the `D` divisors takes `O(D log D)`.
  - `D` is always very small compared to `N` (for example, `n = 100,000` has only `36` divisors), so the loop is the main cost: <mark>O(√N)</mark>.
- **Space Complexity:** `O(D)`.
  - The list stores all `D` divisors.
  - Apart from that, only the loop variable `i` is used.

<br><br>

## Related Problems

- [Count Primes (204)](https://leetcode.com/problems/count-primes/)
- [Ugly Number (263)](https://leetcode.com/problems/ugly-number/)
- [Perfect Number (507)](https://leetcode.com/problems/perfect-number/)
- [Closest Divisors (1362)](https://leetcode.com/problems/closest-divisors/)
- [Four Divisors (1390)](https://leetcode.com/problems/four-divisors/)
- [The kth Factor of n (1492)](https://leetcode.com/problems/the-kth-factor-of-n/)
- [Three Divisors (1952)](https://leetcode.com/problems/three-divisors/)
- [Find Greatest Common Divisor of Array (1979)](https://leetcode.com/problems/find-greatest-common-divisor-of-array/)
- [Number of Common Factors (2427)](https://leetcode.com/problems/number-of-common-factors/)
- [Sum of Squares of Special Elements (2778)](https://leetcode.com/problems/sum-of-squares-of-special-elements/)
