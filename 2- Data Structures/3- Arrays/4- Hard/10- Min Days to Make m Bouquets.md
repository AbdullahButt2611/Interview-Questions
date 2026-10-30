# Minimum Number of Days to Make m Bouquets

`Amazon` • `Google` • `Microsoft` • `Meta`

<br>

## Problem Statement

You are given an integer array `bloomDay`, an integer `m` and an integer `k`.

- You want to make `m` bouquets.
- One bouquet needs `k` **adjacent** flowers.
- The garden has `n` flowers. Flower `i` blooms on day `bloomDay[i]`.
- Each flower can be used in exactly one bouquet.

Return the minimum number of days to wait before `m` bouquets can be made. Return `-1` if it is impossible.

## Examples

**Example 1**

```ini
Input  = bloomDay = [1,10,3,10,2], m = 3, k = 1
Output = 3
```

```ini
After day 1 = [x, _, _, _, _]   1 bouquet
After day 2 = [x, _, _, _, x]   2 bouquets
After day 3 = [x, _, x, _, x]   3 bouquets, done
```

**Example 2**

```ini
Input  = bloomDay = [1,10,3,10,2], m = 3, k = 2
Output = -1
```

We need 6 flowers. The garden only has 5.

**Example 3**

```ini
Input  = bloomDay = [7,7,7,7,12,7,7], m = 2, k = 3
Output = 12
```

```ini
After day 7  = [x, x, x, x, _, x, x]   1 bouquet only
After day 12 = [x, x, x, x, x, x, x]   2 bouquets, done
```

## Constraints

```ini
bloomDay.length = n
1 <= n           <= 10^5
1 <= bloomDay[i] <= 10^9
1 <= m           <= 10^6
1 <= k           <= n
```

<br><br>

## The Idea in Simple Words

Picture the garden as a straight line of flower pots. Each pot has a date on it.

Now stand in the garden on some day `D`:

- Flowers with date **<= D** are open.
- Flowers with date **> D** are still closed.
- A closed flower is a **wall**. It splits the line into pieces.

You must pick `k` flowers standing side by side, with no wall in between.

So the whole problem becomes one question:

> What is the earliest day `D` where the open flowers form enough side by side groups to build `m` bouquets?

<br><br>

## Step 1: The Impossible Case

Each bouquet eats `k` flowers, and a flower is used only once. So `m` bouquets need `m * k` flowers.

If the garden has fewer than that, waiting cannot help. Waiting grows the number of **open** flowers, never the number of flowers.

```python
if len(bloomDay) < m * k:
    return -1
```

<mark>This is the only case that returns -1. If enough flowers exist, an answer always exists, because on the last bloom day the whole garden is open.</mark>

<br><br>

## Step 2: The Answer Only Turns On Once

Ask this for each day:

> Can I make `m` bouquets by day `D`?

A bloomed flower never closes again. So a "Yes" on day 7 stays a "Yes" on day 8, day 9, day 100.

The answers therefore look like this:

```ini
Day    = 1   2   3   4   5   6   7   8   9   10
Answer = No  No  No  No  No  No  Yes Yes Yes Yes
                                  ^
                                  we want this one
```

<mark>No, No, No, then Yes forever. It never flips back. This property is what makes binary search legal here.</mark>

We want the **first Yes**, which is exactly the boundary binary search is built to find.

<br><br>

## Step 3: Why We Search Between min and max

This is the part that trips people up.

We are **not** searching array indices. We are searching **days**, which are the answers themselves. This is called binary search on the answer.

Every search needs a range, so:

**Lower bound = `min(bloomDay)`**

- Before the earliest bloom day, the garden is empty.
- Zero open flowers means zero bouquets.
- Every day before it is a guaranteed "No", so there is nothing to check there.

**Upper bound = `max(bloomDay)`**

- On this day, every flower in the garden is open.
- The garden is as full as it will ever get.
- Day `max + 1` looks identical to day `max`, so searching further is pointless.

```ini
low  = min(bloomDay)   first day anything is even possible
high = max(bloomDay)   day the whole garden is open, best case ever
```

The answer, if it exists, must sit inside `[low, high]`.

Note that the array does **not** need to be sorted, because we search the day range, not the array.

<br><br>

## Step 4: The Helper Function

Given a candidate day, count how many bouquets are possible.

