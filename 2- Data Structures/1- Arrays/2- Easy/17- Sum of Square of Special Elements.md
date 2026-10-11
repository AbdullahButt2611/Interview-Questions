# Sum of Squares of Special Elements

`Educative`

## Problem Statement

You are given a **1-indexed** integer array `nums` of length `n`.

An element `nums[i]` of `nums` is called **special** if `i` divides `n`, i.e. `n % i == 0`.

Return the **sum of the squares** of all **special** elements of `nums`.

## Examples

**Example 1:**

```ini
Input: nums = [1,2,3,4]
Output: 21
Explanation: There are exactly 3 special elements in nums: nums[1] since 1 divides 4, nums[2] since 2 divides 4, and nums[4] since 4 divides 4.
Hence, the sum of the squares of all special elements of nums is nums[1] * nums[1] + nums[2] * nums[2] + nums[4] * nums[4] = 1 * 1 + 2 * 2 + 4 * 4 = 21.
```

**Example 2:**

```ini
Input: nums = [2,7,1,19,18,3]
Output: 63
Explanation: There are exactly 4 special elements in nums: nums[1] since 1 divides 6, nums[2] since 2 divides 6, nums[3] since 3 divides 6, and nums[6] since 6 divides 6.
Hence, the sum of the squares of all special elements of nums is nums[1] * nums[1] + nums[2] * nums[2] + nums[3] * nums[3] + nums[6] * nums[6] = 2 * 2 + 7 * 7 + 1 * 1 + 3 * 3 = 63.
```

## Constraints

- `1 <= nums.length == n <= 50`
- `1 <= nums[i] <= 50`

<br><br>

## Approach

### The One Rule to Remember

An element is special when <mark>its position fits perfectly into the length of the array</mark>.

- "Fits perfectly" means **no remainder**: `n % position == 0`.
- Example: in an array of length `6`, positions `1, 2, 3, 6` fit perfectly. Positions `4` and `5` leave a remainder, so they do not.

### The One Trap to Avoid

The problem counts positions starting from **1**, but Python counts from **0**.

- Python index `0` is position `1`.
- Python index `1` is position `2`, and so on.
- So before checking, always **add 1** to the Python index to get the real position.

> If you forget the `+1`, you would compute `n % 0` on the very first element and crash.

### Step by Step

1. **Get ready.**
   - Store the length of the array in `n`.
   - Start a running total `indexed_sum` at `0`.
2. **Walk through the array, one element at a time.**
   - For each element, take its Python index `i` and its value `num`.
3. **Fix the position.**
   - Add 1 to `i`, so it matches the problem's 1-indexed position.
4. **Check if it is special.**
   - Does the position divide `n` with no remainder (`n % i == 0`)?
   - **Yes:** square the value (`num * num`) and add it to `indexed_sum`.
   - **No:** skip it and move on.
5. **Done walking?**
   - Return `indexed_sum`.

> Memory hook: <mark>"Shift by one, check the fit, square and add."</mark>

<br><br>

## Solution

```python
class Solution:
    def sumOfSquares(self, nums: List[int]) -> int:
        n = len(nums)
        indexed_sum = 0
        for i, num in enumerate(nums):
            i += 1
            if n % i == 0:
                indexed_sum += num * num
        return indexed_sum
```

<br><br>

## Dry Run

