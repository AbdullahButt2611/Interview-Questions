# Aggressive Cows

`takeUforward` • `Google` • `Amazon` • `Adobe` • `PhonePe` • `Samsung`

<br>

## Problem Statement

You are given an array `nums` of size `n` holding stall positions on a straight line, and an integer `k`, the number of aggressive cows.

- Place all `k` cows in `k` different stalls.
- Cows fight, so we care about the smallest gap between any two neighbouring cows.
- Arrange them so that this smallest gap becomes as large as possible.

Return that maximum possible minimum distance.

## Examples

**Example 1**

```ini
Input  : n = 6, k = 4, nums = [0, 3, 4, 7, 10, 9]
Output : 3
```

Place cows at `[0, 3, 7, 10]`. Gaps are `3`, `4`, `3`, so the smallest gap is `3` and nothing better exists.

**Example 2**

```ini
Input  : n = 5, k = 2, nums = [4, 2, 1, 3, 6]
Output : 5
```

Place cows at `[1, 6]`. The only gap is `5`, which is the largest possible.

## Constraints

- `2 <= n <= 10^5`
- `0 <= nums[i] <= 10^9`
- `2 <= k <= n`

<br><br>

## Intuition

Instead of hunting for positions, guess the answer and verify it.

"Can I place `k` cows with every gap at least `5`?" is easy to answer with one left to right walk.

And the answers follow a clean pattern. If `5` works, every smaller value works. If `5` fails, every bigger value fails.

```ini
distance :  1     2     3     4     5     6     7     8     9    10
possible : YES   YES   YES    NO    NO    NO    NO    NO    NO    NO
                        ^ the last YES is our answer
```

<mark>A block of YES followed by a block of NO means we can binary search on the answer instead of testing every value.</mark>

<br><br>

## Approach

- Sort `nums` once, then set `low = 1` and `high = max(nums) - min(nums)`.
- Keep `dist` to remember the best working distance.
- While `low <= high`, take `mid = (low + high) // 2` and test if `mid` is achievable:
  - Place the first cow at `nums[0]`, so `cowsCount = 1` and `lastCow = nums[0]`.
  - Walk through the rest of the stalls.
  - If `nums[i] - lastCow >= mid`, place a cow here, bump `cowsCount` and move `lastCow` to `nums[i]`. Otherwise skip the stall.
  - Reaching `cowsCount == k` means possible. Finishing the walk without it means not possible.
- If possible, save `dist = mid` and go greedier with `low = mid + 1`.
- If not possible, the gap was too big, so `high = mid - 1`.
- When the loop ends, `dist` is the answer.

Grabbing the earliest valid stall is always safe, because pushing a cow further right only steals room from the cows behind it.

<br><br>

## Why These Choices

**Why `low = 1` ?**

All positions are distinct, so a real gap is never `0`. Anything below `1` can never be the answer.

**Why `high = max(nums) - min(nums)` ?**

Cows can only sit between the leftmost and rightmost stall, so no gap can beat that full span. For `[0, 3, 4, 7, 9, 10]` the span is `10`, so the answer lives in `[1 ... 10]`.

<mark>A tight upper bound also keeps the search short, since the number of rounds is log of this range.</mark>

**Why sort ?**

The check does `nums[i] - lastCow` and treats it as a gap. On the unsorted input, `9` sits after `10`, so `9 - 10 = -1`, which is not a real gap and quietly breaks the count. Sorting makes every subtraction a genuine forward distance.

**Why sort outside the loop ?**

The check runs once per binary search round. Sorting inside would repeat identical work every round. The array never changes, so one sort is enough.

<br><br>

## Code

```python
class Solution:
    def cowPlacementPossible(self, nums, k, checkDistance):
        cowsCount = 1
        lastCow = nums[0]

        for i in range(1, len(nums)):
            dist = nums[i] - lastCow

            if dist >= checkDistance:
                cowsCount += 1
                lastCow = nums[i]

                if cowsCount == k: return True
        
        return False


    def aggressiveCows(self, nums, k):
        low = 1
        high = max(nums) - min(nums)

        dist = float('inf')

        nums.sort()

        while low <= high:
            mid = (low + high) // 2

            if self.cowPlacementPossible(nums, k, mid):
                dist = mid
                low = mid + 1
            else:
                high = mid - 1
        
        return dist
```

<br><br>

## Dry Run