```python
def bloomingPossible(self, bloomDay, possibleDay, no_of_bouchets, no_of_flowers):
    count = 0        # length of the current run of adjacent open flowers
    bouchets = 0     # bouquets collected so far

    for bloom in bloomDay:
        if possibleDay >= bloom:
            count += 1                              # open, the run grows
        else:
            bouchets += count // no_of_flowers      # wall, cash in the run
            count = 0                               # and reset it

    bouchets += count // no_of_flowers              # cash in the final run
    return bouchets >= no_of_bouchets
```

**Why `count // k` works**

A run of `L` adjacent open flowers is just chopped into chunks of `k`.

```ini
run of 8, k = 2  =  8 // 2  =  4 bouquets
run of 7, k = 3  =  7 // 3  =  2 bouquets (1 wasted)
run of 2, k = 3  =  2 // 3  =  0 bouquets
```

**Two lines people forget**

- The reset `count = 0`. Without it, flowers on opposite sides of a wall are treated as neighbours.
- The `bouchets += count // k` **after** the loop. If the array ends on open flowers, that run never hits the `else` branch and would be lost.

This helper is `O(n)`, one clean pass.

<br><br>

## Approach 1: Brute Force (Linear Search)

**The plan**

1. Start at `day = min(bloomDay)`.
2. Ask the helper if `m` bouquets are possible.
3. Yes, return that day.
4. No, move to `day + 1` and repeat.

Since we walk upward and stop at the first success, that first "Yes" is automatically the minimum.

```python
class Solution:
    def bloomingPossible(self, bloomDay, possibleDay, no_of_bouchets, no_of_flowers):
        count = 0
        bouchets = 0

        for bloom in bloomDay:
            if possibleDay >= bloom:
                count += 1
            else:
                bouchets += count // no_of_flowers
                count = 0

        bouchets += count // no_of_flowers
        return bouchets >= no_of_bouchets

    def minDays(self, bloomDay: List[int], m: int, k: int) -> int:
        if len(bloomDay) < m * k:
            return -1

        for day in range(min(bloomDay), max(bloomDay) + 1):
            if self.bloomingPossible(bloomDay, day, m, k):
                return day

        return -1
```

```ini
Time  = O((max - min + 1) * n)
Space = O(1)
```

**Why it fails**

`bloomDay[i]` goes up to `10^9` and `n` up to `10^5`, so roughly `10^14` operations. It times out.

Still worth mentioning in an interview. It shows you understood the problem before optimising it.

<br><br>

## Approach 2: Optimized (Binary Search on the Answer)

**The plan**

Instead of walking day by day, jump to the middle and throw away half the range each time.

1. `low = min(bloomDay)`, `high = max(bloomDay)`.
2. Take the middle day `mid`.
3. Ask the helper about `mid`:
   - **Works** → save it in `ans`, then try earlier with `high = mid - 1`.
   - **Fails** → every earlier day fails too, so jump right with `low = mid + 1`.
4. Stop when `low > high`. The last saved `ans` is the answer.

The `ans` variable is the safety net. We save a working day before trying to beat it, so a valid answer can never be lost.

```python
class Solution:
    def bloomingPossible(self, bloomDay, possibleDay, no_of_bouchets, no_of_flowers):
        count = 0
        bouchets = 0

        for bloom in bloomDay:
            if possibleDay >= bloom:
                count += 1
            else:
                bouchets += count // no_of_flowers
                count = 0

        bouchets += count // no_of_flowers
        return bouchets >= no_of_bouchets

    def minDays(self, bloomDay: List[int], m: int, k: int) -> int:
        ans = -1

        if len(bloomDay) < m * k:        # not enough flowers, ever
            return -1

        low = min(bloomDay)              # earliest day anything is open
        high = max(bloomDay)             # day the whole garden is open

        while low <= high:
            mid = (low + high) // 2

            if self.bloomingPossible(bloomDay, mid, m, k):
                ans = mid                # works, save it
                high = mid - 1           # now try even earlier
            else:
                low = mid + 1            # too early, wait longer

        return ans
```

```ini
Time  = O(n * log(max - min))
Space = O(1)
```

With `n = 10^5` and a range of `10^9`, that is about 30 checks, so roughly `3 * 10^6` operations instead of `10^14`.

<br><br>

## Dry Run

Four cases follow. Each one stresses a different part of the solution.

