# Capacity To Ship Packages Within D Days

`Amazon` • `Google` • `Meta` • `Uber` • `Morgan Stanley` • `Coinbase` • `DoorDash` • `Expedia` • `Flipkart` • `Agoda`

## Problem Statement

Packages on a conveyor belt must be shipped from one port to another within `days` days.

- Package `i` weighs `weights[i]`.
- Each day we load the ship in the given order, never going over its weight capacity.

Return the least ship capacity that gets every package shipped within `days` days.

<mark>Packages must be taken in array order. Reordering or skipping is not allowed.</mark>

## Examples

**Example 1**

```ini
Input:  weights = [1,2,3,4,5,6,7,8,9,10], days = 5
Output: 15

Explanation:
A ship capacity of 15 is the minimum to ship all packages in 5 days:
1st day: 1, 2, 3, 4, 5
2nd day: 6, 7
3rd day: 8
4th day: 9
5th day: 10

A capacity of 14 with a split like (2,3,4,5), (1,6,7), (8), (9), (10)
is NOT allowed, because the order was changed.
```

**Example 2**

```ini
Input:  weights = [3,2,2,4,1,4], days = 3
Output: 6

Explanation:
1st day: 3, 2
2nd day: 2, 4
3rd day: 1, 4
```

**Example 3**

```ini
Input:  weights = [1,2,3,1,1], days = 4
Output: 3

Explanation:
1st day: 1
2nd day: 2
3rd day: 3
4th day: 1, 1
```

## Constraints

- `1 <= days <= weights.length <= 5 * 10^4`
- `1 <= weights[i] <= 500`

<br><br>

## Approach (Binary Search on the Answer)

**Step 1: Fix the search range**

We are searching for a number (the capacity), not for an element in the array.

- `low = max(weights)`: the ship must at least carry the heaviest package.
- `high = sum(weights)`: everything ships in one day, so this always works.

The answer lies somewhere in `[low, high]`.

<br><br>

**Step 2: Spot the NO/YES pattern**

A bigger ship is never worse, so once a capacity works, every larger one works too.

```ini
Capacity:   4    5    6    7    8    9   10 ...
Works?     NO   NO  YES  YES  YES  YES  YES
                    ^ first YES = answer
```

<mark>A block of NO followed by a block of YES is exactly what binary search needs.</mark>

<br><br>

**Step 3: Check one capacity (greedy count)**

Start with `load = 0`, `days = 1`, then scan left to right:

- `load + weight <= capacity`: it fits today, so `load += weight`.
- `load + weight > capacity`: today is full, so `days += 1` and `load = weight`.

The final `days` is the cost of that capacity. Greedy is safe because the order is fixed, and leaving a day half empty never helps.

<br><br>

**Step 4: Binary search the range**

- `mid = (low + high) // 2` is the capacity we test.
- Days needed `<=` given `days`: `mid` works, so store it in `capacity` and shrink with `high = mid - 1`.
- Days needed `>` given `days`: `mid` is too small, so grow with `low = mid + 1`.
- Loop stops when `low > high`, and `capacity` holds the smallest working value.

<br><br>

## Code

```python
class Solution:
    def daysToLoadWithGivenCapacity(self, weights, capacity):
        load = 0
        days = 1

        for weight in weights:
            if load + weight > capacity:
                load = weight
                days += 1
            else:
                load += weight
        
        return days

    def shipWithinDays(self, weights: List[int], days: int) -> int:
        low = max(weights)
        high = sum(weights)
        capacity = float('inf')

        while low <= high:
            mid = (low + high) // 2
            
            if self.daysToLoadWithGivenCapacity(weights, mid) <= days:
                capacity = mid
                high = mid - 1
            else:
                low = mid + 1

        return capacity
```

<br><br>

## Dry Run

We will use `weights = [3, 2, 2, 4, 1, 4]` and `days = 3`.

