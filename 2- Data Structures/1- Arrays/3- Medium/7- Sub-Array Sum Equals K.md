# Subarray Sum Equals K

`Meta` • `Amazon` • `Google` • `Microsoft` • `Bloomberg` • `Apple` • `Adobe` • `Uber` • `TikTok` • `Goldman Sachs`

**Topic:** Prefix Sum

<br>

## Problem Statement

Given an integer array `nums` and an integer `k`, return the **total number of subarrays** whose sum equals `k`.

A **subarray** is a contiguous and non-empty sequence of elements within an array.

**Examples**

**Example 1:**
```
Input:  nums = [1, 1, 1], k = 2
Output: 2
Explanation: The subarrays [1, 1] (indices 0..1) and [1, 1] (indices 1..2) both sum to 2.
```

**Example 2:**
```
Input:  nums = [1, 2, 3], k = 3
Output: 2
Explanation: The subarrays [1, 2] and [3] both sum to 3.
```

**Example 3:**
```
Input:  nums = [1, -1, 0], k = 0
Output: 3
Explanation: The subarrays [1, -1], [0], and [1, -1, 0] all sum to 0.
```

**Constraints**
- `1 <= nums.length <= 2 * 10^4`
- `-1000 <= nums[i] <= 1000`
- `-10^7 <= k <= 10^7`

Note that `nums` can contain **negative numbers and zeros**. This single detail rules out a few intuitive shortcuts, as the approaches below will show.

<br><br>

## Approach 1: Brute Force (recompute every subarray sum)

**Intuition**

The most direct reading of the problem is to enumerate every possible subarray and add up its elements. A subarray is defined by a start index and an end index, so we loop over all valid `(start, end)` pairs. For each pair we run a third loop to compute the sum of that slice from scratch, then compare it against `k`.

**Solution**

```python
class Solution:
    def subarraySum(self, nums, k):
        n = len(nums)
        count = 0

        for start in range(n):
            for end in range(start, n):
                total = 0
                for i in range(start, end + 1):
                    total += nums[i]
                if total == k:
                    count += 1

        return count
```

**Explanation**

The outer two loops pick every `(start, end)` combination, which represents one unique subarray. The innermost loop recomputes the sum of `nums[start..end]` every single time. Whenever that sum matches `k`, we increment the counter. It is correct for positives, negatives, and zeros because it never assumes anything about the values, it just adds them up.

**What we can improve**

The fatal weakness is speed. There are roughly `n^2` subarrays, and for each one we spend up to `n` steps recomputing the sum, giving `O(n^3)` time. With `n` up to `2 * 10^4`, that is on the order of `8 * 10^12` operations, which will time out.

The waste is easy to spot: when we move `end` forward by one position, we throw away the sum we just computed and start adding from `start` again. We should reuse that work instead of discarding it.

**Complexity**

| | |
|---|---|
| Time | O(n^3) |
| Space | O(1) |

<br><br>

## Approach 2: Running Sum (extend the window instead of recomputing)

**Intuition**

We keep the idea of fixing a `start` index, but instead of recomputing the sum for every `end`, we carry a running total. As `end` slides to the right by one, we simply add the new element to the total we already have. This removes the innermost loop entirely.

**Solution**

```python
class Solution:
    def subarraySum(self, nums, k):
        n = len(nums)
        count = 0

        for start in range(n):
            total = 0
            for end in range(start, n):
                total += nums[end]
                if total == k:
                    count += 1

        return count
```

**Explanation**

For each `start`, the variable `total` accumulates the sum of `nums[start..end]` as `end` advances. Because we only add the newest element each step, every subarray sum is computed in constant time rather than by rescanning. The correctness argument is the same as before, we still visit every subarray, we just compute its sum more cheaply.

**What we can improve**

This is a real gain, dropping us from `O(n^3)` to `O(n^2)`, but it is still quadratic. For `n = 2 * 10^4` that is about `4 * 10^8` operations, which is borderline and can still be too slow depending on the limits.

