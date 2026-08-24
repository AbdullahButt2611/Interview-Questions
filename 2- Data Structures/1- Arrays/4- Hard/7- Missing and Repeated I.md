# Repeating and Missing Number I

`Amazon` • `GeeksforGeeks` • `Naukri Code 360`
<br>
## Problem Statement

You are given an integer array `nums` of size `n` containing values from `1` to `n`.

Each value should appear exactly once, but:

- One number, call it **A**, appears **twice**
- One number, call it **B**, is **missing** from the array

Find and return `A` and `B` as an array of size 2, where `A` is at index 0 and `B` is at index 1.

**Note:** You are not allowed to modify the original array.

### Example 1

```
Input: nums = [3, 5, 4, 1, 1]
Output: [1, 2]
```

Explanation: 1 appears two times in the array and 2 is missing from nums.

### Example 2

```
Input: nums = [1, 2, 3, 6, 7, 5, 7]
Output: [7, 4]
```

Explanation: 7 appears two times in the array and 4 is missing from nums.

### Constraints

- `n == nums.length`
- `1 <= n <= 10^5`
- `n - 2` elements in nums appear exactly once and are valued between `[1, n]`
- 1 element appears twice, and is valued between `[1, n]`

## Approach 1: Brute Force (Count Each Number)

### Idea

- For every number `i` from `1` to `n`, count how many times it shows up in the array.
- If the count is `2`, that number is `A` (the repeating one).
- If the count is `0`, that number is `B` (the missing one).
- Stop as soon as both are found.

### Code

```python
class Solution:
    def findMissingRepeatingNumbers(self, nums):
        n = len(nums)
        repeating, missing = -1, -1

        for i in range(1, n + 1):
            count = 0
            for num in nums:
                if num == i:
                    count += 1
            if count == 2:
                repeating = i
            elif count == 0:
                missing = i
            if repeating != -1 and missing != -1:
                break

        return [repeating, missing]
```

### Dry Run

`nums = [3, 5, 4, 1, 1]`, `n = 5`

- `i = 1` → appears twice → `repeating = 1`
- `i = 2` → appears zero times → `missing = 2`
- Both found, stop loop.
- Output: `[1, 2]`

### What's the Problem Here?

- For every number from `1` to `n`, we scan the whole array again.
- This is `n` numbers times `n` array scans, so the work grows very fast as `n` increases.
- Time Complexity: `O(n^2)`
- Space Complexity: `O(1)`

This is too slow for large inputs (n up to 10^5 means up to 10 billion operations).

<br>

## Approach 2: Hashing using an Array

### Idea

- Create a new array called `freq` of size `n + 1`, filled with zeros.
- Go through `nums` once, and for every number, increase its count in `freq`.
- Now go through `freq` from index `1` to `n`:
  - If `freq[i] == 2`, that index is `A`.
  - If `freq[i] == 0`, that index is `B`.

### Code

```python
class Solution:
    def findMissingRepeatingNumbers(self, nums):
        n = len(nums)
        freq = [0] * (n + 1)

        for num in nums:
            freq[num] += 1

        repeating, missing = -1, -1
        for i in range(1, n + 1):
            if freq[i] == 2:
                repeating = i
            elif freq[i] == 0:
                missing = i

        return [repeating, missing]
```

### Dry Run

`nums = [3, 5, 4, 1, 1]`, `n = 5`

- Build `freq` (index 0 to 5): start as `[0, 0, 0, 0, 0, 0]`
- After counting: `freq = [0, 2, 0, 1, 1, 1]`
  (index 1 has count 2, index 2 has count 0)
- Scan `freq` from index 1 to 5:
  - index 1, count 2 → `repeating = 1`
  - index 2, count 0 → `missing = 2`
- Output: `[1, 2]`

### What's Better Here?

- We only go through the array twice (once to build `freq`, once to read it), instead of `n` times.
- Time Complexity: `O(n)`, much faster than before.

### What's the Problem Here?

- We used an extra array of size `n + 1` just to store counts.
- Space Complexity: `O(n)`, this uses extra memory that grows with input size.
- Can we solve this using only a constant amount of extra space? Yes, with math.

<br>

## Approach 3: Mathematical Formula (Optimal)

### Idea

This approach uses two simple facts about numbers from `1` to `n`:

- The sum of numbers from `1` to `n` should be `n * (n + 1) / 2`
- The sum of squares of numbers from `1` to `n` should be `n * (n + 1) * (2n + 1) / 6`

Because one number `B` is missing and another number `A` is repeated, the actual sum and actual sum of squares of `nums` will not match these expected values. We use that difference to find `A` and `B`.

(Curious where these two formulas come from? Check the "Where Do These Formulas Come From" section at the end of this file.)

### Mathematical Steps

We will use one example throughout: `nums = [3, 5, 4, 1, 1]`, `n = 5`, where `A = 1` (repeated) and `B = 2` (missing).

