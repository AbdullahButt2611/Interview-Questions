# Prefix Sum

A technique for answering "what's the sum of this range" instantly, by precomputing running totals once.

## What It Is

A prefix sum array stores running totals. For every position, it holds the sum of everything from the start up to and including that position, like a car's odometer reading at each checkpoint.

If you know the odometer reading at checkpoint A and at checkpoint B, the distance between them is one subtraction away. No need to re-measure the road.

## Core Idea

For an array `arr`, define:

`prefix[i]` = sum of `arr[0]` through `arr[i-1]`, with `prefix[0] = 0`.

To get the sum of `arr[L]` through `arr[R]` (inclusive), use:

`sum(L, R) = prefix[R + 1] - prefix[L]`

This one formula works for every range, including ranges starting at index 0, because of the leading `prefix[0] = 0`.

<br>

## When To Reach For It

Certain problem phrasings are reliable tells that prefix sum applies:

- A static array (it doesn't change) with many "sum of range [i, j]" queries
- A problem asking to count or find subarrays matching a target sum
- A "running total" framing, balances, distances, scores over time
- A 2D grid with many "sum of this rectangle" queries

Avoid it when the array is updated frequently between queries. Prefix sum needs an `O(n)` rebuild after every change. For "many updates + many range queries," a Fenwick Tree or Segment Tree is the right tool instead.

<br>

## Template Code (Python)

```python
def build_prefix_sum(arr):
    n = len(arr)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    return prefix

def range_sum(prefix, left, right):
    # sum of arr[left..right], inclusive
    return prefix[right + 1] - prefix[left]
```

## Step-by-Step Walkthrough

Take `arr = [5, 2, 9, 1, 7]`. Building the prefix array one running total at a time:

| Step | Calculation | Value |
|---|---|---|
| prefix[0] | start | 0 |
| prefix[1] | 0 + 5 | 5 |
| prefix[2] | 5 + 2 | 7 |
| prefix[3] | 7 + 9 | 16 |
| prefix[4] | 16 + 1 | 17 |
| prefix[5] | 17 + 7 | 24 |

Final prefix array: `[0, 5, 7, 16, 17, 24]`

To find the sum of `arr[1..3]` (that's `2 + 9 + 1 = 12`):

`sum(1, 3) = prefix[4] - prefix[1] = 17 - 5 = 12`

## Complexity

| Operation | Time | Space |
|---|---|---|
| Build prefix array | `O(n)` | `O(n)` |
| Range sum query | `O(1)` | - |
| Naive range sum (no prefix) | `O(n)` per query | `O(1)` |

With `n` elements and `q` queries, prefix sum gives `O(n + q)` total versus `O(n * q)` for the naive approach. This is the entire reason the pattern exists, pay a small fixed cost once, then every future query is instant.

<br>

## Variations

### Prefix Sum + Hash Map (Subarray Sum Equals K)

This is the highest-value variation to know cold, it appears constantly in interviews.

The intuition: if the running sum at the current position is `prefix_sum`, and some earlier running sum was exactly `prefix_sum - k`, then the slice between those two points sums to `k`. So rather than re-scanning, store every running sum seen so far and, at each step, ask how many times `prefix_sum - k` has already appeared. Each prior occurrence is one valid subarray ending here.

```python
def subarray_sum_equals_k(arr, k):
    count = 0
    prefix_sum = 0
    seen = {0: 1}  # an empty prefix has occurred once

    for num in arr:
        prefix_sum += num
        count += seen.get(prefix_sum - k, 0)
        seen[prefix_sum] = seen.get(prefix_sum, 0) + 1

    return count
```

Quick trace on `arr = [3, 1, 2]` with `k = 3`:

| Step | prefix_sum | looks for prefix_sum - k | already seen? | count |
|---|---|---|---|---|
| start | 0 | | `{0: 1}` | 0 |
| + 3 | 3 | 0 | yes, once | 1 |
| + 1 | 4 | 1 | no | 1 |
| + 2 | 6 | 3 | yes, once | 2 |

The two matching subarrays are `[3]` and `[1, 2]`.

Two points worth raising out loud in an interview:

- The `seen = {0: 1}` start is essential, it covers subarrays that begin at index 0.
- This holds up with negative numbers, which is the reason to reach for it instead of a sliding window. A sliding window assumes the sum only grows as the window widens, negatives break that assumption, while prefix sum plus a hash map does not depend on it.

<br>

### 2D Prefix Sum (Summed-Area Table)

For rectangle sum queries on a grid, build a 2D prefix array using inclusion-exclusion:

`prefix[i][j] = prefix[i-1][j] + prefix[i][j-1] - prefix[i-1][j-1] + matrix[i][j]`

The subtraction removes the double-counted overlap of the row above and the column to the left.

<br>

### Difference Array (the reverse pattern)

For many range updates (add `v` to every element from index `i` to `j`), with the final array only needed at the end, a difference array does each update in `O(1)`:

`diff[i] += v` and `diff[j + 1] -= v`

A single prefix sum pass over `diff` then reconstructs the final array in `O(n)`.

<br>

### Prefix XOR and Modular Prefix Sums

The pattern extends to any operation with an inverse. XOR is its own inverse, so "prefix XOR" answers range-XOR queries the same way. For "subarray sum divisible by k" problems, track `prefix_sum % k` in a hash map instead of the raw sum.

<br>

## Variations at a Glance

| Variation | Best For | Time |
|---|---|---|
| 1D Prefix Sum | Range sum queries | `O(n)` build, `O(1)` query |
| Prefix Sum + Hash Map | Count/find subarrays with sum k | `O(n)` |
| 2D Prefix Sum | Rectangle sum queries | `O(rows * cols)` build, `O(1)` query |
| Difference Array | Many range updates | `O(1)` per update, `O(n)` to finalize |
| Prefix XOR / Modular | Range XOR or divisibility checks | `O(n)` |

<br>

## Common Pitfalls

- Mixing up `prefix[R] - prefix[L]` with the correct `prefix[R + 1] - prefix[L]`. The padded `prefix[0] = 0` exists specifically to avoid this off-by-one.
- Forgetting `seen = {0: 1}` in the hash map pattern, which silently undercounts subarrays starting at index 0.
- Using prefix sum on an array that changes often. Rebuild cost is `O(n)` per change, use a Fenwick Tree or Segment Tree instead.
- Trying to apply prefix sum to max or min. These have no inverse, so subtraction can't undo them, range-max queries need a different structure entirely.

<br>

## Practice Problems (LeetCode)

Recognizing "this is a prefix sum problem" is the key step in each of these. No solutions here, just the list to practice against, ordered Easy to Hard.

### Easy

- Running Sum of 1D Array (LeetCode 1480)
- Range Sum Query - Immutable (LeetCode 303)
- Find Pivot Index (LeetCode 724)
- Find the Middle Index in Array (LeetCode 1991)
- Minimum Value to Get Positive Step by Step Sum (LeetCode 1413)
- Left and Right Sum Differences (LeetCode 2574)

### Medium

- Subarray Sum Equals K (LeetCode 560)
- Continuous Subarray Sum (LeetCode 523)
- Subarray Sums Divisible by K (LeetCode 974)
- Contiguous Array (LeetCode 525)
- Product of Array Except Self (LeetCode 238)
- Count Number of Nice Subarrays (LeetCode 1248)
- Range Sum Query 2D - Immutable (LeetCode 304)
- Binary Subarrays With Sum (LeetCode 930)
- Matrix Block Sum (LeetCode 1314)
- Corporate Flight Bookings (LeetCode 1109)
- Car Pooling (LeetCode 1094)
- Path Sum III (LeetCode 437)
- XOR Queries of a Subarray (LeetCode 1310)
- Find Kth Largest XOR Coordinate Value (LeetCode 1738)
- Longest Well-Performing Interval (LeetCode 1124)

### Hard

- Shortest Subarray with Sum at Least K (LeetCode 862)
- Max Sum of Rectangle No Larger Than K (LeetCode 363)
- Number of Submatrices That Sum to Target (LeetCode 1074)
- Count of Range Sum (LeetCode 327)
- Maximum Sum of 3 Non-Overlapping Subarrays (LeetCode 689)
