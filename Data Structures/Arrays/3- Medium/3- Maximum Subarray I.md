# Maximum Subarray I

`Google` • `Amazon` • `Microsoft` • `Apple` • `Meta` • `LinkedIn` • `Uber` • `Bloomberg` • `Goldman Sachs` • `Tesla`

**Topic:** Kadane's Algorithm

## Problem Statement

Given an integer array `nums`, find the subarray with the largest sum, and return its sum.

A **subarray** is a contiguous and non-empty sequence of elements within an array.

**Examples**

**Example 1:**
```
Input:  nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
Output: 6
Explanation: The subarray [4, -1, 2, 1] has the largest sum = 6.
```

**Example 2:**
```
Input:  nums = [1]
Output: 1
Explanation: The subarray [1] has the largest sum = 1.
```

**Example 3:**
```
Input:  nums = [5, 4, -1, 7, 8]
Output: 23
Explanation: The subarray [5, 4, -1, 7, 8] has the largest sum = 23.
```

**Constraints**
- `1 <= nums.length <= 10^5`
- `-10^4 <= nums[i] <= 10^4`

<br><br>

## Approach 1: Brute Force (Naive)

**Intuition**

The most straightforward approach is to consider every possible subarray. Use three nested loops: the first two pick the start and end indices `(i, j)`, and the third sums all elements between them. Track the maximum sum seen across all subarrays.

**Solution**

```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        max_sum = nums[0]

        for i in range(len(nums)):
            for j in range(i, len(nums)):
                current_sum = sum(nums[i:j+1])
                max_sum = max(max_sum, current_sum)

        return max_sum
```

**Explanation**

We start `max_sum` at `nums[0]` to correctly handle all-negative arrays, where the answer is the largest (least negative) single element. For every pair `(i, j)`, we compute the full subarray sum using a slice and compare it against the running maximum.

**Complexity**

| | |
|---|---|
| Time | O(n^3) |
| Space | O(1) |

**Problem with this approach**

Three levels of work (two loops plus a full slice summation inside) push the complexity to O(n^3). For `n = 10^5` this is completely infeasible. The obvious waste here is recomputing the subarray sum from scratch every time. We can eliminate that by accumulating the sum incrementally as we extend the inner loop, which is what Approach 2 does.

<br><br>

## Approach 2: Optimized Brute Force (Prefix Sum)

**Intuition**

In the pure brute force, the innermost logic recomputes the subarray sum from scratch for every `(i, j)` pair. We can eliminate that redundancy by noticing that the sum of `nums[i..j]` is just the sum of `nums[i..j-1]` plus `nums[j]`. By accumulating `current_sum` as we extend `j`, we bring the work per pair down to O(1), cutting the overall complexity from O(n^3) to O(n^2).

This is still two nested loops, but it removes the hidden inner summation and is the natural stepping stone toward recognizing the pattern that leads to Kadane's Algorithm.

**Solution**

```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        max_sum = nums[0]

        for i in range(len(nums)):
            current_sum = 0
            for j in range(i, len(nums)):
                current_sum += nums[j]
                max_sum = max(max_sum, current_sum)

        return max_sum
```

**Explanation**

For every starting index `i`, we reset `current_sum` to zero and then walk `j` forward, adding one element at a time. Because we never recompute the sum from scratch, each inner iteration is O(1). We compare against `max_sum` after every extension so no subarray sum is missed.

**Complexity**

| | |
|---|---|
| Time | O(n^2) |
| Space | O(1) |

**Problem with this approach**

Even though we removed the redundant inner summation, we still have two nested loops. For `n = 10^5` this is roughly 5 billion iterations, which will TLE. The deeper issue is that we are still evaluating every possible subarray independently. What if we could use information from the previous step to make a constant-time decision about whether to extend or discard the current subarray? That is exactly what Kadane's Algorithm does.

<br><br>

## Approach 3: Kadane's Algorithm (Optimal)

**Intuition**

The key insight is this: at every position in the array, we face exactly one decision. Do we extend the current running subarray to include this element, or do we discard everything accumulated so far and start a fresh subarray from this element?

We should extend if the running sum is positive, because adding a positive prefix will only make the current element's contribution larger. We should reset if the running sum has gone negative, because carrying a negative prefix would strictly decrease any future subarray sum. A negative prefix is dead weight and should always be dropped.

This gives us a clean single-pass algorithm. Maintain two variables:

- `summ`: the best subarray sum ending at the current index.
- `max_sum`: the best subarray sum seen anywhere so far.

At each step, add the current element to `summ`, update `max_sum` if `summ` is a new maximum, and then reset `summ` to zero if it has gone negative.

**Solution**

```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        max_sum = nums[0]
        summ = 0

        for num in nums:
            summ += num
            max_sum = max(max_sum, summ)

            if summ < 0:
                summ = 0

        return max_sum
```

**Explanation**

We initialize `max_sum` to `nums[0]` rather than negative infinity so that an all-negative array returns the largest (least negative) single element, which is the correct answer since the subarray must contain at least one element.

`summ` starts at zero. For each `num`:

1. We add `num` to `summ`, extending the current subarray.
2. We check whether this running total beats our recorded `max_sum` and update accordingly.
3. If `summ` has dropped below zero, we reset it to zero. This is equivalent to saying: "discard the current subarray and start fresh from the next element."

The comparison `max_sum = max(max_sum, summ)` happens before the reset, which is important. It ensures we capture the actual sum at the current position before potentially throwing it away.

**Walkthrough on Example 1:** `nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]`

| Step | num | summ (after add) | max_sum | Reset? |
|------|-----|-----------------|---------|--------|
| 1    | -2  | -2              | -2      | Yes (summ = 0) |
| 2    | 1   | 1               | 1       | No     |
| 3    | -3  | -2              | 1       | Yes (summ = 0) |
| 4    | 4   | 4               | 4       | No     |
| 5    | -1  | 3               | 4       | No     |
| 6    | 2   | 5               | 5       | No     |
| 7    | 1   | 6               | 6       | No     |
| 8    | -5  | 1               | 6       | No     |
| 9    | 4   | 5               | 6       | No     |

Final answer: `6`. The subarray `[4, -1, 2, 1]` produced the maximum.

**Complexity**

| | |
|---|---|
| Time | O(n) |
| Space | O(1) |

We make a single pass through the array and use only two variables regardless of input size. This is optimal: you must read every element at least once, so O(n) time and O(1) space is the best achievable.

<br><br>

## Summary

| Approach | Time | Space | Notes |
|---|---|---|---|
| Brute Force (Naive) | O(n^3) | O(1) | Completely infeasible for large inputs |
| Optimized Brute Force | O(n^2) | O(1) | Better, but still too slow |
| Kadane's Algorithm | O(n) | O(1) | Optimal. Recommended answer |

**Recommended approach for interviews:** Kadane's Algorithm (Approach 3). Start by walking through the brute force progression to demonstrate structured thinking, then derive Kadane's by highlighting the key observation that a negative running sum is always worth discarding. This shows both problem-solving depth and the ability to optimize iteratively.