# Koko Eating Bananas

`Amazon` • `Google` • `Microsoft` • `Apple` • `Meta`

## Problem Statement
Koko loves to eat bananas. There are `n` piles of bananas, and the `ith` pile has `piles[i]` bananas. The guards have gone and will come back in `h` hours.

- Koko picks an eating speed `k` (bananas per hour).
- Every hour, she chooses one pile and eats `k` bananas from it.
- If that pile has fewer than `k` bananas left, she eats all of them and then just waits for the rest of that hour (she does not move to another pile in the same hour).

Koko likes to eat slowly, but she still wants to finish every pile before the guards return.

Return the <mark>minimum integer `k`</mark> such that she can eat all the bananas within `h` hours.

## Examples
**Example 1:**
- Input: `piles = [3,6,7,11]`, `h = 8`
- Output: `4`

**Example 2:**
- Input: `piles = [30,11,23,4,20]`, `h = 5`
- Output: `30`

**Example 3:**
- Input: `piles = [30,11,23,4,20]`, `h = 6`
- Output: `23`

## Constraints
- `1 <= piles.length <= 10^4`
- `piles.length <= h <= 10^9`
- `1 <= piles[i] <= 10^9`

<br><br>

## Intuition (Explained Simply)
Think about the two extreme speeds first:

- **Slowest possible speed** is `1` banana per hour. This always finishes the bananas, but it might take too long.
- **Fastest useful speed** is `max(piles)`. At this speed, even the biggest pile is finished in exactly `1` hour, so a bigger speed is never needed.

So the answer always lives somewhere between `1` and `max(piles)`.

Now notice a very important pattern:

- If a speed `k` is **fast enough** to finish in time, then any speed **larger** than `k` is also fast enough.
- If a speed `k` is **too slow**, then any speed **smaller** than `k` is also too slow.

This "yes, yes, yes, ..., no, no, no" pattern is exactly what <mark>Binary Search</mark> loves. Instead of trying every speed from `1` upward (which is way too slow), we jump to the middle, check it, and throw away half the choices each time.

<br><br>

## Approach (Step by Step)
- Set `low = 1` and `high = max(piles)`.
- Pick the middle speed `mid`.
- Count how many hours Koko needs at speed `mid`.
  - For one pile, the hours needed is `ceil(pile / mid)` (round up, because a leftover part of a pile still costs a full hour).
  - Add this up for every pile to get `totalHours`.
- Compare `totalHours` with `h`:
  - If `totalHours <= h`, this speed works. Save it as a possible answer and try to go **slower** (move `high` left).
  - If `totalHours > h`, this speed is too slow, so go **faster** (move `low` right).
- Keep shrinking the range until `low` passes `high`. The last saved speed is the smallest one that works.

<br><br>

## Solution (Python)
```python
import math
from typing import List

class Solution:
    def calculateHours(self, bananas, piles):
        totalHours = 0

        for pile in piles:
            totalHours += math.ceil(pile / bananas)

        return totalHours

    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        low, high = 1, max(piles)
        ans = 1

        while low <= high:
            mid = (low + high) // 2
            totalHours = self.calculateHours(mid, piles)

            if totalHours <= h:
                high = mid - 1
                ans = mid
            else:
                low = mid + 1

        return ans
```

<br><br>

## Dry Run
Using `piles = [3,6,7,11]`, `h = 8`, so `max(piles) = 11`.

```ini
Start: low = 1, high = 11, ans = 1

Step 1: mid = (1 + 11) // 2 = 6
        hours = ceil(3/6) + ceil(6/6) + ceil(7/6) + ceil(11/6)
              = 1 + 1 + 2 + 2 = 6
        6 <= 8  ->  works, so ans = 6, high = 5

Step 2: mid = (1 + 5) // 2 = 3
        hours = ceil(3/3) + ceil(6/3) + ceil(7/3) + ceil(11/3)
              = 1 + 2 + 3 + 4 = 10
        10 > 8  ->  too slow, so low = 4

Step 3: mid = (4 + 5) // 2 = 4
        hours = ceil(3/4) + ceil(6/4) + ceil(7/4) + ceil(11/4)
              = 1 + 2 + 2 + 3 = 8
        8 <= 8  ->  works, so ans = 4, high = 3

Now low = 4 > high = 3, loop ends.

Answer = 4
```

<br><br>

## Complexity
- **Time:** `O(n * log(max(piles)))`, where `n` is the number of piles. We do a binary search over the speed range (the `log` part), and for each speed we scan all piles once (the `n` part).
- **Space:** `O(1)`, since we only use a few variables and no extra data structures.

<br><br>

## Related Problems
- [Capacity To Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/)
- [Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/)
- [Minimum Number of Days to Make m Bouquets](https://leetcode.com/problems/minimum-number-of-days-to-make-m-bouquets/)
- [Find the Smallest Divisor Given a Threshold](https://leetcode.com/problems/find-the-smallest-divisor-given-a-threshold/)
- [Minimum Time to Complete Trips](https://leetcode.com/problems/minimum-time-to-complete-trips/)
- [Magnetic Force Between Two Balls](https://leetcode.com/problems/magnetic-force-between-two-balls/)