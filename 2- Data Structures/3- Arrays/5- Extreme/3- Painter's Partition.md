# Painter's Partition

`Google` • `Amazon` • `Microsoft` • `Facebook` • `Oracle` • `takeUforward`

## Problem Statement

You are given `A` painters and an array `C` of `N` integers, where `C[i]` is the length of the ith board. Each painter needs `B` units of time to paint 1 unit of board.

You have to assign boards to painters with these rules:

- Each painter paints only a contiguous block of boards (they cannot skip around).
- A single board cannot be split between two painters.
- You want to finish painting everything as fast as possible.

All painters work at the same time, so the total time equals the time taken by the busiest painter. The goal is to split the boards so that this busiest painter finishes as early as possible.

Return that minimum time, taken modulo `10000003`.

## Examples

**Example 1**

```ini
Input:  A = 2, B = 5, C = [1, 10]
Output: 50

Painter 1 paints board 0 (length 1)  -> time = 1 * 5 = 5
Painter 2 paints board 1 (length 10) -> time = 10 * 5 = 50
Busiest painter = 50
50 % 10000003 = 50
```

**Example 2**

```ini
Input:  A = 10, B = 1, C = [1, 8, 11, 3]
Output: 11

Enough painters exist, so give one board to each painter.
Busiest painter = max(1, 8, 11, 3) = 11
11 % 10000003 = 11
```

## Constraints

- `1 <= A <= 1000`
- `1 <= B <= 10^6`
- `1 <= N <= 10^5`
- `1 <= C[i] <= 10^6`

<br><br>

## Approach

Trying every possible split is too slow, so instead we **guess the final time and check if it is possible**. This flips a hard "how to split" question into an easy "yes or no" question.

**Why we search on length, not time**

Time is always `length * B`, and `B` is fixed for everyone. So the painter with the most length is also the one with the most time. We can find the best length first, then multiply by `B` at the very end. This keeps the numbers small and simple.

**Why the answer sits in `[max(C), sum(C)]`**

- The busiest painter can never do less than `max(C)`, because one painter has to paint the biggest board fully (boards cannot be split). So the answer cannot go below this.
- The busiest painter can never do more than `sum(C)`, because that only happens if a single painter paints everything. So the answer cannot go above this.

<mark>The answer is trapped inside `[max(C), sum(C)]`, and this range is sorted, which is exactly why binary search works here.</mark>

**Why we pick a `mid` and count painters**

- We take the middle value `mid` and treat it as a limit: "no painter may hold more than `mid` length." We test the middle so that each check throws away half the range, which is what makes it fast.
- To test `mid`, we give the current painter as much as possible and only start a new painter when the next board would cross `mid`. We fill each painter to the limit because that uses the fewest painters possible, so if even this cannot fit in `A` painters, nothing can.

**Why we move `low` and `high` the way we do**

- If painters needed `<= A`, then `mid` is doable. But maybe an even smaller time also works, so we save `mid` and search the lower half (`high = mid - 1`) to hunt for something better.
- If painters needed `> A`, then `mid` is too strict to finish with `A` painters. A smaller limit would need even more painters, so it is pointless to look lower. We search the upper half (`low = mid + 1`).

**Why the final two operations**

When the loop ends, `ans` holds the smallest length that `A` painters can handle. We multiply by `B` to turn that length into actual time, then take `% 10000003` because the problem asks for the answer under that modulo.

<br><br>

## Code

```python
class Solution:
    def totalPainters(self, painters, lengths, minLength):
        currPainters = 1
        currLength = lengths[0]

        for i in range(1, len(lengths)):
            if currLength + lengths[i] > minLength:
                currPainters += 1
                currLength = lengths[i]
            else:
                currLength += lengths[i]

        return currPainters

    def paint(self, A: int, B: int, C: list[int]) -> int:
        low = max(C)
        high = sum(C)
        ans = -1

        while low <= high:
            mid = (low + high) // 2

            if self.totalPainters(A, C, mid) <= A:
                high = mid - 1
                ans = mid
            else:
                low = mid + 1

        ans *= B
        return ans % 10000003
```

<br><br>

## Dry Run