Every iteration is shown in four blocks:

1. **State before** the iteration
2. **Pick mid** and see the garden on that day
3. **Helper walk**, one line per flower
4. **Verdict and state after**, with the reason the range moved

### Case 1: `[1000000000, 1000000000]`, m = 1, k = 1

**Why this case:** proves why the range starts at `min(bloomDay)`, and shows what happens when `min` equals `max`, so the range holds exactly one candidate day.

**Setup**

```ini
guard = len(bloomDay) is 2, m * k is 1, and 2 >= 1, so we continue
low   = min(bloomDay) = 1000000000
high  = max(bloomDay) = 1000000000
ans   = -1
```

**Iteration 1**

State before:

```ini
low = 1000000000, high = 1000000000, ans = -1
low <= high is true, so we enter the loop
```

Pick mid:

```ini
mid = (1000000000 + 1000000000) // 2 = 1000000000
question = can we make 1 bouquet of 1 flower by day 1000000000
```

Garden on day 1000000000:

```ini
index  =  0            1
value  =  1000000000   1000000000
open?  =  x            x
```

Helper walk, starting from `count = 0` and `bouchets = 0`:

```ini
step 1 = flower[0] is 1000000000, and 1000000000 <= 1000000000, so it is open
         count goes 0 to 1, bouchets stays 0

step 2 = flower[1] is 1000000000, and 1000000000 <= 1000000000, so it is open
         count goes 1 to 2, bouchets stays 0

after the loop = the array ended on an open run of 2, so cash it in
                 2 // 1 = 2 bouquets, bouchets goes 0 to 2
```

Verdict:

```ini
bouchets = 2, we need m = 1, and 2 >= 1, so the helper returns True
```

State after:

```ini
day 1000000000 works, so ans goes -1 to 1000000000
we still want an earlier day, so high goes 1000000000 to 999999999
```

**Loop check**

```ini
low = 1000000000, high = 999999999
low <= high is false, so the loop stops
Answer = ans = 1000000000
```

**Summary**

```ini
iteration | low        | high       | mid        | got | need | verdict | ans        | move
    1     | 1000000000 | 1000000000 | 1000000000 |  2  |  1   |  Yes    | 1000000000 | high = 999999999
```

**Lesson**

- The whole thing finished in a **single** iteration.
- Binary search would survive even if `low` started at day 1, since that is only about 30 checks.
- A linear scan starting at day 1 would crawl through a billion useless days first.
- The bounds are not decoration, they are the reason this runs fast.

### Case 2: `[1,10,2,9,3,8,4,7,5,6]`, m = 4, k = 2

**Why this case:** small and big values alternate, so the garden fills in unevenly. This shows the search narrowing over several rounds, and the reset logic doing real work.

**Setup**

```ini
guard = len(bloomDay) is 10, m * k is 8, and 10 >= 8, so we continue
low   = min(bloomDay) = 1
high  = max(bloomDay) = 10
ans   = -1
```

**Iteration 1**

State before:

```ini
low = 1, high = 10, ans = -1
low <= high is true, so we enter the loop
```

Pick mid:

```ini
mid = (1 + 10) // 2 = 5
question = can we make 4 bouquets of 2 adjacent flowers by day 5
```

Garden on day 5:

```ini
index =  0  1   2  3  4  5  6  7  8  9
value =  1  10  2  9  3  8  4  7  5  6
open? =  x  _   x  _  x  _  x  _  x  _
```

Helper walk, starting from `count = 0` and `bouchets = 0`:

```ini
step 1  = flower 1 is open, since 1 <= 5
          count 0 to 1, bouchets stays 0

step 2  = flower 10 is a wall, since 10 > 5
          cash the run, 1 // 2 = 0 bouquets, bouchets stays 0
          count resets 1 to 0

step 3  = flower 2 is open, since 2 <= 5
          count 0 to 1, bouchets stays 0

step 4  = flower 9 is a wall, since 9 > 5
          cash the run, 1 // 2 = 0, bouchets stays 0
          count resets 1 to 0

step 5  = flower 3 is open, since 3 <= 5
          count 0 to 1, bouchets stays 0

step 6  = flower 8 is a wall, since 8 > 5
          cash the run, 1 // 2 = 0, bouchets stays 0
          count resets 1 to 0

step 7  = flower 4 is open, since 4 <= 5
          count 0 to 1, bouchets stays 0

step 8  = flower 7 is a wall, since 7 > 5
          cash the run, 1 // 2 = 0, bouchets stays 0
          count resets 1 to 0

step 9  = flower 5 is open, since 5 <= 5
          count 0 to 1, bouchets stays 0

step 10 = flower 6 is a wall, since 6 > 5
          cash the run, 1 // 2 = 0, bouchets stays 0
          count resets 1 to 0

after the loop = count is already 0, so 0 // 2 = 0, bouchets stays 0
```

