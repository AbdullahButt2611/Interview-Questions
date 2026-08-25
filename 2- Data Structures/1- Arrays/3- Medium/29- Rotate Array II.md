# Rotate an Array by N Elements

`Amazon` • `Microsoft` • `Google` • `Netflix` • `Educative`

## Problem Statement
We are given an array of integers, `nums`. Rotate the array by `n` elements, where `n` is an integer:

- For a positive `n`, do a right rotation (the last elements wrap around to the front).
- For a negative `n`, do a left rotation (the first elements wrap around to the back).

<mark>The change must happen on the original array itself, not on a copy.</mark>

## Examples

**Example 1 (positive n, right rotation)**

```ini
Input:  nums = [1, 10, 20, 0, 59, 86, 32, 11, 9, 40],  n = 2
Output: [9, 40, 1, 10, 20, 0, 59, 86, 32, 11]
```

**Example 2 (negative n, left rotation)**

```ini
Input:  nums = [1, 2, 3, 4, 5],  n = -2
Output: [3, 4, 5, 1, 2]
```

## Constraints

- `1 <= len(nums) <= 10^5`
- `-2^31 <= nums[i] <= 2^31 - 1`
- `n` can be positive, negative, or larger than the array size.

<br><br>

## Approach 1: Rotate One Step at a Time (Brute Force)

The simplest way to think about it. A right rotation by 1 just means "pick up the last element, slide everyone else one spot to the right, and drop that element at the front." If we repeat that tiny move `n` times, the array ends up rotated by `n`.

**How it works**

- First, tidy up `n` so it is easy to work with. If `n` is bigger than the array, or if it is negative (a left rotation), the line `n = n % length` quietly turns it into a plain right rotation. For example, a left rotation of 11 on a 10 item array becomes a right rotation of 9.
- Then repeat `n` times: save the last element, shift every element one place to the right, and place the saved element at the front.

```python
def rotate_array(nums, n):
    length = len(nums)
    n = n % length  # turns a big or negative n into a simple right rotation

    for _ in range(n):
        last_element = nums[length - 1]
        for j in range(length - 1, 0, -1):
            nums[j] = nums[j - 1]
        nums[0] = last_element
    return nums
```

**Why we move on**

- We walk the whole array once for every single rotation.
- If `n` is large, that is a lot of repeated work, and the cost grows like `length * n` (close to `length^2` in the worst case).
- Time: `O(length * n)`, Space: `O(1)`. Too slow for big inputs.

<br><br>

## Approach 2: Use an Extra Array

Instead of nudging elements one by one, figure out where each element belongs and drop it straight there in a single pass. In a right rotation, the element at index `i` lands at index `(i + n) % length`.

**How it works**

- Tidy up `n` with `n = n % length`.
- Build a fresh array of the same size.
- For each `i`, copy `nums[i]` into `result[(i + n) % length]`.
- Copy `result` back into `nums`, so the original array is the one that changes.

```python
def rotate_array(nums, n):
    length = len(nums)
    n = n % length

    result = [0] * length
    for i in range(length):
        result[(i + n) % length] = nums[i]

    for i in range(length):   # copy back so the original array changes
        nums[i] = result[i]
    return nums
```

**Why we move on**

- It is fast because it only passes over the data a couple of times.
- But it needs a second array of the same size.
- <mark>The interviewer almost always follows up with "can you do it in place, without extra space?"</mark>
- Time: `O(length)`, Space: `O(length)`.

<br><br>

## Approach 3: Reversal Trick (Optimal)

This is the one to remember. Reversing pieces of the array hands us the rotation for free, and it needs no extra space at all.

The idea in three small moves:

- Reverse the whole array. Now the elements that belong at the front are already at the front, just in the wrong order.
- Reverse the first `n` elements to fix their order.
- Reverse the rest to fix their order too.

**How it works**

- Tidy up `n` with `n = n % length`.
- Reverse the entire array.
- Reverse the first `n` elements.
- Reverse the remaining elements.

```python
def rotate_array(nums, n):
    length = len(nums)
    n = n % length

    # 1) reverse the whole array
    start, end = 0, length - 1
    while start < end:
        nums[start], nums[end] = nums[end], nums[start]
        start += 1
        end -= 1

    # 2) reverse the first n elements
    start, end = 0, n - 1
    while start < end:
        nums[start], nums[end] = nums[end], nums[start]
        start += 1
        end -= 1

    # 3) reverse the remaining elements
    start, end = n, length - 1
    while start < end:
        nums[start], nums[end] = nums[end], nums[start]
        start += 1
        end -= 1

    return nums
```

**Why it wins**

