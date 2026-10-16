# Reverse a Number (Ignoring Trailing Zeroes)

`TCS` • `Cognizant` • `Accenture` • `Wells Fargo` • `EY` • `Protium`

## Problem Statement

Given a non-negative integer `num`, return its **reverse**.

If the number has **trailing zeroes** (zeroes at the end), they must be **ignored** in the reversed number.

- For example, the reverse of `10400` is `401`, not `00401`.

## Examples

**Example 1:**

```ini
Input: num = 10400
Output: 401
Explanation: Reading 10400 backwards gives 00401. Zeroes at the front of a number carry no value, so the answer is 401.
```

**Example 2:**

```ini
Input: num = 12345
Output: 54321
Explanation: No trailing zeroes here, so every digit simply flips its position.
```

**Example 3:**

```ini
Input: num = 1000
Output: 1
Explanation: Reading 1000 backwards gives 0001, which is just 1.
```

## Constraints

- `num` is a non-negative integer (`num >= 0`).

<br><br>

## Approach

### The One Rule to Remember

<mark>Peel digits off the back of the old number, and stack them onto the back of the new number.</mark>

- The **last** digit of the old number becomes the **first** digit of the new number.
- Keep doing this until the old number runs out of digits.

### The Three Tiny Tools

You only need three simple math moves. No strings, no lists.

- **Grab the last digit:** `num % 10`
  - `% 10` gives the remainder after dividing by 10, which is always the last digit.
  - Example: `10400 % 10 = 0`, `104 % 10 = 4`.
- **Chop off the last digit:** `num // 10`
  - `// 10` divides by 10 and drops the decimal, so the last digit falls off.
  - Example: `10400 // 10 = 1040`.
- **Push a digit onto the end of the new number:** `reverse_num * 10 + last_digit`
  - `* 10` shifts every digit one place to the left, making an empty spot at the end.
  - `+ last_digit` drops the new digit into that empty spot.
  - Example: `40 * 10 + 1 = 401`.

### Why Trailing Zeroes Disappear on Their Own

This is the best part: <mark>we do not need any special code for the zeroes</mark>.

- The trailing zeroes are the **first** digits we grab, so they land at the **front** of the new number.
- But `0 * 10 + 0` is still `0`.
- So while only zeroes have been pushed, `reverse_num` just stays `0`. They never show up.
- This is the same reason nobody writes `00401`. Zeroes in front of a number are worth nothing.

### Step by Step

1. **Get ready.**
   - Start `reverse_num` at `0`. This is the empty new number.
2. **Loop while `num > 0`.** (While the old number still has digits.)
   - **Grab** the last digit: `last_digit = num % 10`.
   - **Chop** it off the old number: `num = num // 10`.
   - **Push** it onto the new number: `reverse_num = reverse_num * 10 + last_digit`.
3. **Done.**
   - When `num` becomes `0`, every digit has moved over. `reverse_num` is the answer.

> If `num` starts as `0`, the loop never runs and `reverse_num` stays `0`, which is the correct answer.

> Memory hook: <mark>"Grab the last, chop the last, push it in. Repeat until nothing is left."</mark>

<br><br>

## Solution

```python
num = 10400
reverse_num = 0
while num > 0:
    last_digit = num % 10
    num = num // 10
    reverse_num = (reverse_num * 10) + last_digit
```

<br><br>

## Dry Run

