# Kth Missing Positive Number

`Amazon` • `Google` • `Meta` • `Microsoft` • `Apple` • `Bloomberg` • `Adobe` • `TikTok`

## Problem Statement

Given an array `arr` of positive integers sorted in **strictly increasing** order, and an integer `k`, return the `k`th **positive integer that is missing** from this array.

## Examples

**Example 1**

```ini
Input : arr = [2, 3, 4, 7, 11], k = 5
Output: 9

Missing numbers -> [1, 5, 6, 8, 9, 10, 12, 13, ...]
                            ^
                    the 5th missing number is 9
```

**Example 2**

```ini
Input : arr = [1, 2, 3, 4], k = 2
Output: 6

Missing numbers -> [5, 6, 7, ...]
                       ^
               the 2nd missing number is 6
```

## Constraints

- `1 <= arr.length <= 1000`
- `1 <= arr[i] <= 1000`
- `1 <= k <= 1000`
- `arr[i] < arr[j]` for `1 <= i < j <= arr.length`

<br><br>

## The One Formula To Remember

Before looking at any approach, lock this line in your head:

<mark>missing = arr[index] - (index + 1)</mark>

**Why does this work?**

- If **nothing** was missing, the array would simply be `[1, 2, 3, 4, 5, ...]`.
- In that perfect array, index `0` holds `1`, index `1` holds `2`, so index `i` holds `i + 1`.
- So `index + 1` is the value that **should** be sitting at that index.
- Every number that got skipped pushes the real value one step forward.
- So the gap between the real value and the expected value is exactly **how many numbers are missing before it**.

Quick check on `arr = [2, 3, 4, 7, 11]`:

```ini
index    :  0    1    2    3    4
arr[i]   :  2    3    4    7    11
should be:  1    2    3    4    5     (index + 1)
missing  :  1    1    1    3    6     (arr[i] - (index + 1))
```

Read the last row like this: before `7` sits at index `3`, exactly `3` positive numbers are missing (`1`, `5`, `6`).

<br><br>

## Approach 1: Brute Force (Linear Scan)

**Idea in plain words**

- Walk through the array from left to right, one index at a time.
- At each index compute `missing = arr[i] - (i + 1)`.
- If `missing < k`, the answer is still ahead of us, so we save a guess and keep moving.
- The guess is easy: we still need `k - missing` more missing numbers after `arr[i]`, and the numbers right after `arr[i]` are all fresh candidates, so the guess is `arr[i] + (k - missing)`.
- The moment `missing >= k`, we have gone **too far**. The guess we saved at the previous index is already the correct answer, so we stop.
- If the loop never crosses `k`, the guess built from the last element is the answer (the case where the missing number lies beyond the array).
- We start `ans = k`, which covers the case where we overshoot at index `0` itself (then `1, 2, 3, ...` are all missing, so the kth missing is just `k`).

**Code**

```python
class Solution:
    def findKthPositive(self, arr: List[int], k: int) -> int:
        ans = k

        for i in range(len(arr)):
            missing = arr[i] - (i + 1)

            if missing < k:
                ans = arr[i] + (k - missing)
            else:
                break

        return ans
```

**Dry Run** (`arr = [2, 3, 4, 7, 11]`, `k = 5`)

```ini
arr = [2, 3, 4, 7, 11]
k   = 5
ans = 5                       (default guess)

Iteration 1
  i         = 0
  arr[0]    = 2
  should be = 0 + 1 = 1
  missing   = 2 - 1 = 1
  1 < 5     -> answer is still ahead, save a guess
  still need= 5 - 1 = 4 more missing numbers
  ans       = 2 + 4 = 6

Iteration 2
  i         = 1
  arr[1]    = 3
  should be = 1 + 1 = 2
  missing   = 3 - 2 = 1
  1 < 5     -> answer is still ahead, save a guess
  still need= 5 - 1 = 4 more missing numbers
  ans       = 3 + 4 = 7

Iteration 3
  i         = 2
  arr[2]    = 4
  should be = 2 + 1 = 3
  missing   = 4 - 3 = 1
  1 < 5     -> answer is still ahead, save a guess
  still need= 5 - 1 = 4 more missing numbers
  ans       = 4 + 4 = 8

Iteration 4
  i         = 3
  arr[3]    = 7
  should be = 3 + 1 = 4
  missing   = 7 - 4 = 3
  3 < 5     -> answer is still ahead, save a guess
  still need= 5 - 3 = 2 more missing numbers
  ans       = 7 + 2 = 9

Iteration 5
  i         = 4
  arr[4]    = 11
  should be = 4 + 1 = 5
  missing   = 11 - 5 = 6
  6 >= 5    -> we have gone past the answer, stop
  break

Return ans = 9
```