The deeper issue is that we are still examining every subarray one by one. To go faster we need to stop enumerating subarrays explicitly and instead answer the question with a mathematical relationship between sums. That is where prefix sums come in.

A tempting wrong turn here is the sliding window technique that works for problems like "minimum subarray of sum at least k". That technique relies on the sum only growing as the window expands, which is only true when all values are non-negative. Since `nums` can contain negatives and zeros, growing the window can shrink the sum, so sliding window does not apply to this problem.

**Complexity**

| | |
|---|---|
| Time | O(n^2) |
| Space | O(1) |

<br><br>

## Approach 3: Prefix Sum with a Hash Map (optimal)

**Intuition**

Define the prefix sum `P(i)` as the sum of all elements from the start of the array up to index `i`. The sum of any subarray from index `i + 1` to `j` is then `P(j) - P(i)`.

We want that subarray sum to equal `k`:

```
P(j) - P(i) = k
P(i) = P(j) - k
```

So while we scan the array and track the current prefix sum `P(j)`, the number of valid subarrays ending at `j` is exactly the number of earlier prefix sums equal to `P(j) - k`. If we store how many times each prefix sum has occurred so far in a hash map, we can look that count up in constant time and never re-scan the array.

**Solution**

```python
class Solution:
    def subarraySum(self, nums, k):
        count = 0
        prefix_sum = 0
        seen = {0: 1}  # one empty prefix, so subarrays starting at index 0 are counted

        for num in nums:
            prefix_sum += num
            count += seen.get(prefix_sum - k, 0)
            seen[prefix_sum] = seen.get(prefix_sum, 0) + 1

        return count
```

**Explanation**

We walk through the array once, maintaining `prefix_sum` as the running total up to the current element. At each step we ask how many earlier positions had a prefix sum of `prefix_sum - k`. Each such position marks the start of a subarray that ends here and sums to exactly `k`, so we add that count to the answer. We then record the current `prefix_sum` in the map for future elements to reference.

The map is seeded with `{0: 1}` to represent the empty prefix before the array begins. This is what lets a subarray that starts at index `0` be counted, since for such a subarray the matching earlier prefix sum is `0`.

Because the map stores counts rather than just presence, repeated prefix sums (which happen naturally with zeros and negatives) are all tallied correctly. This is the part that a set-based version would get wrong.

**Walkthrough on Example 1:** `nums = [1, 1, 1], k = 2`

| num | prefix_sum | look for (prefix_sum - k) | count added | map after step |
|-----|------------|---------------------------|-------------|----------------|
| 1   | 1          | -1 (not present)          | 0           | {0:1, 1:1} |
| 1   | 2          | 0 (present once)          | 1           | {0:1, 1:1, 2:1} |
| 1   | 3          | 1 (present once)          | 1           | {0:1, 1:1, 2:1, 3:1} |

Final count is `2`, which matches the expected output.

**Why this is optimal**

We touch each element exactly once and do constant work per element, so the time is linear. We cannot do better than reading every element at least once, so `O(n)` time is the best possible for this problem. The trade-off is the hash map, which costs `O(n)` space in the worst case where every prefix sum is distinct.

**Complexity**

| | |
|---|---|
| Time | O(n) |
| Space | O(n) |

<br><br>

## Summary

| | |
|---|---|
| Best Algorithm | Prefix Sum with a Hash Map |
| Time Complexity | O(n) |
| Space Complexity | O(n) |
| Key Insight | `P(j) - P(i) = k` turns a subarray search into a lookup of seen prefix sums |
| Common Trap | Sliding window fails because negatives break the "sum grows with the window" assumption |

**Note for interviews:** The progression from brute force to the hash map version is the whole story here, so state it out loud. Start by naming the `O(n^3)` and `O(n^2)` ideas to show you see the search space, then pivot to the prefix sum identity once you have earned it. Two small details separate a correct answer from a buggy one: seed the map with `{0: 1}` so subarrays starting at index `0` are counted, and store counts rather than just presence so duplicate prefix sums from zeros and negatives are handled correctly.