Verdict:

```ini
bouchets = 0, we need m = 4, and 0 >= 4 is false, so the helper returns False
```

Read that picture again. Five flowers are open, which is more than the 8 we eventually need, and yet every single one of them stands alone between two walls. A run of length 1 with `k = 2` is worth nothing.

State after:

```ini
day 5 failed, and every day before 5 has fewer open flowers, so those fail too
we throw away the whole left half, low goes 1 to 6

range before = 1 to 10
range after  = 6 to 10
```

**Iteration 2**

State before:

```ini
low = 6, high = 10, ans = -1
low <= high is true, so we enter the loop
```

Pick mid:

```ini
mid = (6 + 10) // 2 = 8
question = can we make 4 bouquets of 2 adjacent flowers by day 8
```

Garden on day 8:

```ini
index =  0  1   2  3  4  5  6  7  8  9
value =  1  10  2  9  3  8  4  7  5  6
open? =  x  _   x  _  x  x  x  x  x  x
```

The `8` at index 5 has now opened, which glues indices 4 through 9 into one long run.

Helper walk, starting from `count = 0` and `bouchets = 0`:

```ini
step 1  = flower 1 is open, since 1 <= 8
          count 0 to 1, bouchets stays 0

step 2  = flower 10 is a wall, since 10 > 8
          cash the run, 1 // 2 = 0, bouchets stays 0
          count resets 1 to 0

step 3  = flower 2 is open, since 2 <= 8
          count 0 to 1, bouchets stays 0

step 4  = flower 9 is a wall, since 9 > 8
          cash the run, 1 // 2 = 0, bouchets stays 0
          count resets 1 to 0

step 5  = flower 3 is open, since 3 <= 8
          count 0 to 1

step 6  = flower 8 is open, since 8 <= 8
          count 1 to 2

step 7  = flower 4 is open, since 4 <= 8
          count 2 to 3

step 8  = flower 7 is open, since 7 <= 8
          count 3 to 4

step 9  = flower 5 is open, since 5 <= 8
          count 4 to 5

step 10 = flower 6 is open, since 6 <= 8
          count 5 to 6

after the loop = the array ended while a run of 6 was still growing
                 cash it in, 6 // 2 = 3 bouquets, bouchets goes 0 to 3
```

Verdict:

```ini
bouchets = 3, we need m = 4, and 3 >= 4 is false, so the helper returns False
```

Pay attention to that last block. Steps 5 through 10 never hit the `else` branch, so nothing was ever cashed in during the loop. Without the line **after** the loop, this whole run of 6 would have scored 0 and the answer would be wrong.

State after:

```ini
day 8 failed, so every earlier day fails too
low goes 6 to 9

range before = 6 to 10
range after  = 9 to 10
```

**Iteration 3**

State before:

```ini
low = 9, high = 10, ans = -1
low <= high is true, so we enter the loop
```

Pick mid:

```ini
mid = (9 + 10) // 2 = 9
question = can we make 4 bouquets of 2 adjacent flowers by day 9
```

Garden on day 9:

```ini
index =  0  1   2  3  4  5  6  7  8  9
value =  1  10  2  9  3  8  4  7  5  6
open? =  x  _   x  x  x  x  x  x  x  x
```

The `9` at index 3 opened, so indices 2 through 9 are now one run of 8.

Helper walk, starting from `count = 0` and `bouchets = 0`:

```ini
step 1  = flower 1 is open, since 1 <= 9
          count 0 to 1

step 2  = flower 10 is a wall, since 10 > 9
          cash the run, 1 // 2 = 0, bouchets stays 0
          count resets 1 to 0

step 3  = flower 2 is open, since 2 <= 9
          count 0 to 1

step 4  = flower 9 is open, since 9 <= 9
          count 1 to 2

step 5  = flower 3 is open, since 3 <= 9
          count 2 to 3

step 6  = flower 8 is open, since 8 <= 9
          count 3 to 4

step 7  = flower 4 is open, since 4 <= 9
          count 4 to 5

step 8  = flower 7 is open, since 7 <= 9
          count 5 to 6

step 9  = flower 5 is open, since 5 <= 9
          count 6 to 7

step 10 = flower 6 is open, since 6 <= 9
          count 7 to 8

after the loop = cash the final run, 8 // 2 = 4 bouquets, bouchets goes 0 to 4
```

Verdict:

```ini
bouchets = 4, we need m = 4, and 4 >= 4 is true, so the helper returns True
```

State after:

```ini
day 9 works, so ans goes -1 to 9
we still want to know if something earlier works, so high goes 10 to 8
```

**Loop check**

```ini
low = 9, high = 8
low <= high is false, so the loop stops
Answer = ans = 9
```

**Summary**

```ini
iteration | low | high | mid | got | need | verdict | ans | move
    1     |  1  |  10  |  5  |  0  |  4   |   No    | -1  | low = 6
    2     |  6  |  10  |  8  |  3  |  4   |   No    | -1  | low = 9
    3     |  9  |  10  |  9  |  4  |  4   |   Yes   |  9  | high = 8
```

**Lesson**

- One closed flower (the `10` at index 1) cuts the line in two and costs us a bouquet all the way to the end.
- Ten candidate days were settled in three checks.
- Between day 8 and day 9 the bouquet count jumped from 3 to 4 because a single wall came down and merged two runs.

### Case 3: `[7,7,7,7,12,7,7]`, m = 2, k = 3

**Why this case:** the adjacency trap. By day 7 there are already 6 open flowers and we need exactly 6, yet day 7 is still not the answer.

**Setup**

```ini
guard = len(bloomDay) is 7, m * k is 6, and 7 >= 6, so we continue
low   = min(bloomDay) = 7
high  = max(bloomDay) = 12
ans   = -1
```

Before starting, look at day 7 by hand, because this is the trap:

```ini
index    =  0  1  2  3  4   5  6
value    =  7  7  7  7  12  7  7
open?    =  x  x  x  x  _   x  x

run A    = indices 0 to 3, length 4, worth 4 // 3 = 1 bouquet
run B    = indices 5 to 6, length 2, worth 2 // 3 = 0 bouquets
total    = 1 bouquet, but we need 2
```

Six flowers are open, exactly the number we need, but the wall at index 4 splits them into 4 and 2. The run of 4 gives one bouquet and wastes a flower. The run of 2 is too short to give anything at all.

**Iteration 1**

State before:

```ini
low = 7, high = 12, ans = -1
low <= high is true, so we enter the loop
```

Pick mid:

```ini
mid = (7 + 12) // 2 = 9
question = can we make 2 bouquets of 3 adjacent flowers by day 9
```

Garden on day 9:

```ini
index =  0  1  2  3  4   5  6
value =  7  7  7  7  12  7  7
open? =  x  x  x  x  _   x  x
```

Helper walk, starting from `count = 0` and `bouchets = 0`:

```ini
step 1 = flower 7 is open, since 7 <= 9
         count 0 to 1

step 2 = flower 7 is open, since 7 <= 9
         count 1 to 2

step 3 = flower 7 is open, since 7 <= 9
         count 2 to 3

step 4 = flower 7 is open, since 7 <= 9
         count 3 to 4

step 5 = flower 12 is a wall, since 12 > 9
         cash the run, 4 // 3 = 1 bouquet, bouchets goes 0 to 1
         count resets 4 to 0
         note that the 4th flower of that run is wasted, 3 were used and 1 is left over

step 6 = flower 7 is open, since 7 <= 9
         count 0 to 1

step 7 = flower 7 is open, since 7 <= 9
         count 1 to 2

after the loop = cash the final run, 2 // 3 = 0 bouquets, bouchets stays 1
```

Verdict:

```ini
bouchets = 1, we need m = 2, and 1 >= 2 is false, so the helper returns False
```

State after:

```ini
day 9 failed, so days 7 and 8 fail too
low goes 7 to 10

range before = 7 to 12
range after  = 10 to 12
```

**Iteration 2**

State before:

```ini
low = 10, high = 12, ans = -1
low <= high is true, so we enter the loop
```

