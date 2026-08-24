# Max Number of K-Sum Pairs
`LeetCode 75`

## Problem Statement

You are given an integer array `nums` and an integer `k`.

In one operation, you can pick two numbers from the array whose sum equals `k` and remove them from the array.

Return the **maximum number of operations** you can perform on the array.

### Example 1

```python
Input: nums = [1,2,3,4], k = 5
Output: 2
```

**Explanation:**

* Remove numbers 1 and 4 → nums = [2,3]
* Remove numbers 2 and 3 → nums = []
  Total of 2 operations.

### Example 2

```python
Input: nums = [3,1,3,4,3], k = 6
Output: 1
```

**Explanation:**

* Remove two 3's → nums = [1,4,3]
  No more valid pairs remain.

<br>

## Approach 1: Using HashMap (Efficient O(n) Time)

### Idea

* For each number `x`, we check if its complement `k - x` exists in a map.
* If yes → we can form a valid pair → increase the operation count.
* If not → store the current number for future pairing.

This allows pairing numbers in a single pass.

### Code

```python
class Solution:
    def maxOperations(self, nums: List[int], k: int) -> int:
        operations = 0
        counts = {}

        for num in nums:
            complement = k - num
            if complement in counts and counts[complement] > 0:
                operations += 1
                counts[complement] -= 1
            else:
                counts[num] = counts.get(num, 0) + 1

        return operations
```

### Explanation

* We loop through all numbers.
* When we find a matching complement, we use it and reduce its count.
* If no match exists, we store the number for later use.

### Complexity

* **Time Complexity:** O(n)
* **Space Complexity:** O(n)

<br>

## Approach 2: Sorting + Two Pointers

### Why Another Approach?

While the HashMap solution is very fast, it uses extra space.
If we want to reduce space usage, we can try a **two-pointer** method after sorting the array.

### Idea

1. Sort the array.
2. Use two pointers — one at the start and one at the end.
3. Move pointers based on the sum:

   * If `nums[left] + nums[right] == k` → we found a pair → count one operation → move both pointers.
   * If the sum < k → move left pointer (need a larger number).
   * If the sum > k → move right pointer (need a smaller number).

### Code

```python
class Solution:
    def maxOperations(self, nums: List[int], k: int) -> int:
        operations = 0
        nums.sort()
        left, right = 0, len(nums) - 1

        while left < right:
            total = nums[left] + nums[right]
            if total == k:
                operations += 1
                left += 1
                right -= 1
            elif total < k:
                left += 1
            else:
                right -= 1

        return operations
```

### Explanation

* Sorting allows controlled movement of pointers.
* The left pointer increases to make the sum larger.
* The right pointer decreases to make the sum smaller.

### Complexity

* **Time Complexity:** O(n log n) (due to sorting)
* **Space Complexity:** O(1)

<br>

## Comparison Between Approaches

| Approach     | Time Complexity | Space Complexity | Notes                               |
| ------------ | --------------- | ---------------- | ----------------------------------- |
| HashMap      | O(n)            | O(n)             | Faster but uses extra space         |
| Two Pointers | O(n log n)      | O(1)             | Slightly slower but space-efficient |

<br>

## Final Thoughts

Both methods are valid and efficient.

* If memory is not a concern → **Use HashMap approach (O(n))**.
* If you want minimal space → **Use Two Pointers (O(1) extra space)**.