```ini
=====================================================
SCENARIO A: nums = [1,2,3,4]
=====================================================

Setup:
  n           = 4
  indexed_sum = 0

Iteration 1:
  Python index i = 0, num = 1
  Fix the position: i = 0 + 1 = 1
  Is it special? n % i = 4 % 1 = 0. YES, 1 fits perfectly into 4.
  Square it: 1 * 1 = 1
  indexed_sum = 0 + 1 = 1

Iteration 2:
  Python index i = 1, num = 2
  Fix the position: i = 1 + 1 = 2
  Is it special? n % i = 4 % 2 = 0. YES, 2 fits perfectly into 4.
  Square it: 2 * 2 = 4
  indexed_sum = 1 + 4 = 5

Iteration 3:
  Python index i = 2, num = 3
  Fix the position: i = 2 + 1 = 3
  Is it special? n % i = 4 % 3 = 1. NO, remainder is 1.
  Skip this element.
  indexed_sum = 5 (unchanged)

Iteration 4:
  Python index i = 3, num = 4
  Fix the position: i = 3 + 1 = 4
  Is it special? n % i = 4 % 4 = 0. YES, 4 fits perfectly into 4.
  Square it: 4 * 4 = 16
  indexed_sum = 5 + 16 = 21

Loop finished. All 4 elements checked.

Special positions found: 1, 2, 4
Calculation: 1 + 4 + 16 = 21

Return indexed_sum = 21
Output: 21  ✓


=====================================================
SCENARIO B: nums = [2,7,1,19,18,3]
=====================================================

Setup:
  n           = 6
  indexed_sum = 0

Iteration 1:
  Python index i = 0, num = 2
  Fix the position: i = 0 + 1 = 1
  Is it special? n % i = 6 % 1 = 0. YES, 1 fits perfectly into 6.
  Square it: 2 * 2 = 4
  indexed_sum = 0 + 4 = 4

Iteration 2:
  Python index i = 1, num = 7
  Fix the position: i = 1 + 1 = 2
  Is it special? n % i = 6 % 2 = 0. YES, 2 fits perfectly into 6.
  Square it: 7 * 7 = 49
  indexed_sum = 4 + 49 = 53

Iteration 3:
  Python index i = 2, num = 1
  Fix the position: i = 2 + 1 = 3
  Is it special? n % i = 6 % 3 = 0. YES, 3 fits perfectly into 6.
  Square it: 1 * 1 = 1
  indexed_sum = 53 + 1 = 54

Iteration 4:
  Python index i = 3, num = 19
  Fix the position: i = 3 + 1 = 4
  Is it special? n % i = 6 % 4 = 2. NO, remainder is 2.
  Skip this element.
  indexed_sum = 54 (unchanged)

Iteration 5:
  Python index i = 4, num = 18
  Fix the position: i = 4 + 1 = 5
  Is it special? n % i = 6 % 5 = 1. NO, remainder is 1.
  Skip this element.
  indexed_sum = 54 (unchanged)

Iteration 6:
  Python index i = 5, num = 3
  Fix the position: i = 5 + 1 = 6
  Is it special? n % i = 6 % 6 = 0. YES, 6 fits perfectly into 6.
  Square it: 3 * 3 = 9
  indexed_sum = 54 + 9 = 63

Loop finished. All 6 elements checked.

Special positions found: 1, 2, 3, 6
Calculation: 4 + 49 + 1 + 9 = 63

Return indexed_sum = 63
Output: 63  ✓


=====================================================
SCENARIO C: nums = [7]  (single element)
=====================================================

Setup:
  n           = 1
  indexed_sum = 0

Iteration 1:
  Python index i = 0, num = 7
  Fix the position: i = 0 + 1 = 1
  Is it special? n % i = 1 % 1 = 0. YES, 1 fits perfectly into 1.
  Square it: 7 * 7 = 49
  indexed_sum = 0 + 49 = 49

Loop finished. All 1 element checked.

Note: Position 1 always divides any n, so the first element is ALWAYS special.
The same goes for the last element (position n always divides n).

Return indexed_sum = 49
Output: 49  ✓
```

<br><br>

## Complexity Analysis

- **Time Complexity:** `O(N)`, where `N` is the length of `nums`.
  - We visit every element exactly once.
  - Each visit does a constant amount of work (one `%`, maybe one multiply and one add).
- **Space Complexity:** `O(1)`.
  - Only a few variables (`n`, `indexed_sum`, `i`, `num`) are used.
  - No extra list or data structure is created.

<br><br>

## Related Problems

- [Squares of a Sorted Array (977)](https://leetcode.com/problems/squares-of-a-sorted-array/)
- [Sum of Square Numbers (633)](https://leetcode.com/problems/sum-of-square-numbers/)
- [The kth Factor of n (1492)](https://leetcode.com/problems/the-kth-factor-of-n/)
- [Sum of Unique Elements (1748)](https://leetcode.com/problems/sum-of-unique-elements/)
- [Three Divisors (1952)](https://leetcode.com/problems/three-divisors/)
- [Smallest Even Multiple (2413)](https://leetcode.com/problems/smallest-even-multiple/)
- [Count the Digits That Divide a Number (2520)](https://leetcode.com/problems/count-the-digits-that-divide-a-number/)
- [Sum of Values at Indices With K Set Bits (2859)](https://leetcode.com/problems/sum-of-values-at-indices-with-k-set-bits/)