# Longest Consecutive Sequence

`Amazon` • `Google` • `Facebook` • `Microsoft` • `Apple` • `Bloomberg` • `Uber` • `Spotify` • `Oracle`
<br>

## Problem Statement

Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence.

You must write an algorithm that runs in **O(n)** time.

## Examples

**Example 1:**
```
Input:  nums = [100, 4, 200, 1, 3, 2]
Output: 4
Explanation: The longest consecutive elements sequence is [1, 2, 3, 4]. Therefore its length is 4.
```

**Example 2:**
```
Input:  nums = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]
Output: 9
```

**Example 3:**
```
Input:  nums = [1, 0, 1, 2]
Output: 3
```

## Constraints

- `0 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`

<br><br>

## Approach 1: Brute Force

### Intuition

For every number in the array, treat it as a potential start of a sequence and keep checking if the next consecutive number (`num + 1`, `num + 2`, ...) exists in the array. Track the maximum length found across all starting points.

### Solution

```python
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        max_len = 0

        for num in nums:
            current = num
            length = 1

            while current + 1 in nums:
                current += 1
                length += 1

            max_len = max(max_len, length)

        return max_len
```

### Complexity Analysis

| | Complexity |
|---|---|
| Time | O(n^2) |
| Space | O(1) |

The `in nums` check on a list is O(n), and it runs inside a loop over all elements, giving a worst-case O(n^2) overall.

### Problem with this Approach

Every membership check (`current + 1 in nums`) scans the entire list linearly. For a fully consecutive array like `[1, 2, 3, ..., n]`, the inner while loop runs O(n) times for the very first element, making the total time O(n^2). This will **TLE** on large inputs and violates the O(n) constraint.

**What can we do better?** The bottleneck is the linear membership check. If we could check whether a number exists in O(1), we would eliminate the inner scan entirely. A hash set gives us exactly that.

<br><br>

## Approach 2: Sorting

### Intuition

Sort the array so that consecutive numbers become adjacent. Then a single linear pass is enough to count streaks: if `nums[i] == nums[i-1] + 1`, extend the current streak; if they are equal, skip (duplicate); otherwise reset.

### Solution

```python
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        if not nums:
            return 0

        nums.sort()
        longest = 1
        current = 1

        for i in range(1, len(nums)):
            if nums[i] == nums[i - 1]:
                continue                        # skip duplicates
            elif nums[i] == nums[i - 1] + 1:
                current += 1                   # extend streak
            else:
                longest = max(longest, current)
                current = 1                    # reset streak

        return max(longest, current)
```

### Complexity Analysis

| | Complexity |
|---|---|
| Time | O(n log n) |
| Space | O(1) if sorting in-place, O(n) otherwise |

### Problem with this Approach

Sorting costs O(n log n), which violates the strict O(n) time requirement stated in the problem. While this solution is clean and would pass most online judges, it is **not acceptable** in interviews where the O(n) constraint is explicitly enforced.

**What can we do better?** We do not actually need the array sorted. We just need to know, for any given number, whether its predecessor exists. A hash set answers that in O(1) and lets us avoid sorting altogether.

<br><br>

## Approach 3: Hash Set (Optimal)

### Intuition

The key observation is: a number `x` is the **start** of a consecutive sequence if and only if `x - 1` is not present in the array. If `x - 1` existed, then `x` would simply be a continuation of that earlier sequence, not a new one.

So the algorithm is:

1. Load all numbers into a hash set (O(1) lookups, duplicates removed automatically).
2. Iterate over the set. For each number, check whether `num - 1` is absent. If it is absent, `num` is a sequence start.
3. From that start, keep incrementing (`num + 1`, `num + 2`, ...) and counting as long as the next number exists in the set.
4. Track the maximum count seen.

### Why is this O(n) and not O(n^2)?

The inner `while` loop looks like it could blow up, but each number is visited **at most twice**: once in the outer loop and at most once in the inner while loop of the sequence it belongs to. Because we only enter the while loop from a sequence start, and each element belongs to exactly one sequence, the total number of inner iterations across all outer iterations is at most n. The overall complexity is therefore O(n).

### Solution

```python
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        if not nums:
            return 0

        num_set = set(nums)   # O(n) to build, O(1) lookups
        longest = 0

        for num in num_set:
            # Only start counting from the beginning of a sequence
            if num - 1 not in num_set:
                current_num = num
                current_streak = 1

                while current_num + 1 in num_set:
                    current_num += 1
                    current_streak += 1

                longest = max(longest, current_streak)

        return longest
```

### Dry Run

Input: `[100, 4, 200, 1, 3, 2]`

Set: `{1, 2, 3, 4, 100, 200}`

| num | num - 1 in set? | Sequence explored | Streak |
|-----|-----------------|-------------------|--------|
| 100 | 99 not in set   | 100               | 1      |
| 4   | 3 in set        | (skipped)         | -      |
| 200 | 199 not in set  | 200               | 1      |
| 1   | 0 not in set    | 1, 2, 3, 4        | 4      |
| 3   | 2 in set        | (skipped)         | -      |
| 2   | 1 in set        | (skipped)         | -      |

Longest = **4**

### Complexity Analysis

| | Complexity |
|---|---|
| Time | O(n) |
| Space | O(n) |

Building the set is O(n). The outer loop runs over all n elements. The inner while loop, summed across all sequence starts, also runs at most n iterations total. Space is O(n) for the set.

<br><br>

## Summary

| Approach | Time | Space | Meets O(n) Requirement |
|---|---|---|---|
| Brute Force | O(n^2) | O(1) | No |
| Sorting | O(n log n) | O(1) / O(n) | No |
| Hash Set (Optimal) | O(n) | O(n) | Yes |

The hash set approach is the standard expected answer in interviews. The core insight is identifying sequence starts by checking for the absence of a predecessor, which ensures each element is processed at most twice regardless of the input structure.