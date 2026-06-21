# Maximum Average Subarray I

`Amazon` • `Bloomberg` • `Goldman Sachs` • `Google` • `Meta` • `Microsoft` • `Oppo` • `Uber` • `Yandex` • `TakeUForward`

<br>

## Problem Statement

You are given an integer array `nums` consisting of `n` elements, and an integer `k`.

Find a contiguous subarray whose length is equal to `k` that has the maximum average value and return this value. Any answer with a calculation error less than `10^-5` will be accepted.

**Example 1:**

```python
Input: nums = [1,12,-5,-6,50,3], k = 4
Output: 12.75000
Explanation: Maximum average is (12 - 5 - 6 + 50) / 4 = 51 / 4 = 12.75
```

**Example 2:**

```python
Input: nums = [5], k = 1
Output: 5.00000
```

**Constraints:**

```
1 <= k <= n <= 10^5
-10^4 <= nums[i] <= 10^4
```

<br><br>

## Approach 1: Brute Force

### Idea

Check every subarray of size `k`, sum its elements, and track the highest average found.

### Code

```python
class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        n = len(nums)
        max_avg = float('-inf')

        for i in range(n - k + 1):
            sub_sum = 0
            for j in range(i, i + k):
                sub_sum += nums[j]
            avg = sub_sum / k
            max_avg = max(max_avg, avg)

        return max_avg
```

### Explanation

* Loop through every starting index of a window of length `k`.
* Sum that window using an inner loop, then divide by `k` for the average.
* Track the maximum average seen so far.

**Time complexity:** O(n * k) \
**Space complexity:** O(1)

### The Problem With This Approach

Each new window overlaps the previous one by `k - 1` elements, but the sum is recomputed from scratch every time. This redundant work makes it too slow for large inputs (up to 10^5).

We need to reuse the previous window's sum instead of recalculating it.

<br><br>

## Approach 2: Sliding Window (Optimal)

### Idea

Since every subarray has the same length `k`, the one with the maximum sum also has the maximum average. So track sums instead of averages, and divide by `k` only once at the end.

Reuse the previous window's sum: subtract the element leaving the window and add the one entering it.

```
new_sum = old_sum - nums[i - k] + nums[i]
```

### Code

First version:

```python
class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        if k > len(nums):
            return 0.0

        sum = 0.0
        for i in range(k):
            sum += nums[i]
        max = sum / k

        for i in range(k, len(nums)):
            sum -= nums[i - k]
            sum += nums[i]
            if sum / k > max:
                max = sum / k
        return max
```

Cleaner version:

```python
class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        window_sum = sum(nums[:k])
        max_sum = window_sum

        for i in range(k, len(nums)):
            window_sum += nums[i] - nums[i - k]
            max_sum = max(max_sum, window_sum)

        return max_sum / k
```

### Explanation

* Compute the sum of the first window and set it as `max_sum`.
* Slide one element at a time: add the new element, subtract the old one.
* Track the maximum sum, then divide by `k` once at the end.

**Time complexity:** O(n) \
**Space complexity:** O(1)

### Why This Is The Best Approach

A single pass with constant work per step, no redundant recalculation, and it scales comfortably to n = 10^5.

<br><br>

## Summary

| Approach       | Description                  | Time   | Space |
| -------------- | ----------------------------- | ------ | ----- |
| Brute Force    | Recompute sum for every window | O(n*k) | O(1)  |
| Sliding Window | Reuse the previous window's sum | O(n)   | O(1)  |