```
GIVEN
  nums = [3, 5, 4, 1, 1]
  n    = 5

STEP 1: Get the actual sum, and the expected sum
  S  = sum of nums            = 3 + 5 + 4 + 1 + 1   = 14
  Sn = n * (n + 1) / 2         = 5 * 6 / 2            = 15

STEP 2: eq1 = S - Sn
  Since nums has an extra A and is missing a B,
  every other number cancels out, leaving:
      S - Sn = A - B

  Here's why, written out term by term:

      nums = {1, 1, 3, 4, 5}     (A = 1 appears twice)
      1..n = {1, 2, 3, 4, 5}     (B = 2 appears once, A = 1 appears once)

      S - Sn = (1 + 1 + 3 + 4 + 5) - (1 + 2 + 3 + 4 + 5)

      Numbers 3, 4, 5 are present on both sides, so they cancel:
            (1 + 1 + ̶3̶ + ̶4̶ + ̶5̶) - (1 + 2 + ̶3̶ + ̶4̶ + ̶5̶)
          = (1 + 1) - (1 + 2)

      One copy of "1" is also common to both sides, so it cancels too:
            (̶1̶ + 1) - (̶1̶ + 2)
          = 1 - 2

      What's left is just the extra copy of A on the nums side,
      and the missing B on the 1..n side:
          = A - B
          = 1 - 2 = -1

  eq1 = 14 - 15 = -1
  → A - B = -1


STEP 3: Get the actual sum of squares, and the expected sum of squares
  S2  = sum of squares of nums = 9 + 25 + 16 + 1 + 1  = 52
  S2n = n*(n+1)*(2n+1) / 6      = 5*6*11 / 6            = 55

STEP 4: eq2 = (S2 - S2n) / eq1
  Same logic as Step 2, but with squares:
      S2 - S2n = A^2 - B^2 = (A - B)(A + B)
  Since (A - B) is already known as eq1, divide it out:
      eq2 = (S2 - S2n) / eq1
  eq2 = (52 - 55) / -1 = -3 / -1 = 3
  → A + B = 3

STEP 5: A = (eq1 + eq2) / 2
  Adding eq1 and eq2 cancels out B:
      eq1 + eq2 = (A - B) + (A + B) = 2A
  A = (-1 + 3) / 2 = 2 / 2 = 1

STEP 6: B = A - eq1
  B = 1 - (-1) = 2

ANSWER
  [A, B] = [1, 2]
```

### Code

```python
class Solution:
    def findMissingRepeatingNumbers(self, nums):
        n = len(nums)

        sum_of_n = (n * (n + 1)) // 2
        sum_of_sqr_of_n = (n * (n + 1) * (2 * n + 1)) // 6

        sum_of_num = 0
        sum_of_sqr_of_num = 0

        for num in nums:
            sum_of_num += num
            sum_of_sqr_of_num += num * num

        eq1 = sum_of_num - sum_of_n                  # A - B

        eq2 = sum_of_sqr_of_num - sum_of_sqr_of_n     # (A - B)(A + B)
        eq2 = eq2 // eq1                              # A + B

        A = (eq1 + eq2) // 2                          # 2A = eq1 + eq2
        B = A - eq1

        return [A, B]
```

### Dry Run

We already walked through the full example `nums = [3, 5, 4, 1, 1]` step by step above (in the "Mathematical Steps" section), arriving at `eq1 = -1`, `eq2 = 3`, `A = 1`, and `B = 2`.

Running the code above on this same input produces:

**Output: `[1, 2]`**

This matches the expected output exactly.

### Why This Is Better

- We only go through the array once, to calculate `sum_of_num` and `sum_of_sqr_of_num`.
- We don't use any extra array, only a few variables.
- Time Complexity: `O(n)`
- Space Complexity: `O(1)`

This is the most optimal solution among the three.

<br>

## Comparison of All Approaches

| Approach | Time Complexity | Space Complexity |
|---|---|---|
| Brute Force | O(n^2) | O(1) |
| Hashing | O(n) | O(n) |
| Mathematical Formula | O(n) | O(1) |

## Related Problems

- Find Missing and Repeated Values (LeetCode 2965, the 2D matrix version of this same idea)
- Set Mismatch (LeetCode 645)
- Missing Number (LeetCode 268)
- First Missing Positive (LeetCode 41)
- Find All Numbers Disappeared in an Array (LeetCode 448)

<br>

## Where Do These Formulas Come From

- `n * (n + 1) / 2` is the standard formula for the sum of the first `n` natural numbers. For example, if `n = 5`, the sum of `1 + 2 + 3 + 4 + 5` equals `5 * 6 / 2 = 15`.
- `n * (n + 1) * (2n + 1) / 6` is the standard formula for the sum of the squares of the first `n` natural numbers. For example, if `n = 5`, the sum of `1^2 + 2^2 + 3^2 + 4^2 + 5^2` equals `5 * 6 * 11 / 6 = 55`.
- Both are well known mathematical identities, so we don't need to loop through `1` to `n` to calculate them. We just plug `n` into the formula directly.