- One clean pass over the data and zero extra arrays.
- Works for positive and negative `n` because the modulo step handles direction first.
- Time: `O(length)`, Space: `O(1)`.

<br><br>

## Dry Run

Walking through the optimal reversal approach so every swap is visible.

**Positive n (right rotation)**

```ini
Input:  nums = [1, 10, 20, 0, 59, 86, 32, 11, 9, 40],  n = 2

Step 0  Normalize n
  length = 10
  n = 2 % 10 = 2            (a plain right rotation by 2)

Step 1  Reverse the WHOLE array (indices 0 to 9)
  start=0, end=9  -> swap 1 and 40    -> [40, 10, 20, 0, 59, 86, 32, 11, 9, 1]
  start=1, end=8  -> swap 10 and 9    -> [40, 9, 20, 0, 59, 86, 32, 11, 10, 1]
  start=2, end=7  -> swap 20 and 11   -> [40, 9, 11, 0, 59, 86, 32, 20, 10, 1]
  start=3, end=6  -> swap 0 and 32    -> [40, 9, 11, 32, 59, 86, 0, 20, 10, 1]
  start=4, end=5  -> swap 59 and 86   -> [40, 9, 11, 32, 86, 59, 0, 20, 10, 1]
  start=5, end=4  -> start passed end, stop
  After Step 1:  [40, 9, 11, 32, 86, 59, 0, 20, 10, 1]

Step 2  Reverse the FIRST n=2 elements (indices 0 to 1)
  start=0, end=1  -> swap 40 and 9    -> [9, 40, 11, 32, 86, 59, 0, 20, 10, 1]
  start=1, end=0  -> stop
  After Step 2:  [9, 40, 11, 32, 86, 59, 0, 20, 10, 1]

Step 3  Reverse the REST (indices 2 to 9)
  start=2, end=9  -> swap 11 and 1    -> [9, 40, 1, 32, 86, 59, 0, 20, 10, 11]
  start=3, end=8  -> swap 32 and 10   -> [9, 40, 1, 10, 86, 59, 0, 20, 32, 11]
  start=4, end=7  -> swap 86 and 20   -> [9, 40, 1, 10, 20, 59, 0, 86, 32, 11]
  start=5, end=6  -> swap 59 and 0    -> [9, 40, 1, 10, 20, 0, 59, 86, 32, 11]
  start=6, end=5  -> stop
  After Step 3:  [9, 40, 1, 10, 20, 0, 59, 86, 32, 11]

Final Output:  [9, 40, 1, 10, 20, 0, 59, 86, 32, 11]   (matches expected)
```

**Negative n (left rotation)**

Here the direction is flipped for us before anything else happens by the single line `n = n % length`. In Python, the `%` operator always returns a result with the same sign as the divisor, and `length` is positive, so `n % length` is always a clean value between `0` and `length - 1`, even when `n` is negative. On top of that, a left rotation by `k` lands in the same place as a right rotation by `(length - k)`, which is exactly the value the modulo produces. For `n = -2` on a 5 item array, `-2 % 5 = 3`, so the code quietly does a right rotation by 3 and every step after that is identical.

```ini
Input:  nums = [1, 2, 3, 4, 5],  n = -2

Step 0  Normalize n
  length = 5
  n = -2 % 5 = 3           (left rotation by 2 becomes right rotation by 3)

Step 1  Reverse the WHOLE array (indices 0 to 4)
  start=0, end=4  -> swap 1 and 5     -> [5, 2, 3, 4, 1]
  start=1, end=3  -> swap 2 and 4     -> [5, 4, 3, 2, 1]
  start=2, end=2  -> start not < end, stop
  After Step 1:  [5, 4, 3, 2, 1]

Step 2  Reverse the FIRST n=3 elements (indices 0 to 2)
  start=0, end=2  -> swap 5 and 3     -> [3, 4, 5, 2, 1]
  start=1, end=1  -> stop
  After Step 2:  [3, 4, 5, 2, 1]

Step 3  Reverse the REST (indices 3 to 4)
  start=3, end=4  -> swap 2 and 1     -> [3, 4, 5, 1, 2]
  start=4, end=3  -> stop
  After Step 3:  [3, 4, 5, 1, 2]

Final Output:  [3, 4, 5, 1, 2]   (matches expected left rotation by 2)
```

<br><br>

## Related Problems

- [Rotate Array (189)](https://leetcode.com/problems/rotate-array/)
- [Rotate List (61)](https://leetcode.com/problems/rotate-list/)
- [Reverse String (344)](https://leetcode.com/problems/reverse-string/)
- [Reverse Words in a String (151)](https://leetcode.com/problems/reverse-words-in-a-string/)
- [Rotate Image (48)](https://leetcode.com/problems/rotate-image/)