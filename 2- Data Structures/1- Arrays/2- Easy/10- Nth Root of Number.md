# Find Nth Root of a Number

`Amazon` • `Directi` • `Accenture`

## Problem Statement
Given two numbers N and M, find the Nth root of M.

- The Nth root of M is a number X such that X raised to the power N equals M (X^N = M).
- If the Nth root is not an integer, return -1.

## Examples
**Example 1**
- Input: N = 3, M = 27
- Output: 3
- Explanation: The cube root of 27 is 3, because 3^3 = 27.

**Example 2**
- Input: N = 4, M = 69
- Output: -1
- Explanation: No integer raised to the power 4 gives 69, so the answer is -1.

## Constraints
- 1 <= N <= 30
- 1 <= M <= 10^9

<br><br>

## Approach 1: Linear Search (Brute Force)

The simplest idea is to just try every number one by one.

- Start from X = 1 and keep going up to M.
- For each X, calculate X^N.
- If X^N equals M, then X is our answer, so return it.
- If X^N becomes greater than M, we can stop early (no bigger number will ever work).
- If we finish the loop without finding anything, return -1.

```python
class Solution:
    def NthRoot(self, n, m):
        for x in range(1, m + 1):
            power = pow(x, n)

            if power == m:
                return x
            if power > m:
                break

        return -1
```

**Why it works:** As X grows, X^N only grows too. So the first X whose power matches M is the answer, and once we cross M there is no point checking further.

- Time Complexity: O(M), since in the worst case we may check up to M numbers.
- Space Complexity: O(1), we only use a couple of variables.

The catch: when M is large (up to 10^9), scanning one by one is far too slow. That is exactly where binary search saves us.

<br><br>

## Approach 2: Binary Search (Optimal)

Here is the key observation: <mark>X^N keeps increasing as X increases.</mark> Because the values are effectively sorted in increasing order, we can binary search instead of checking every single number.

This is the approach I used:

```python
class Solution:
    def NthRoot(self, n, m):
        low = 0
        high = m

        while low <= high:
            mid = (low + high) // 2

            if pow(mid, n) == m:
                return mid
            
            if pow(mid, n) < m:
                low = mid + 1
            else:
                high = mid - 1
        
        return -1
```

**Breaking it down piece by piece:**

- `low = 0` and `high = m`: our answer must lie somewhere between 0 and M, so this is our search range.
- `while low <= high`: keep searching as long as the range is still valid.
- `mid = (low + high) // 2`: pick the middle number of the current range.
- `pow(mid, n) == m`: if mid raised to the power N is exactly M, we found the root, so return mid.
- `pow(mid, n) < m`: mid is too small, so throw away the left half by moving low to mid + 1.
- `else` (which means pow(mid, n) > m): mid is too big, so throw away the right half by moving high to mid - 1.
- `return -1`: if the loop ends and nothing matched, there is no integer root.

- Time Complexity: O(log M), binary search cuts the range in half every step (with a tiny extra cost from pow).
- Space Complexity: O(1).

<br><br>

## Dry Run

Let us trace Approach 2 with N = 3, M = 27.

```ini
Initial:  low = 0,  high = 27

Step 1:   mid = (0 + 27) // 2 = 13
          13^3 = 2197   ->  2197 > 27  ->  too big
          high = 13 - 1 = 12

Step 2:   low = 0,  high = 12
          mid = (0 + 12) // 2 = 6
          6^3 = 216     ->  216 > 27   ->  too big
          high = 6 - 1 = 5

Step 3:   low = 0,  high = 5
          mid = (0 + 5) // 2 = 2
          2^3 = 8       ->  8 < 27     ->  too small
          low = 2 + 1 = 3

Step 4:   low = 3,  high = 5
          mid = (3 + 5) // 2 = 4
          4^3 = 64      ->  64 > 27    ->  too big
          high = 4 - 1 = 3

Step 5:   low = 3,  high = 3
          mid = (3 + 3) // 2 = 3
          3^3 = 27      ->  27 == 27   ->  match found

Answer:   return 3
```

Quick note on the -1 case (N = 4, M = 69): the search halves the range the same way, but no mid ever gives mid^4 = 69. Eventually low becomes greater than high, the loop ends, and we return -1.

<br><br>

## Related Problems
- [Sqrt(x)](https://leetcode.com/problems/sqrtx/)
- [Pow(x, n)](https://leetcode.com/problems/powx-n/)
- [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/)
- [Find the Smallest Divisor Given a Threshold](https://leetcode.com/problems/find-the-smallest-divisor-given-a-threshold/)
- [Binary Search](https://leetcode.com/problems/binary-search/)