```ini
=====================================================
SCENARIO A: num = 10400  (has trailing zeroes)
=====================================================

Setup:
  num         = 10400
  reverse_num = 0

Iteration 1:
  Loop check: num = 10400 > 0. Enter loop.
  Grab:  last_digit  = 10400 % 10 = 0
  Chop:  num         = 10400 // 10 = 1040
  Push:  reverse_num = (0 * 10) + 0 = 0 + 0 = 0
  (A trailing zero was pushed, but 0 stays 0. It is invisible.)

Iteration 2:
  Loop check: num = 1040 > 0. Enter loop.
  Grab:  last_digit  = 1040 % 10 = 0
  Chop:  num         = 1040 // 10 = 104
  Push:  reverse_num = (0 * 10) + 0 = 0 + 0 = 0
  (Second trailing zero, still invisible.)

Iteration 3:
  Loop check: num = 104 > 0. Enter loop.
  Grab:  last_digit  = 104 % 10 = 4
  Chop:  num         = 104 // 10 = 10
  Push:  reverse_num = (0 * 10) + 4 = 0 + 4 = 4
  (First real digit. The new number finally starts.)

Iteration 4:
  Loop check: num = 10 > 0. Enter loop.
  Grab:  last_digit  = 10 % 10 = 0
  Chop:  num         = 10 // 10 = 1
  Push:  reverse_num = (4 * 10) + 0 = 40 + 0 = 40
  (This zero is in the MIDDLE, so it is kept. 4 shifts left, 0 fills the end.)

Iteration 5:
  Loop check: num = 1 > 0. Enter loop.
  Grab:  last_digit  = 1 % 10 = 1
  Chop:  num         = 1 // 10 = 0
  Push:  reverse_num = (40 * 10) + 1 = 400 + 1 = 401

Iteration 6:
  Loop check: num = 0. Condition 0 > 0 is False. Exit loop.

Summary of digits grabbed: 0 → 0 → 4 → 0 → 1
The first two zeroes stayed invisible. The middle zero was kept.

reverse_num = 401
Output: 401  ✓


=====================================================
SCENARIO B: num = 12345  (no zeroes at all)
=====================================================

Setup:
  num         = 12345
  reverse_num = 0

Iteration 1:
  Loop check: num = 12345 > 0. Enter loop.
  Grab:  last_digit  = 12345 % 10 = 5
  Chop:  num         = 12345 // 10 = 1234
  Push:  reverse_num = (0 * 10) + 5 = 0 + 5 = 5

Iteration 2:
  Loop check: num = 1234 > 0. Enter loop.
  Grab:  last_digit  = 1234 % 10 = 4
  Chop:  num         = 1234 // 10 = 123
  Push:  reverse_num = (5 * 10) + 4 = 50 + 4 = 54

Iteration 3:
  Loop check: num = 123 > 0. Enter loop.
  Grab:  last_digit  = 123 % 10 = 3
  Chop:  num         = 123 // 10 = 12
  Push:  reverse_num = (54 * 10) + 3 = 540 + 3 = 543

Iteration 4:
  Loop check: num = 12 > 0. Enter loop.
  Grab:  last_digit  = 12 % 10 = 2
  Chop:  num         = 12 // 10 = 1
  Push:  reverse_num = (543 * 10) + 2 = 5430 + 2 = 5432

Iteration 5:
  Loop check: num = 1 > 0. Enter loop.
  Grab:  last_digit  = 1 % 10 = 1
  Chop:  num         = 1 // 10 = 0
  Push:  reverse_num = (5432 * 10) + 1 = 54320 + 1 = 54321

Iteration 6:
  Loop check: num = 0. Condition 0 > 0 is False. Exit loop.

Watch the two numbers trade digits:
  Old number shrinks:  12345 → 1234 → 123 → 12 → 1 → 0
  New number grows:    0     → 5    → 54  → 543 → 5432 → 54321

reverse_num = 54321
Output: 54321  ✓


=====================================================
SCENARIO C: num = 1000  (only one real digit)
=====================================================

Setup:
  num         = 1000
  reverse_num = 0

Iteration 1:
  Loop check: num = 1000 > 0. Enter loop.
  Grab:  last_digit  = 1000 % 10 = 0
  Chop:  num         = 1000 // 10 = 100
  Push:  reverse_num = (0 * 10) + 0 = 0

Iteration 2:
  Loop check: num = 100 > 0. Enter loop.
  Grab:  last_digit  = 100 % 10 = 0
  Chop:  num         = 100 // 10 = 10
  Push:  reverse_num = (0 * 10) + 0 = 0

Iteration 3:
  Loop check: num = 10 > 0. Enter loop.
  Grab:  last_digit  = 10 % 10 = 0
  Chop:  num         = 10 // 10 = 1
  Push:  reverse_num = (0 * 10) + 0 = 0

Iteration 4:
  Loop check: num = 1 > 0. Enter loop.
  Grab:  last_digit  = 1 % 10 = 1
  Chop:  num         = 1 // 10 = 0
  Push:  reverse_num = (0 * 10) + 1 = 0 + 1 = 1

Iteration 5:
  Loop check: num = 0. Condition 0 > 0 is False. Exit loop.

All three trailing zeroes were pushed first, and all three stayed invisible.

reverse_num = 1
Output: 1  ✓


=====================================================
SCENARIO D: num = 0  (edge case)
=====================================================

Setup:
  num         = 0
  reverse_num = 0

Iteration 1:
  Loop check: num = 0. Condition 0 > 0 is False.
  The loop never runs.

Note: reverse_num already starts at 0, and the reverse of 0 is 0.
So no special check is needed.

reverse_num = 0
Output: 0  ✓
```

<br><br>

## Complexity Analysis

- **Time Complexity:** `O(D)`, where `D` is the number of digits in `num`.
  - Each loop run removes exactly one digit.
  - Since `D` is about `log10(num)`, this is the same as `O(log N)`.
  - Even a 10 digit number needs only 10 loop runs.
- **Space Complexity:** `O(1)`.
  - Only three variables (`num`, `reverse_num`, `last_digit`) are used.
  - No strings, lists, or recursion.

<br><br>

## Related Problems

- [Reverse Integer (7)](https://leetcode.com/problems/reverse-integer/)
- [Palindrome Number (9)](https://leetcode.com/problems/palindrome-number/)
- [Reverse Bits (190)](https://leetcode.com/problems/reverse-bits/)
- [Happy Number (202)](https://leetcode.com/problems/happy-number/)
- [Add Digits (258)](https://leetcode.com/problems/add-digits/)
- [Subtract the Product and Sum of Digits of an Integer (1281)](https://leetcode.com/problems/subtract-the-product-and-sum-of-digits-of-an-integer/)
- [Count Nice Pairs in an Array (1814)](https://leetcode.com/problems/count-nice-pairs-in-an-array/)
- [Sum of Digits in Base K (1837)](https://leetcode.com/problems/sum-of-digits-in-base-k/)
- [A Number After a Double Reversal (2119)](https://leetcode.com/problems/a-number-after-a-double-reversal/)
- [Count Number of Distinct Integers After Reverse Operations (2442)](https://leetcode.com/problems/count-number-of-distinct-integers-after-reverse-operations/)