```ini
SETUP
=====
low      = max(weights) = 4
high     = sum(weights) = 16
capacity = infinity


ITERATION 1
===========
low = 4, high = 16
mid = (4 + 16) // 2 = 10   -> test a ship of capacity 10

Counting days for capacity 10:
start: load = 0, days = 1

weight = 3 -> load + 3 = 0 + 3 = 3   -> 3 <= 10, fits  -> load = 3
weight = 2 -> load + 2 = 3 + 2 = 5   -> 5 <= 10, fits  -> load = 5
weight = 2 -> load + 2 = 5 + 2 = 7   -> 7 <= 10, fits  -> load = 7
weight = 4 -> load + 4 = 7 + 4 = 11  -> 11 > 10, OVERFLOW
              new day  -> days = 2, load = 4
weight = 1 -> load + 1 = 4 + 1 = 5   -> 5 <= 10, fits  -> load = 5
weight = 4 -> load + 4 = 5 + 4 = 9   -> 9 <= 10, fits  -> load = 9

days needed = 2
Split: [3,2,2] | [4,1,4]

Decision: 2 <= 3  -> capacity 10 WORKS
          capacity = 10
          high = mid - 1 = 9      (try smaller ships)


ITERATION 2
===========
low = 4, high = 9
mid = (4 + 9) // 2 = 6   -> test a ship of capacity 6

Counting days for capacity 6:
start: load = 0, days = 1

weight = 3 -> load + 3 = 0 + 3 = 3   -> 3 <= 6, fits  -> load = 3
weight = 2 -> load + 2 = 3 + 2 = 5   -> 5 <= 6, fits  -> load = 5
weight = 2 -> load + 2 = 5 + 2 = 7   -> 7 > 6, OVERFLOW
              new day  -> days = 2, load = 2
weight = 4 -> load + 4 = 2 + 4 = 6   -> 6 <= 6, fits  -> load = 6
weight = 1 -> load + 1 = 6 + 1 = 7   -> 7 > 6, OVERFLOW
              new day  -> days = 3, load = 1
weight = 4 -> load + 4 = 1 + 4 = 5   -> 5 <= 6, fits  -> load = 5

days needed = 3
Split: [3,2] | [2,4] | [1,4]

Decision: 3 <= 3  -> capacity 6 WORKS
          capacity = 6
          high = mid - 1 = 5      (try even smaller ships)


ITERATION 3
===========
low = 4, high = 5
mid = (4 + 5) // 2 = 4   -> test a ship of capacity 4

Counting days for capacity 4:
start: load = 0, days = 1

weight = 3 -> load + 3 = 0 + 3 = 3   -> 3 <= 4, fits  -> load = 3
weight = 2 -> load + 2 = 3 + 2 = 5   -> 5 > 4, OVERFLOW
              new day  -> days = 2, load = 2
weight = 2 -> load + 2 = 2 + 2 = 4   -> 4 <= 4, fits  -> load = 4
weight = 4 -> load + 4 = 4 + 4 = 8   -> 8 > 4, OVERFLOW
              new day  -> days = 3, load = 4
weight = 1 -> load + 1 = 4 + 1 = 5   -> 5 > 4, OVERFLOW
              new day  -> days = 4, load = 1
weight = 4 -> load + 4 = 1 + 4 = 5   -> 5 > 4, OVERFLOW
              new day  -> days = 5, load = 4

days needed = 5
Split: [3] | [2,2] | [4] | [1] | [4]

Decision: 5 > 3   -> capacity 4 FAILS (too small, needs too many days)
          capacity stays 6
          low = mid + 1 = 5       (we must go bigger)


ITERATION 4
===========
low = 5, high = 5
mid = (5 + 5) // 2 = 5   -> test a ship of capacity 5

Counting days for capacity 5:
start: load = 0, days = 1

weight = 3 -> load + 3 = 0 + 3 = 3   -> 3 <= 5, fits  -> load = 3
weight = 2 -> load + 2 = 3 + 2 = 5   -> 5 <= 5, fits  -> load = 5
weight = 2 -> load + 2 = 5 + 2 = 7   -> 7 > 5, OVERFLOW
              new day  -> days = 2, load = 2
weight = 4 -> load + 4 = 2 + 4 = 6   -> 6 > 5, OVERFLOW
              new day  -> days = 3, load = 4
weight = 1 -> load + 1 = 4 + 1 = 5   -> 5 <= 5, fits  -> load = 5
weight = 4 -> load + 4 = 5 + 4 = 9   -> 9 > 5, OVERFLOW
              new day  -> days = 4, load = 4

days needed = 4
Split: [3,2] | [2] | [4,1] | [4]

Decision: 4 > 3   -> capacity 5 FAILS
          capacity stays 6
          low = mid + 1 = 6


LOOP ENDS
=========
low = 6, high = 5
low <= high is FALSE  -> exit the while loop

return capacity = 6
```

<br><br>

**Summary of the whole search**

| Iteration | low | high | mid (capacity tested) | days needed | Verdict | Action |
|:--|:--|:--|:--|:--|:--|:--|
| 1 | 4 | 16 | 10 | 2 | works | capacity = 10, high = 9 |
| 2 | 4 | 9 | 6 | 3 | works | capacity = 6, high = 5 |
| 3 | 4 | 5 | 4 | 5 | fails | low = 5 |
| 4 | 5 | 5 | 5 | 4 | fails | low = 6 |

Final answer: `6`

<br><br>

## Complexity Analysis

**Time:** `O(n * log(sum(weights) - max(weights)))`

- Binary search over the capacity range takes `log` steps.
- Each step scans the array once to count days, costing `O(n)`.

**Space:** `O(1)`

- Only a few variables (`low`, `high`, `mid`, `load`, `days`), no extra data structures.

<br><br>

## Related Problems

- [410. Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/)
- [875. Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/)
- [1482. Minimum Number of Days to Make m Bouquets](https://leetcode.com/problems/minimum-number-of-days-to-make-m-bouquets/)
- [1283. Find the Smallest Divisor Given a Threshold](https://leetcode.com/problems/find-the-smallest-divisor-given-a-threshold/)
- [1552. Magnetic Force Between Two Balls](https://leetcode.com/problems/magnetic-force-between-two-balls/)
- [2064. Minimized Maximum of Products Distributed to Any Store](https://leetcode.com/problems/minimized-maximum-of-products-distributed-to-any-store/)
- [774. Minimize Max Distance to Gas Station](https://leetcode.com/problems/minimize-max-distance-to-gas-station/)
- [1231. Divide Chocolate](https://leetcode.com/problems/divide-chocolate/)
- [1891. Cutting Ribbons](https://leetcode.com/problems/cutting-ribbons/)
- [1898. Maximum Number of Removable Characters](https://leetcode.com/problems/maximum-number-of-removable-characters/)