**Complexity**

- Time: `O(n)` because we may touch every element once.
- Space: `O(1)`.

<br><br>

## Approach 2: Binary Search (Optimal)

**The key observation**

- As we move right, `missing` **never decreases** (the array is strictly increasing, so gaps only pile up).
- That means the `missing` values themselves form a sorted sequence: `1, 1, 1, 3, 6`.
- Anything sorted invites **binary search**.

**What are we searching for?**

- We want the **first index where `missing >= k`**, that is the exact point where the count of missing numbers finally reaches `k`.
- If `missing < k` at `mid`, we have not collected enough missing numbers yet, so go right (`low = mid + 1`).
- If `missing >= k` at `mid`, this index is already enough or too far, so go left (`high = mid - 1`) to look for an earlier one.

**Where do the pointers land?**

```ini
low  -> first index where missing >= k   (just past the answer)
high -> last  index where missing <  k   (just before the answer)
high = low - 1 always, once the loop ends
```

**Now the important part, where `low + k` comes from**

- `high` is the last index whose missing count is still smaller than `k`, so `arr[high]` sits just **before** the answer.
- At that point: `missing = arr[high] - (high + 1)`.
- We have `missing` numbers so far, so we still need `k - missing` more.
- Everything right after `arr[high]` is missing (that is exactly why the count jumps at the next index), so we just count forward from `arr[high]`:

```ini
ans = arr[high] + (k - missing)

substitute missing = arr[high] - (high + 1)

ans = arr[high] + k - (arr[high] - (high + 1))
ans = arr[high] + k - arr[high] + high + 1
ans = high + 1 + k

and since high = low - 1

ans = (low - 1) + 1 + k
ans = low + k
```

<mark>arr[high] cancels out completely, which is why the final line is just `return low + k`.</mark>

**Code**

```python
class Solution:
    def findKthPositive(self, arr: List[int], k: int) -> int:
        low = 0
        high = len(arr) - 1

        while low <= high:
            mid = (low + high) // 2
            missing = arr[mid] - (mid + 1)

            if missing < k:
                low = mid + 1
            else:
                high = mid - 1

        return low + k
```

**Dry Run** (`arr = [2, 3, 4, 7, 11]`, `k = 5`)

```ini
arr  = [2, 3, 4, 7, 11]
k    = 5
low  = 0
high = 4

Iteration 1
  low = 0, high = 4
  mid       = (0 + 4) // 2 = 2
  arr[2]    = 4
  should be = 2 + 1 = 3
  missing   = 4 - 3 = 1
  1 < 5     -> not enough missing numbers up to here
  go right  -> low = mid + 1 = 3

Iteration 2
  low = 3, high = 4
  mid       = (3 + 4) // 2 = 3
  arr[3]    = 7
  should be = 3 + 1 = 4
  missing   = 7 - 4 = 3
  3 < 5     -> still not enough
  go right  -> low = mid + 1 = 4

Iteration 3
  low = 4, high = 4
  mid       = (4 + 4) // 2 = 4
  arr[4]    = 11
  should be = 4 + 1 = 5
  missing   = 11 - 5 = 6
  6 >= 5    -> enough missing, this index may be too far
  go left   -> high = mid - 1 = 3

Loop ends because low = 4 > high = 3

  high = 3 -> last  index with missing < k   (arr[3] = 7,  missing = 3)
  low  = 4 -> first index with missing >= k  (arr[4] = 11, missing = 6)

Answer = low + k = 4 + 5 = 9

Cross check using the long formula:
  ans = arr[high] + (k - missing)
  ans = 7 + (5 - 3)
  ans = 9                       (same result)
```

**Edge case worth noting**

- If nothing is missing inside the array (for example `arr = [1, 2, 3, 4]`), `missing` stays `0` everywhere, so `low` walks all the way to `n`.
- The formula still holds: `ans = n + k = 4 + 2 = 6`, which is correct.

**Complexity**

- Time: `O(log n)` because the search space halves every step.
- Space: `O(1)`.

<br><br>

## Related Problems

- [Missing Number (268)](https://leetcode.com/problems/missing-number/)
- [First Missing Positive (41)](https://leetcode.com/problems/first-missing-positive/)
- [Missing Element in Sorted Array (1060)](https://leetcode.com/problems/missing-element-in-sorted-array/)
- [Missing Ranges (163)](https://leetcode.com/problems/missing-ranges/)
- [Search Insert Position (35)](https://leetcode.com/problems/search-insert-position/)
- [Single Element in a Sorted Array (540)](https://leetcode.com/problems/single-element-in-a-sorted-array/)
- [Find Smallest Letter Greater Than Target (744)](https://leetcode.com/problems/find-smallest-letter-greater-than-target/)