Pick mid:

```ini
mid = (10 + 12) // 2 = 11
question = can we make 2 bouquets of 3 adjacent flowers by day 11
```

Garden on day 11:

```ini
index =  0  1  2  3  4   5  6
value =  7  7  7  7  12  7  7
open? =  x  x  x  x  _   x  x
```

The only closed flower needs day 12, and 12 > 11, so the picture has not changed at all since day 9.

Helper walk, starting from `count = 0` and `bouchets = 0`:

```ini
step 1 = flower 7 is open, since 7 <= 11, count 0 to 1
step 2 = flower 7 is open, since 7 <= 11, count 1 to 2
step 3 = flower 7 is open, since 7 <= 11, count 2 to 3
step 4 = flower 7 is open, since 7 <= 11, count 3 to 4

step 5 = flower 12 is a wall, since 12 > 11
         cash the run, 4 // 3 = 1, bouchets goes 0 to 1
         count resets 4 to 0

step 6 = flower 7 is open, since 7 <= 11, count 0 to 1
step 7 = flower 7 is open, since 7 <= 11, count 1 to 2

after the loop = 2 // 3 = 0, bouchets stays 1
```

Verdict:

```ini
bouchets = 1, we need m = 2, so False again
```

State after:

```ini
day 11 failed, so low goes 11 + 1 = 12

range before = 10 to 12
range after  = 12 to 12
```

**Iteration 3**

State before:

```ini
low = 12, high = 12, ans = -1
low <= high is true, so we enter the loop
```

Pick mid:

```ini
mid = (12 + 12) // 2 = 12
question = can we make 2 bouquets of 3 adjacent flowers by day 12
```

Garden on day 12:

```ini
index =  0  1  2  3  4   5  6
value =  7  7  7  7  12  7  7
open? =  x  x  x  x  x   x  x
```

The wall has fallen. The garden is now one unbroken run of 7.

Helper walk, starting from `count = 0` and `bouchets = 0`:

```ini
step 1 = flower 7 is open, since 7 <= 12, count 0 to 1
step 2 = flower 7 is open, since 7 <= 12, count 1 to 2
step 3 = flower 7 is open, since 7 <= 12, count 2 to 3
step 4 = flower 7 is open, since 7 <= 12, count 3 to 4

step 5 = flower 12 is open, since 12 <= 12, count 4 to 5
         this is the step that changes everything, the else branch is never taken

step 6 = flower 7 is open, since 7 <= 12, count 5 to 6
step 7 = flower 7 is open, since 7 <= 12, count 6 to 7

after the loop = cash the final run, 7 // 3 = 2 bouquets, bouchets goes 0 to 2
```

Verdict:

```ini
bouchets = 2, we need m = 2, and 2 >= 2 is true, so the helper returns True
```

State after:

```ini
day 12 works, so ans goes -1 to 12
we still try earlier, so high goes 12 to 11
```

**Loop check**

```ini
low = 12, high = 11
low <= high is false, so the loop stops
Answer = ans = 12
```

**Summary**

```ini
iteration | low | high | mid | got | need | verdict | ans | move
    1     |  7  |  12  |  9  |  1  |  2   |   No    | -1  | low = 10
    2     | 10  |  12  | 11  |  1  |  2   |   No    | -1  | low = 12
    3     | 12  |  12  | 12  |  2  |  2   |   Yes   | 12  | high = 11
```

**Lesson**

<mark>Enough open flowers does not mean enough bouquets. A wall in the wrong place wastes flowers on both sides of it.</mark>

- On day 9 we had 6 open flowers split as 4 plus 2, which is worth only 1 bouquet.
- On day 12 we had 7 open flowers in one run, which is worth 2 bouquets.
- One extra flower doubled the result, purely because it joined the two groups together.
- This is exactly why the helper resets `count` instead of just summing totals.

### Case 4: `[1,10,3,10,2]`, m = 3, k = 2

**Why this case:** the impossible case. It justifies the guard clause, and it never reaches the binary search at all.

**Setup**

```ini
len(bloomDay) = 5
m * k = 3 * 2 = 6
is 5 < 6, yes
return -1 immediately
```

We need 6 flowers and only 5 exist. A flower is used in exactly one bouquet, so no clever arrangement rescues us, and waiting only opens flowers, it never creates them.

**What if the guard were missing?**