```ini
Input : nums = [0, 3, 4, 7, 10, 9], k = 4


SETUP
  low  = 1
  high = 10 - 0 = 10
  dist = infinity
  sorted nums -> [0, 3, 4, 7, 9, 10]
                  0  1  2  3  4   5     (indexes)


ITERATION 1
  low = 1, high = 10, mid = 5      -> gap of at least 5 ?

    cow 1 at 0                     cowsCount = 1, lastCow = 0
    i = 1 : 3 - 0  = 3  <  5       skip
    i = 2 : 4 - 0  = 4  <  5       skip
    i = 3 : 7 - 0  = 7  >= 5       place, cowsCount = 2, lastCow = 7
    i = 4 : 9 - 7  = 2  <  5       skip
    i = 5 : 10 - 7 = 3  <  5       skip

  cowsCount = 2, need 4            -> NOT possible
  too greedy, high = 5 - 1 = 4     dist still infinity


ITERATION 2
  low = 1, high = 4, mid = 2       -> gap of at least 2 ?

    cow 1 at 0                     cowsCount = 1, lastCow = 0
    i = 1 : 3 - 0  = 3  >= 2       place, cowsCount = 2, lastCow = 3
    i = 2 : 4 - 3  = 1  <  2       skip
    i = 3 : 7 - 3  = 4  >= 2       place, cowsCount = 3, lastCow = 7
    i = 4 : 9 - 7  = 2  >= 2       place, cowsCount = 4 = k, stop early

  possible, cows at [0, 3, 7, 9]   -> POSSIBLE
  save dist = 2, try bigger        low = 2 + 1 = 3


ITERATION 3
  low = 3, high = 4, mid = 3       -> gap of at least 3 ?

    cow 1 at 0                     cowsCount = 1, lastCow = 0
    i = 1 : 3 - 0  = 3  >= 3       place, cowsCount = 2, lastCow = 3
    i = 2 : 4 - 3  = 1  <  3       skip
    i = 3 : 7 - 3  = 4  >= 3       place, cowsCount = 3, lastCow = 7
    i = 4 : 9 - 7  = 2  <  3       skip
    i = 5 : 10 - 7 = 3  >= 3       place, cowsCount = 4 = k, stop early

  possible, cows at [0, 3, 7, 10]  -> POSSIBLE
  save dist = 3, try bigger        low = 3 + 1 = 4


ITERATION 4
  low = 4, high = 4, mid = 4       -> gap of at least 4 ?

    cow 1 at 0                     cowsCount = 1, lastCow = 0
    i = 1 : 3 - 0  = 3  <  4       skip
    i = 2 : 4 - 0  = 4  >= 4       place, cowsCount = 2, lastCow = 4
    i = 3 : 7 - 4  = 3  <  4       skip
    i = 4 : 9 - 4  = 5  >= 4       place, cowsCount = 3, lastCow = 9
    i = 5 : 10 - 9 = 1  <  4       skip

  cowsCount = 3, need 4            -> NOT possible
  high = 4 - 1 = 3


LOOP ENDS
  low = 4 > high = 3, so we stop

  Output : dist = 3
```

<br><br>

## Complexity Analysis

**Time : O(n log n + n log(max - min))**

Sorting costs `O(n log n)`. The binary search runs `log(max - min)` rounds, and each round walks all `n` stalls once.

**Space : O(1)**

Only a few variables, plus whatever the language sort uses internally.

<br><br>

## Related Problems

- [Magnetic Force Between Two Balls (1552)](https://leetcode.com/problems/magnetic-force-between-two-balls/)
- [Koko Eating Bananas (875)](https://leetcode.com/problems/koko-eating-bananas/)
- [Capacity To Ship Packages Within D Days (1011)](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/)
- [Split Array Largest Sum (410)](https://leetcode.com/problems/split-array-largest-sum/)
- [Minimum Number of Days to Make m Bouquets (1482)](https://leetcode.com/problems/minimum-number-of-days-to-make-m-bouquets/)
- [Find the Smallest Divisor Given a Threshold (1283)](https://leetcode.com/problems/find-the-smallest-divisor-given-a-threshold/)
- [Maximum Candies Allocated to K Children (2226)](https://leetcode.com/problems/maximum-candies-allocated-to-k-children/)
- [Minimize Max Distance to Gas Station (774)](https://leetcode.com/problems/minimize-max-distance-to-gas-station/)
- [Maximum Number of Removable Characters (1898)](https://leetcode.com/problems/maximum-number-of-removable-characters/)