```ini
Input: A = 2, B = 1, C = [10, 20, 30, 40]

Setup:
  low  = max(C) = 40      (a painter must paint the biggest board alone)
  high = sum(C) = 100     (one painter paints everything)
  ans  = -1

We binary search on the "max length one painter may take".
For each mid we greedily count how many painters that limit needs.


Iteration 1:
  low = 40, high = 100
  mid = (40 + 100) // 2 = 70

  Count painters with limit = 70:
    start:    painter 1, load = 10
    board 20: 10 + 20 = 30  <= 70  -> load = 30
    board 30: 30 + 30 = 60  <= 70  -> load = 60
    board 40: 60 + 40 = 100 >  70  -> new painter 2, load = 40
    painters needed = 2

  2 <= A(2)? YES (feasible)
  Save ans = 70, shrink right side: high = 70 - 1 = 69


Iteration 2:
  low = 40, high = 69
  mid = (40 + 69) // 2 = 54

  Count painters with limit = 54:
    start:    painter 1, load = 10
    board 20: 10 + 20 = 30 <= 54 -> load = 30
    board 30: 30 + 30 = 60 >  54 -> new painter 2, load = 30
    board 40: 30 + 40 = 70 >  54 -> new painter 3, load = 40
    painters needed = 3

  3 <= A(2)? NO (too tight)
  Push left side up: low = 54 + 1 = 55


Iteration 3:
  low = 55, high = 69
  mid = (55 + 69) // 2 = 62

  Count painters with limit = 62:
    start:    painter 1, load = 10
    board 20: 10 + 20 = 30  <= 62 -> load = 30
    board 30: 30 + 30 = 60  <= 62 -> load = 60
    board 40: 60 + 40 = 100 >  62 -> new painter 2, load = 40
    painters needed = 2

  2 <= A(2)? YES (feasible)
  Save ans = 62, shrink right side: high = 62 - 1 = 61


Iteration 4:
  low = 55, high = 61
  mid = (55 + 61) // 2 = 58

  Count painters with limit = 58:
    start:    painter 1, load = 10
    board 20: 10 + 20 = 30 <= 58 -> load = 30
    board 30: 30 + 30 = 60 >  58 -> new painter 2, load = 30
    board 40: 30 + 40 = 70 >  58 -> new painter 3, load = 40
    painters needed = 3

  3 <= A(2)? NO (too tight)
  Push left side up: low = 58 + 1 = 59


Iteration 5:
  low = 59, high = 61
  mid = (59 + 61) // 2 = 60

  Count painters with limit = 60:
    start:    painter 1, load = 10
    board 20: 10 + 20 = 30  <= 60 -> load = 30
    board 30: 30 + 30 = 60  <= 60 -> load = 60
    board 40: 60 + 40 = 100 >  60 -> new painter 2, load = 40
    painters needed = 2

  2 <= A(2)? YES (feasible)
  Save ans = 60, shrink right side: high = 60 - 1 = 59


Iteration 6:
  low = 59, high = 59
  mid = (59 + 59) // 2 = 59

  Count painters with limit = 59:
    start:    painter 1, load = 10
    board 20: 10 + 20 = 30 <= 59 -> load = 30
    board 30: 30 + 30 = 60 >  59 -> new painter 2, load = 30
    board 40: 30 + 40 = 70 >  59 -> new painter 3, load = 40
    painters needed = 3

  3 <= A(2)? NO (too tight)
  Push left side up: low = 59 + 1 = 60


Loop ends:
  low = 60, high = 59
  low <= high? 60 <= 59 -> NO, so the loop stops.

  ans = 60                 (best "max length" found)
  ans = ans * B = 60 * 1 = 60
  Answer = 60 % 10000003 = 60
```

<br><br>

## Related Problems

- [Split Array Largest Sum (410)](https://leetcode.com/problems/split-array-largest-sum/)
- [Capacity To Ship Packages Within D Days (1011)](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/)
- [Koko Eating Bananas (875)](https://leetcode.com/problems/koko-eating-bananas/)
- [Find the Smallest Divisor Given a Threshold (1283)](https://leetcode.com/problems/find-the-smallest-divisor-given-a-threshold/)
- [Minimum Number of Days to Make m Bouquets (1482)](https://leetcode.com/problems/minimum-number-of-days-to-make-m-bouquets/)