# Maximum Subarray II

`Google` • `Amazon` • `Microsoft` • `Apple` • `Meta` • `LinkedIn` • `Uber` • `Bloomberg` • `Goldman Sachs` • `Tesla`

**Topic:** Kadane's Algorithm

## Problem Statement

Given an integer array `nums`, find the subarray with the largest sum, and return **the subarray itself**.

A **subarray** is a contiguous and non-empty sequence of elements within an array.

**Examples**

**Example 1:**
```
Input:  nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
Output: [4, -1, 2, 1]
Explanation: The subarray [4, -1, 2, 1] has the largest sum = 6.
```

**Example 2:**
```
Input:  nums = [1]
Output: [1]
Explanation: The only subarray is [1] with sum = 1.
```

**Example 3:**
```
Input:  nums = [5, 4, -1, 7, 8]
Output: [5, 4, -1, 7, 8]
Explanation: The subarray [5, 4, -1, 7, 8] has the largest sum = 23.
```

**Constraints**
- `1 <= nums.length <= 10^5`
- `-10^4 <= nums[i] <= 10^4`

<br><br>

## Approach: Kadane's Algorithm with Index Tracking

**Intuition**

This is a direct extension of the classic Maximum Subarray problem. In that version, we only needed to track the running sum and the global maximum. Here, we also need to know exactly which subarray produced that maximum, so we must track indices.

The core logic of Kadane's Algorithm remains unchanged: accumulate a running sum, reset it to zero whenever it goes negative, and record the global maximum whenever we find a better one. The only addition is that we now maintain three index pointers:

- `start`: the starting index of the current candidate subarray being built. It updates every time we reset (i.e., every time `summ` was zero before adding the current element).
- `ans_start`: the starting index of the best subarray found so far.
- `ans_end`: the ending index of the best subarray found so far.

Whenever we find a new maximum sum, we lock in the current `start` as the new `ans_start` and the current index `i` as the new `ans_end`. At the very end, slicing `nums[ans_start : ans_end + 1]` gives us the answer.

**Solution**

```python
class Solution:
    def maxSubArray(self, nums):
        max_sum = nums[0]
        summ = 0

        start = 0
        ans_start = 0
        ans_end = 0

        for i, num in enumerate(nums):
            if summ == 0:
                start = i
            summ += num

            if summ > max_sum:
                max_sum = summ
                ans_start = start
                ans_end = i

            if summ < 0:
                summ = 0

        return nums[ans_start : ans_end + 1]
```

**Explanation**

We initialize `max_sum` to `nums[0]` so that an all-negative array correctly returns the single largest element rather than an empty result. `summ` starts at zero to represent an empty running subarray before we begin.

The check `if summ == 0` at the top of the loop is the key mechanism for tracking `start`. It fires in two situations: at the very beginning of the array (since `summ` is initialized to zero), and right after a reset (since a reset sets `summ` back to zero). In both cases, the next element we are about to add is the beginning of a fresh candidate subarray, so we assign `start = i`.

The update `if summ > max_sum` uses strict greater-than (not `>=`). This means we only lock in a new answer when we genuinely improve, which preserves the leftmost maximum subarray in case of ties.

After the loop, `nums[ans_start : ans_end + 1]` reconstructs the answer from the tracked indices. The `+ 1` accounts for Python's exclusive upper bound in slicing.

**Walkthrough on Example 1:** `nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]`

| i | num | summ==0? | start | summ (after add) | max_sum | ans_start | ans_end | Reset? |
|---|-----|----------|-------|-----------------|---------|-----------|---------|--------|
| 0 | -2  | Yes      | 0     | -2              | -2      | 0         | 0       | Yes (summ=0) |
| 1 | 1   | Yes      | 1     | 1               | 1       | 1         | 1       | No     |
| 2 | -3  | No       | 1     | -2              | 1       | 1         | 1       | Yes (summ=0) |
| 3 | 4   | Yes      | 3     | 4               | 4       | 3         | 3       | No     |
| 4 | -1  | No       | 3     | 3               | 4       | 3         | 3       | No     |
| 5 | 2   | No       | 3     | 5               | 5       | 3         | 5       | No     |
| 6 | 1   | No       | 3     | 6               | 6       | 3         | 6       | No     |
| 7 | -5  | No       | 3     | 1               | 6       | 3         | 6       | No     |
| 8 | 4   | No       | 3     | 5               | 6       | 3         | 6       | No     |

Final `ans_start = 3`, `ans_end = 6`.
Return `nums[3:7]` = `[4, -1, 2, 1]`.

**Complexity**

| | |
|---|---|
| Time | O(n) |
| Space | O(1) |

A single pass through the array with only a fixed number of scalar variables. The output slice itself takes O(k) where `k` is the length of the result subarray, but no additional auxiliary space is used during the computation.

<br><br>

## Summary

| | |
|---|---|
| Algorithm | Kadane's Algorithm with Index Tracking |
| Time Complexity | O(n) |
| Space Complexity | O(1) |
| Key Difference from Classic Version | Track `start`, `ans_start`, and `ans_end` to reconstruct the subarray |

**Note for interviews:** If asked this as a follow-up to the classic Maximum Subarray problem, emphasize that the algorithmic complexity does not change at all. The only addition is three integer pointers that let us reconstruct the window after a single pass. The reset condition (`summ == 0`) serves double duty as the trigger to advance the `start` pointer.