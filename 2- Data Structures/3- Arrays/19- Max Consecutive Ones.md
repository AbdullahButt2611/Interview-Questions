# Max Consecutive Ones
`LeetCode 75`

## Problem Statement

Given a binary array `nums` and an integer `k`, return the maximum number of consecutive `1`s in the array if you can flip at most `k` `0`s.

### Example 1:

Input: `nums = [1,1,1,0,0,0,1,1,1,1,0]`, `k = 2`
Output: `6`
Explanation: Flipping two `0`s in the sequence gives the longest subarray of `1`s as `[1,1,1,0,0,1,1,1,1,1,1]`.

### Example 2:

Input: `nums = [0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1]`, `k = 3`
Output: `10`
Explanation: Flipping three `0`s results in the longest subarray of `1`s.

### Constraints:

* `1 <= nums.length <= 10^5`
* `nums[i]` is either `0` or `1`.
* `0 <= k <= nums.length`

<br><br>

## Approach 1: Sliding Window

The key insight is to realize that we need the longest subarray containing at most `k` zeros. This can be efficiently done using the sliding window technique.

### Steps:

1. Use two pointers, `left` and `right`, to represent the current window.
2. Keep a count of zeros inside the window (`zeroCount`).
3. Expand the window by moving `right` and increase `zeroCount` whenever a `0` is encountered.
4. If `zeroCount` exceeds `k`, shrink the window from the left until `zeroCount <= k`.
5. Keep track of the maximum window length during this process.

### Python Implementation:

```python
class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        left = 0
        maxLen = 0
        zeroCount = 0
        
        # Iterate through the array with the right pointer
        for right in range(len(nums)):
            # Count zeros in the current window
            if nums[right] == 0:
                zeroCount += 1

            # Shrink window from the left if zeroCount exceeds k
            while zeroCount > k:
                if nums[left] == 0:
                    zeroCount -= 1
                left += 1

            # Update maximum length
            maxLen = max(maxLen, right - left + 1)

        return maxLen
```

### Explanation:

* The `right` pointer expands the window, while the `left` pointer shrinks it when necessary.
* `zeroCount` tracks how many zeros are in the current window.
* `maxLen` stores the largest window length where zeros <= k.
* Time complexity: **O(n)**, Space complexity: **O(1)**

<br><br>

## Approach 2: Brute Force (Inefficient)

One could consider checking all subarrays and counting zeros in each subarray. If zeros <= k, update the maximum length.

### Steps:

1. Iterate through all possible subarrays.
2. Count zeros in each subarray.
3. If zeros <= k, calculate subarray length and update maximum.

### Issues with this approach:

* Checking all subarrays takes **O(n^2)** time.
* Counting zeros in each subarray adds more overhead.
* Not feasible for large arrays (n up to 10^5).

This reinforces why sliding window is optimal for this type of problem.

<br><br>

## Summary

* The problem reduces to finding the longest subarray with at most `k` zeros.
* Sliding window is the optimal approach with **O(n)** time complexity.
* Brute force is inefficient for large input.
* Key points to remember:

  * Expand window using `right` pointer.
  * Track zeros with `zeroCount`.
  * Shrink window with `left` pointer when zeros > k.
  * Update `maxLen` at every valid window.

This completes the professional markdown entry for the question, ready to add to your repository.
