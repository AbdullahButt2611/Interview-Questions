# Find Missing Number

`Amazon` • `Google` • `Adobe` • `Microsoft` • `Meta` • `Apple` • `Uber` • `Goldman Sachs`
<br>

**Difficulty:** Easy \
**Topic Tags:** Array, Math, Bit Manipulation, Brute Force

<br>

## Problem Statement

Given an integer array of size `n-1` containing **distinct** values in the range from `1` to `n` (inclusive), return the **only number missing** from the array within this range.

## Examples

**Example 1**
```
Input:  nums = [2, 3, 1, 4]
Output: 5
```
`nums` contains `1, 2, 3, 4`, leaving `5` as the only missing number in the range `[1, 5]`.

**Example 2**
```
Input:  nums = [1, 2, 4, 5, 6]
Output: 3
```
`nums` contains `1, 2, 4, 5, 6`, leaving `3` as the only missing number in the range `[1, 6]`.

## Constraints

- `n == nums.length + 1`
- `1 <= n <= 10^4`
- `1 <= nums[i] <= n`
- All numbers in `nums` are **unique**.

<br><br>

## Approach 1: Brute Force (Nested Loop)

**Intuition**

The most straightforward approach: for every number `i` in the range `1` to `n`, scan the entire array and check whether `i` exists. If after checking the whole array we never found `i`, then `i` is the missing number.

**Steps**
1. Compute `n = len(nums) + 1`.
2. For each `i` from `1` to `n`, iterate through `nums`.
3. If `i` is never found in `nums`, return `i`.

**Solution**

```python
def missingNumber(nums: list[int]) -> int:
    n = len(nums) + 1

    for i in range(1, n + 1):
        found = False
        for num in nums:
            if num == i:
                found = True
                break
        if not found:
            return i
```

**Walkthrough with Example 1:** `nums = [2, 3, 1, 4]`, `n = 5`

```
i=1: scan [2,3,1,4] => found (1 exists)
i=2: scan [2,3,1,4] => found (2 exists)
i=3: scan [2,3,1,4] => found (3 exists)
i=4: scan [2,3,1,4] => found (4 exists)
i=5: scan [2,3,1,4] => NOT found => return 5  ✓
```

**Complexity**
- Time: `O(n^2)`, for each of the `n` candidates we scan the entire array.
- Space: `O(1)`, no extra data structures used.

**Problem with this approach**

The nested loop makes this quadratic in time. For `n = 10^4` that means up to 10^8 operations, which is far too slow. We need a smarter way to identify the missing number in a single pass.

<br><br>

## Approach 2: Gauss Sum Formula

**Intuition**

If all numbers from `1` to `n` were present, their sum would equal the well-known formula `n * (n + 1) / 2`. Since exactly one number is missing, the actual sum of the array falls short of this expected sum by exactly that missing number. Subtract the actual sum from the expected sum and you have your answer, in constant space and linear time.

**Steps**
1. Compute `n = len(nums) + 1` since the array has one element fewer than the full range.
2. Compute `expected = n * (n + 1) / 2`.
3. Compute `actual = sum(nums)`.
4. Return `expected - actual`.

**Solution**

```python
def missingNumber(nums: list[int]) -> int:
    n = len(nums) + 1
    expected = n * (n + 1) // 2
    actual = sum(nums)
    return expected - actual
```

**Walkthrough with Example 1:** `nums = [2, 3, 1, 4]`, `n = 5`

```
expected = 5 * 6 // 2 = 15
actual   = 2 + 3 + 1 + 4 = 10
missing  = 15 - 10 = 5  ✓
```

**Complexity**
- Time: `O(n)`, single pass to sum the array.
- Space: `O(1)`, only two integer variables used.

**Why this is better**

We went from `O(n^2)` down to `O(n)` time while keeping space at `O(1)`. A massive improvement over brute force.

**Can we do even better?**

The sum approach is excellent but carries one subtle concern: for very large arrays, the accumulated sum could overflow a fixed-width integer in typed languages like Java or C++. There is an alternative that avoids accumulating any large value entirely, by working at the bit level.

<br><br>

## Approach 3: XOR Bit Manipulation (Optimal)

**Intuition**

XOR has two powerful properties: `a ^ a = 0` and `a ^ 0 = a`. If we XOR every number in the full range `1` to `n` together with every value in `nums`, all numbers that appear in both will cancel each other out to `0`. The only number left standing is the one that appeared in the range but never in the array, which is exactly the missing number.

**Steps**
1. Compute `n = len(nums) + 1`.
2. Initialize `result = 0`.
3. XOR `result` with every number from `1` to `n`.
4. XOR `result` with every value in `nums`.
5. Return `result`.

**Solution**

```python
def missingNumber(nums: list[int]) -> int:
    n = len(nums) + 1
    result = 0

    for i in range(1, n + 1):
        result ^= i

    for num in nums:
        result ^= num

    return result
```

**Walkthrough with Example 1:** `nums = [2, 3, 1, 4]`, `n = 5`

```
XOR full range 1..5:  1 ^ 2 ^ 3 ^ 4 ^ 5
XOR all values:       2 ^ 3 ^ 1 ^ 4

Combined: 1^2^3^4^5 ^ 2^3^1^4
Every number present cancels with its twin from the range.
Only 5 has no matching value in nums => result = 5  ✓
```

**Complexity**
- Time: `O(n)`, two linear passes, each O(n).
- Space: `O(1)`, just one integer variable.

**Why this is the best approach**

Same time and space as Approach 2, but avoids any risk of integer overflow since XOR operates on individual bits and never accumulates a large intermediate value. It is also the most impressive answer to give in an interview as it demonstrates solid understanding of bit manipulation.

<br><br>

## Summary

| Approach | Time | Space | Notes |
|---|---|---|---|
| Brute Force (Nested Loop) | O(n^2) | O(1) | Too slow for large inputs |
| Gauss Sum Formula | O(n) | O(1) | Clean and elegant |
| XOR Bit Manipulation | O(n) | O(1) | Optimal, overflow-safe |

**Recommended answer in an interview:** Mention the brute force first to show your thought process, then move to the Gauss Sum to demonstrate mathematical reasoning, and finally offer the XOR approach as an overflow-safe optimal solution. Walking through all three shows both depth and the ability to iteratively improve.