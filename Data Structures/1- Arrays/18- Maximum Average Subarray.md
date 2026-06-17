# Maximum Average Subarray I
`LeetCode 75`

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

<br>

## Approach 1: Brute Force (O(n*k))

### Idea

Check every possible subarray of size `k`, calculate its sum, find the one with the highest average.

This is simple and easy to understand but inefficient for large arrays.

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

* Loop through all subarrays of length `k`.
* Compute the sum each time.
* Keep track of the maximum average found.

### Why this isn’t great

For large `n` and `k`, this becomes very slow since it recalculates overlapping sums repeatedly.

**Time complexity:** O(n * k)
**Space complexity:** O(1)

<br>

## Approach 2: Sliding Window (Optimal)

### Idea

Reuse the previous window’s sum instead of recalculating from scratch.
When moving from one window to the next:

```
new_sum = old_sum - nums[i - k] + nums[i]
```

This keeps the sum updated in constant time.

### Code

Easier version of the code is
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
            sum -= nums[i-k]
            sum += nums[i]
            if sum / k > max:
                max = sum / k
        return max
```


Cleaner Version of the same code is

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

* Compute sum of the first window (first `k` elements).
* For each step, remove the element leaving the window and add the new one.
* Keep track of the maximum sum seen so far.

### Why this is the best

* Uses constant space.
* Single pass through the array.
* Clean and easy to read.

**Time complexity:** O(n)
**Space complexity:** O(1)

<br>

## Summary

| Approach       | Description                          | Time   | Space |
| -------------- | ------------------------------------ | ------ | ----- |
| Brute Force    | Check every subarray and compute sum | O(n*k) | O(1)  |
| Sliding Window | Reuse previous window’s sum          | O(n)   | O(1)  |
