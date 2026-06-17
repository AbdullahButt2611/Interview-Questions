# Pivot Index
`LeetCode 75`

## Problem

Given an array of integers `nums`, return the **pivot index**.

The pivot index is the index where the sum of all the numbers on the left is the same as the sum of all the numbers on the right.

If the index is at the left edge, the left sum is `0`. If the index is at the right edge, the right sum is `0`.

Return the **leftmost** pivot index. If no index matches, return `-1`.

<br>

## Examples

**Example 1**

```
Input: nums = [1,7,3,6,5,6]
Output: 3
```

Left sum = 1 + 7 + 3 = 11
Right sum = 5 + 6 = 11

**Example 2**

```
Input: nums = [1,2,3]
Output: -1
```

No index has equal left and right sums.

**Example 3**

```
Input: nums = [2,1,-1]
Output: 0
```

Left sum = 0
Right sum = 1 + -1 = 0

<br><br>

# Approaches and Solutions

## Approach 1: Using Prefix Sum Array

### Idea

We build a prefix sum list. This helps us get left and right sums for any index fast.

### Code

```python
class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        total_length = len(nums)

        cum_sum = [0] * total_length
        cum_sum[0] = nums[0]

        for i in range(1, total_length):
            cum_sum[i] = cum_sum[i-1] + nums[i]

        for i in range(total_length):
            left_sum = 0
            right_sum = 0

            if i != 0:
                left_sum = cum_sum[i-1]

            if i != total_length - 1:
                right_sum = cum_sum[total_length - 1] - left_sum - nums[i]

            if left_sum == right_sum:
                return i

        return -1
```

### Notes

This works fine but uses extra space equal to the size of the list.

<br><br>

## Approach 2: Single Pass Without Extra Space

### Idea

Instead of a prefix list, we use the total sum. For each index, we track the left sum and check if:

```
left_sum == total_sum - left_sum - nums[i]
```

### Code

```python
class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        total = sum(nums)
        left_sum = 0

        for i, val in enumerate(nums):
            if left_sum == total - left_sum - val:
                return i
            left_sum += val

        return -1
```

### Notes

This avoids extra space and keeps the same time cost. This is the cleaner way to solve the task.

<br><br>

# Final Notes

Both methods work in the same time cost, but the second method is simpler and uses less memory. This makes it the better option for most use cases.
