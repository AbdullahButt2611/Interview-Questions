# 1493. Longest Subarray of 1's After Deleting One Element

## Problem Statement

Given a binary array `nums`, you should delete **one element** from it. Return the size of the longest non-empty subarray containing only 1's in the resulting array. Return 0 if there is no such subarray.

**Example 1:**

```
Input: nums = [1,1,0,1]
Output: 3
Explanation: After deleting the number in position 2, [1,1,1] contains 3 numbers with value of 1's.
```

**Example 2:**

```
Input: nums = [0,1,1,1,0,1,1,0,1]
Output: 5
Explanation: After deleting the number in position 4, [0,1,1,1,1,1,0,1] longest subarray with value of 1's is [1,1,1,1,1].
```

**Example 3:**

```
Input: nums = [1,1,1]
Output: 2
Explanation: You must delete one element.
```

**Constraints:**

* 1 <= nums.length <= 10^5
* nums[i] is either 0 or 1

<br><br>

## Approach 1: Brute Force

**Idea:** Try deleting each element one by one, then calculate the longest consecutive 1's in the new array. Keep track of the maximum length.

**Code:**

```python
def longestSubarray(nums):
    n = len(nums)
    max_len = 0

    for i in range(n):
        # Create a new array without nums[i]
        temp = nums[:i] + nums[i+1:]

        # Count the longest consecutive 1's in temp
        current_len = 0
        temp_max = 0
        for num in temp:
            if num == 1:
                current_len += 1
                temp_max = max(temp_max, current_len)
            else:
                current_len = 0

        max_len = max(max_len, temp_max)

    return max_len
```

**Explanation:**

* Loop through every index and "delete" that element.
* Count the longest consecutive 1's in the new array.
* Update the maximum length.

**Time Complexity:** O(n²) — Too slow for large arrays.

**Space Complexity:** O(n) — For creating temporary arrays.

**Problem with this approach:**

* Inefficient for large arrays (n = 10^5).
* Creates many temporary arrays, wasting memory.

<br><br>

## Approach 2: Sliding Window

**Idea:**

* Keep a window that contains at most one zero.
* Expand the window until there are more than one zero, then shrink it from the left.
* Window length minus one gives the result because we remove one element.

**Code:**

```python
def longestSubarray(nums):
    left = 0
    zeros_count = 0
    max_len = 0

    for right in range(len(nums)):
        if nums[right] == 0:
            zeros_count += 1

        # Shrink window if more than one zero
        while zeros_count > 1:
            if nums[left] == 0:
                zeros_count -= 1
            left += 1

        # Update max length (we always delete one element)
        max_len = max(max_len, right - left)

    return max_len
```

**Explanation:**

* `left` and `right` define the sliding window.
* `zeros_count` keeps track of zeros in the window.
* If zeros exceed 1, move `left` to reduce zeros.
* Window length minus one gives the answer.

**Time Complexity:** O(n) — Each element visited at most twice.

**Space Complexity:** O(1) — Constant extra space.

**Advantage:**

* Works efficiently for large arrays.
* No extra arrays are created.