The answer would still be `-1`, but the code would work much harder to find that out. Here is the full trace without the guard.

```ini
low = 1, high = 10, ans = -1
```

Iteration 1:

```ini
mid = (1 + 10) // 2 = 5

index =  0  1   2  3   4
value =  1  10  3  10  2
open? =  x  _   x  _   x

step 1 = flower 1 is open, count 0 to 1
step 2 = flower 10 is a wall, cash 1 // 2 = 0, count resets to 0
step 3 = flower 3 is open, count 0 to 1
step 4 = flower 10 is a wall, cash 1 // 2 = 0, count resets to 0
step 5 = flower 2 is open, count 0 to 1
after the loop = cash 1 // 2 = 0

bouchets = 0, need 3, False, so low goes to 6
```

Iteration 2:

```ini
mid = (6 + 10) // 2 = 8
the two 10s are still closed, so the picture is identical to day 5
bouchets = 0, need 3, False, so low goes to 9
```

Iteration 3:

```ini
mid = (9 + 10) // 2 = 9
still 10 > 9, so the picture is identical again
bouchets = 0, need 3, False, so low goes to 10
```

Iteration 4:

```ini
mid = (10 + 10) // 2 = 10

open? =  x  x  x  x  x     the whole garden is open

step 1 = flower 1 is open, count 0 to 1
step 2 = flower 10 is open, count 1 to 2
step 3 = flower 3 is open, count 2 to 3
step 4 = flower 10 is open, count 3 to 4
step 5 = flower 2 is open, count 4 to 5
after the loop = cash 5 // 2 = 2, bouchets goes 0 to 2

bouchets = 2, need 3, False, so low goes to 11
```

Loop check:

```ini
low = 11, high = 10
low <= high is false, so the loop stops
ans was never assigned, so it is still -1
Answer = -1
```

**Summary**

```ini
iteration | low | high | mid | got | need | verdict | ans | move
    1     |  1  |  10  |  5  |  0  |  3   |   No    | -1  | low = 6
    2     |  6  |  10  |  8  |  0  |  3   |   No    | -1  | low = 9
    3     |  9  |  10  |  9  |  0  |  3   |   No    | -1  | low = 10
    4     | 10  |  10  | 10  |  2  |  3   |   No    | -1  | low = 11
```

**Lesson**

- Even on day 10, with every flower open, we only squeeze out 2 bouquets.
- Day 10 is the best case that will ever exist, so if it fails, every day fails.
- The guard is not required for correctness, but it turns four passes into an `O(1)` exit.
- `ans = -1` is what quietly handles the failure path, so never initialise it to `0` or to `high`.

<br><br>

## Common Mistakes

- **Missing the final `count // k` after the loop.** A run at the end of the array gets silently dropped.
- **Not resetting `count` on a wall.** Flowers on either side get treated as neighbours.
- **Returning `low` blindly** instead of tracking `ans`. Tracking `ans` is safer and reads clearer.
- **Mixing `high = mid` with `while low <= high`.** That causes an infinite loop. Keep the pair consistent.
- **Sorting the array.** Sorting destroys adjacency, which is the entire problem. Order must stay untouched.
- **Overflow on `m * k`** in Java or C++. With `m` up to `10^6` and `k` up to `10^5`, it can exceed 32 bits. Use `long`, or compare as `len(bloomDay) / k < m`.

<br><br>

## Related Problems

- [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/)
- [Capacity To Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/)
- [Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/)
- [Find the Smallest Divisor Given a Threshold](https://leetcode.com/problems/find-the-smallest-divisor-given-a-threshold/)
- [Magnetic Force Between Two Balls](https://leetcode.com/problems/magnetic-force-between-two-balls/)
- [Minimum Time to Complete Trips](https://leetcode.com/problems/minimum-time-to-complete-trips/)
- [Maximum Candies Allocated to K Children](https://leetcode.com/problems/maximum-candies-allocated-to-k-children/)
- [Minimized Maximum of Products Distributed to Any Store](https://leetcode.com/problems/minimized-maximum-of-products-distributed-to-any-store/)
- [Minimum Limit of Balls in a Bag](https://leetcode.com/problems/minimum-limit-of-balls-in-a-bag/)
- [Kth Smallest Number in Multiplication Table](https://leetcode.com/problems/kth-smallest-number-in-multiplication-table/)