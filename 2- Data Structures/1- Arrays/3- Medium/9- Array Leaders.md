# Leaders in an Array

`Amazon` • `Samsung` • `Paytm`

## Problem Statement

Given an integer array `nums`, return a list of all the **leaders** in the array.

An element is considered a **leader** if its value is **strictly greater** than all elements to its right. The **rightmost element is always a leader**. The leaders must appear in the same order as they appear in `nums`.

## Examples

**Example 1**

```
Input:  nums = [1, 2, 5, 3, 1, 2]
Output: [5, 3, 2]
```

**Explanation:**
- `2` is the rightmost element, so it is always a leader.
- `3` is strictly greater than all elements to its right: `[1, 2]`.
- `5` is strictly greater than all elements to its right: `[3, 1, 2]`.

**Example 2**

```
Input:  nums = [-3, 4, 5, 1, -4, -5]
Output: [5, 1, -4, -5]
```

**Explanation:**
- `-5` is the rightmost element, so it is always a leader.
- `-4` is strictly greater than all elements to its right: `[-5]`.
- `1` is strictly greater than all elements to its right: `[-4, -5]`.
- `5` is strictly greater than all elements to its right: `[1, -4, -5]`.

## Constraints

- `1 <= nums.length <= 10^4`
- `-10^7 <= nums[i] <= 10^7`

<br><br>

## Approach 1: Brute Force (Nested Loops)

**Intuition:**

For each element, scan every element to its right and check whether any of them is strictly greater. If none is found, the current element is a leader.

**Steps:**
1. Iterate over each index `i` from left to right.
2. For each `nums[i]`, scan all indices `j > i`.
3. If any `nums[j] > nums[i]` is found, `nums[i]` is not a leader; move on.
4. If the inner loop finishes without finding a larger element, add `nums[i]` to the result.

**Time Complexity:** O(n^2)
**Space Complexity:** O(1) (excluding the output list)

```python
class Solution:
    def leaders(self, nums):
        result = []
        n = len(nums)

        for i in range(n):
            is_leader = True

            for j in range(i + 1, n):
                if nums[j] > nums[i]:
                    is_leader = False
                    break

            if is_leader:
                result.append(nums[i])

        return result
```

**Dry Run on Example 1:** `nums = [1, 2, 5, 3, 1, 2]`

| Index | Element | Elements to Right | Leader? |
|-------|---------|-------------------|---------|
| 0     | 1       | [2, 5, 3, 1, 2]   | No (2 > 1) |
| 1     | 2       | [5, 3, 1, 2]      | No (5 > 2) |
| 2     | 5       | [3, 1, 2]         | Yes |
| 3     | 3       | [1, 2]            | Yes |
| 4     | 1       | [2]               | No (2 > 1) |
| 5     | 2       | []                | Yes (rightmost) |

**Output:** `[5, 3, 2]`

**Problem with this approach:**

For every element, we scan all elements to its right, giving us O(n^2) time in the worst case. For large inputs (up to 10^4 elements), this becomes unnecessarily slow. We are repeatedly recomputing the maximum of suffixes that heavily overlap. We can eliminate this redundancy entirely by scanning the array once from right to left.

<br><br>

## Approach 2: Optimal - Right to Left Traversal (Suffix Maximum)

**Intuition:**

Instead of looking right from every element, we traverse the array **from right to left** and keep track of the maximum value seen so far (`max_right`). At each position, if `nums[i] > max_right`, then `nums[i]` is a leader (nothing to its right is bigger). We update `max_right` accordingly.

Since we collect leaders right-to-left, we reverse the result before returning to preserve the original order.

**Steps:**
1. Start from the last element. It is always a leader, so add it to the result and set it as `max_right`.
2. Traverse from index `n-2` down to `0`.
3. At each index `i`, if `nums[i] > max_right`, it is a leader: add it to the result and update `max_right = nums[i]`.
4. Reverse the result list to restore left-to-right order and return it.

**Time Complexity:** O(n)
**Space Complexity:** O(1) (excluding the output list)

```python
class Solution:
    def leaders(self, nums):
        leaders_arr = [nums[-1]]
        max_val = nums[-1]

        for i in range(len(nums) - 2, -1, -1):
            if nums[i] > max_val:
                max_val = nums[i]
                leaders_arr.append(nums[i])

        leaders_arr.reverse()
        return leaders_arr
```

**Dry Run on Example 1:** `nums = [1, 2, 5, 3, 1, 2]`

Start: `leaders_arr = [2]`, `max_val = 2`

| Index | nums[i] | max_val | nums[i] > max_val? | leaders_arr       |
|-------|---------|---------|---------------------|-------------------|
| 4     | 1       | 2       | No                  | [2]               |
| 3     | 3       | 2       | Yes                 | [2, 3]  (max=3)   |
| 2     | 5       | 3       | Yes                 | [2, 3, 5] (max=5) |
| 1     | 2       | 5       | No                  | [2, 3, 5]         |
| 0     | 1       | 5       | No                  | [2, 3, 5]         |

After reverse: `[5, 3, 2]`

**Output:** `[5, 3, 2]`

**Dry Run on Example 2:** `nums = [-3, 4, 5, 1, -4, -5]`

Start: `leaders_arr = [-5]`, `max_val = -5`

| Index | nums[i] | max_val | nums[i] > max_val? | leaders_arr              |
|-------|---------|---------|---------------------|--------------------------|
| 4     | -4      | -5      | Yes                 | [-5, -4]  (max=-4)       |
| 3     | 1       | -4      | Yes                 | [-5, -4, 1]  (max=1)     |
| 2     | 5       | 1       | Yes                 | [-5, -4, 1, 5]  (max=5)  |
| 1     | 4       | 5       | No                  | [-5, -4, 1, 5]           |
| 0     | -3      | 5       | No                  | [-5, -4, 1, 5]           |

After reverse: `[5, 1, -4, -5]`

**Output:** `[5, 1, -4, -5]`

<br><br>

## Complexity Comparison

| Approach              | Time Complexity | Space Complexity |
|-----------------------|-----------------|------------------|
| Brute Force           | O(n^2)          | O(1)             |
| Right-to-Left Scan    | O(n)            | O(1)             |

<br><br>

## Key Takeaways

- The brute force is intuitive but wasteful; it recomputes suffix information from scratch at each index.
- The optimal solution reframes the problem: instead of asking "is anything to my right bigger?", we ask "am I bigger than everything seen so far from the right?" This allows a single linear pass.
- The reverse at the end is a simple O(n) step that keeps the output order consistent with the input, and does not affect the overall O(n) complexity.
- Edge cases to consider: a single-element array (always returns that one element), a strictly decreasing array (all elements are leaders), and a strictly increasing array (only the last element is a leader).