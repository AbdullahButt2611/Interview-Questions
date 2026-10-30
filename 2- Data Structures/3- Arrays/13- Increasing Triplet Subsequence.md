# Increasing Triplet Subsequence

`LeetCode 75`

## Problem Statement

Given an integer array `nums`, return `true` if there exists a triple of indices `(i, j, k)` such that `i < j < k` **and** `nums[i] < nums[j] < nums[k]`. Otherwise, return `false`.

##### Example 1:

```python
Input: nums = [1, 2, 3, 4, 5]
Output: True
Explanation: Any triplet where i < j < k is valid.
```

##### Example 2:

```python
Input: nums = [5, 4, 3, 2, 1]
Output: False
Explanation: The numbers are in decreasing order, so no increasing triplet exists.
```

##### Example 3:

```python
Input: nums = [2, 1, 5, 0, 4, 6]
Output: True
Explanation: One valid triplet is (3, 4, 5), because nums[3] = 0 < nums[4] = 4 < nums[5] = 6.
```

### Constraints

* `1 <= nums.length <= 5 * 10^5`
* `-2^31 <= nums[i] <= 2^31 - 1`

### Follow-up

Can you solve this in **O(n)** time and **O(1)** space complexity?

<br><br>

## Approach 1: Brute Force (O(n³) Time)

### Idea

The most straightforward way is to check **every possible triplet** `(i, j, k)` and verify if they satisfy the conditions.

### Pseudocode

1. Loop through all indices `i`, `j`, `k` such that `i < j < k`.
2. Check if `nums[i] < nums[j] < nums[k]`.
3. If yes, return `True`.
4. If no triplet found, return `False`.

### Code

```python
class Solution:
    def increasingTriplet(self, nums: List[int]) -> bool:
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if nums[i] < nums[j] < nums[k]:
                        return True
        return False
```

### Explanation

This approach checks all combinations, ensuring that every triplet is tested. However, for large arrays (up to 500,000 elements), it’s **too slow**.

### Problem with this approach

* Time complexity: **O(n³)** — impractical for large input sizes.
* Space complexity: **O(1)** — no extra space used.

<br>

## Approach 2: Improved Using Prefix and Suffix Arrays
`(O(n) Time, O(n) Space)`

### Idea

We can precompute:

* The **minimum value to the left** of each index.
* The **maximum value to the right** of each index.

Then, for each index `j`, check if there exists a smaller number before it and a larger number after it.

### Steps

1. Create an array `left_min[i]` that stores the smallest number up to index `i`.
2. Create an array `right_max[i]` that stores the largest number from index `i` to the end.
3. For each `i`, if `left_min[i] < nums[i] < right_max[i]`, return `True`.
4. Otherwise, return `False`.

### Code

```python
class Solution:
    def increasingTriplet(self, nums: List[int]) -> bool:
        n = len(nums)
        if n < 3:
            return False

        left_min = [0] * n
        right_max = [0] * n

        left_min[0] = nums[0]
        for i in range(1, n):
            left_min[i] = min(left_min[i - 1], nums[i])

        right_max[-1] = nums[-1]
        for i in range(n - 2, -1, -1):
            right_max[i] = max(right_max[i + 1], nums[i])

        for i in range(1, n - 1):
            if left_min[i - 1] < nums[i] < right_max[i + 1]:
                return True

        return False
```

### Explanation

We efficiently precompute the smallest and largest values seen before and after each element, allowing O(1) lookup per element.

### Complexity

* Time: **O(n)**
* Space: **O(n)** (two extra arrays)

### Problem with this approach

* Although faster than brute force, it still requires **extra memory**, which can be significant for large inputs.

<br>

## Approach 3: Optimal Solution (O(n) Time, O(1) Space)

### Idea

We only need to track **two smallest numbers** while traversing the array:

* `first`: the smallest number found so far.
* `second`: the next number greater than `first`.

If we find any number greater than both `first` and `second`, we have an increasing triplet.

### Steps

1. Initialize `first` and `second` to infinity.
2. Traverse the array:

   * If the current number is smaller than or equal to `first`, update `first`.
   * Else if the number is smaller than or equal to `second`, update `second`.
   * Else, return `True` (since we found a number greater than both).
3. If no such triplet is found, return `False`.

### Code

```python
import sys

class Solution:
    def increasingTriplet(self, nums: List[int]) -> bool:
        if len(nums) < 3:
            return False

        first = sys.maxsize
        second = sys.maxsize

        for num in nums:
            if num <= first:
                first = num
            elif num <= second:
                second = num
            else:
                return True  # Found a number greater than both first and second

        return False
```

### Explanation

* `first` keeps track of the smallest value so far.
* `second` keeps track of the next larger value.
* When a third number greater than both is found, it confirms the existence of an increasing triplet.

### Complexity

* Time Complexity: **O(n)** — we traverse the array once.
* Space Complexity: **O(1)** — we only use two variables.

### Why this is the Best Approach

* Uses constant extra space.
* Efficient and simple logic.
* Handles large inputs easily.

<br>

## Summary of Approaches

| Approach      | Time Complexity | Space Complexity | Description                     |
| ------------- | --------------- | ---------------- | ------------------------------- |
| Brute Force   | O(n³)           | O(1)             | Checks all triplets, very slow  |
| Prefix/Suffix | O(n)            | O(n)             | Precomputes min/max arrays      |
| Optimal       | O(n)            | O(1)             | Tracks two smallest values only |


